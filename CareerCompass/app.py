"""
CareerCompass - An Intelligent Student Career & Skill Gap Recommendation System
Flask Application, Database Operations, Security Layer, and Route Handlers.
"""

import os
import re
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, session,
    flash, abort, jsonify, g
)
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

import career_data

# Load environment configuration if available
load_dotenv()

app = Flask(__name__)

# ============================================================================
# SECURITY CONFIGURATIONS
# ============================================================================

# Secret Key configuration
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    # Safe development fallback with a clear warning
    secret_key = "careercompass-dev-fallback-key-replace-in-production"
app.config["SECRET_KEY"] = secret_key

def resolve_database_path() -> str:
    """
    Resolves the SQLite database file path.
    Supports:
    1. DATABASE_PATH env var (e.g. /var/data/careercompass.db on persistent volumes)
    2. DATABASE_URL env var if an SQLite URI is supplied (e.g. sqlite:////var/data/careercompass.db)
    3. Default local fallback ('careercompass.db' in the project directory).
    Ensures parent directories exist before connecting.
    """
    raw_path = os.environ.get("DATABASE_PATH")
    if not raw_path:
        db_url = os.environ.get("DATABASE_URL")
        if db_url and db_url.startswith("sqlite:///"):
            raw_path = db_url[len("sqlite:///"):]

    if not raw_path:
        raw_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "careercompass.db")

    abs_path = os.path.abspath(raw_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return abs_path


# Database path configuration
app.config["DATABASE_PATH"] = resolve_database_path()

# Cookie & Session Security
is_production = os.environ.get("FLASK_ENV") == "production"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=is_production,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=4),
    MAX_CONTENT_LENGTH=1024 * 1024  # 1 MB request payload limit
)

# CSRF Protection
csrf = CSRFProtect(app)

# Rate Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

# ============================================================================
# DATABASE UTILITIES
# ============================================================================

def get_db():
    """Returns the database connection for the current request context."""
    if "db" not in g:
        db_path = app.config["DATABASE_PATH"]
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        g.db = sqlite3.connect(db_path, timeout=30.0)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
        try:
            g.db.execute("PRAGMA journal_mode = WAL;")
        except sqlite3.Error:
            pass
        g.db.execute("PRAGMA busy_timeout = 30000;")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    """Closes the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initializes database schema if tables do not exist."""
    db_path = app.config["DATABASE_PATH"]
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    db = sqlite3.connect(db_path, timeout=30.0)
    db.execute("PRAGMA foreign_keys = ON;")
    try:
        db.execute("PRAGMA journal_mode = WAL;")
    except sqlite3.Error:
        pass
    db.execute("PRAGMA busy_timeout = 30000;")
    cursor = db.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        college_name TEXT NOT NULL,
        branch TEXT NOT NULL,
        academic_year TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        technical_skills TEXT,
        interests TEXT,
        preferred_career TEXT,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        taken_at TEXT NOT NULL,
        recommended_career TEXT NOT NULL,
        alternative_career TEXT,
        score_total INTEGER NOT NULL,
        percentage_total REAL NOT NULL,
        domain_scores_json TEXT NOT NULL,
        explanation TEXT NOT NULL,
        question_ids_json TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS roadmap_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        career_domain TEXT NOT NULL,
        task_id TEXT NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0,
        updated_at TEXT NOT NULL,
        UNIQUE(user_id, career_domain, task_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)
    db.commit()
    db.close()


# Ensure tables exist on startup
init_db()


# ============================================================================
# HELPER FUNCTIONS & DECORATORS
# ============================================================================

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email):
    """Validates basic RFC compliant email syntax."""
    return bool(EMAIL_REGEX.match(email.strip()))


def get_current_user():
    """Retrieves logged-in user record if session is active."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def get_user_profile(user_id):
    """Fetches user profile and unpacks JSON skills and interests."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        return None
    
    try:
        skills = json.loads(row["technical_skills"]) if row["technical_skills"] else []
    except (ValueError, TypeError):
        skills = []

    try:
        interests = json.loads(row["interests"]) if row["interests"] else []
    except (ValueError, TypeError):
        interests = []

    return {
        "user_id": row["user_id"],
        "technical_skills": skills,
        "interests": interests,
        "preferred_career": row["preferred_career"],
        "updated_at": row["updated_at"]
    }


def login_required(f):
    """Decorator to protect routes requiring student authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in or register to access this section.", "info")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def format_ist_datetime(dt_str):
    """Formats an ISO/UTC datetime string into a readable Indian Standard Time format."""
    if not dt_str:
        return ""
    try:
        # Parse UTC timestamp
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # IST is UTC + 5:30
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        ist_dt = dt.astimezone(ist_offset)
        return ist_dt.strftime("%d %b %Y, %I:%M %p IST")
    except Exception:
        return dt_str[:19].replace("T", " ")


app.jinja_env.filters["format_date"] = format_ist_datetime


def check_retake_eligibility(user_id):
    """
    Checks the 7-day retake restriction on the backend.
    Returns: (is_eligible, next_eligible_date_str, latest_attempt_row)
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM assessments WHERE user_id = ? ORDER BY taken_at DESC LIMIT 1",
        (user_id,)
    )
    latest_attempt = cursor.fetchone()
    if not latest_attempt:
        return True, None, None

    taken_at_str = latest_attempt["taken_at"]
    try:
        taken_dt = datetime.fromisoformat(taken_at_str)
        if taken_dt.tzinfo is None:
            taken_dt = taken_dt.replace(tzinfo=timezone.utc)
    except Exception:
        return True, None, latest_attempt

    now_utc = datetime.now(timezone.utc)
    eligible_dt = taken_dt + timedelta(days=7)

    if now_utc >= eligible_dt:
        return True, None, latest_attempt
    else:
        # Calculate human-readable next eligible date in IST
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        ist_next = eligible_dt.astimezone(ist_offset)
        return False, ist_next.strftime("%d %B %Y at %I:%M %p IST"), latest_attempt


def get_roadmap_stats(user_id, domain_key):
    """Computes completion percentage and task lists for a domain roadmap."""
    domain_meta = career_data.CAREER_DOMAINS.get(domain_key)
    if not domain_meta:
        return {"percentage": 0, "completed": 0, "total": 0, "remaining": 0, "tasks_state": {}}

    all_tasks = []
    for stage_data in domain_meta["roadmap"].values():
        all_tasks.extend(stage_data["tasks"])

    total_tasks = len(all_tasks)
    if total_tasks == 0:
        return {"percentage": 0, "completed": 0, "total": 0, "remaining": 0, "tasks_state": {}}

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT task_id, completed FROM roadmap_progress WHERE user_id = ? AND career_domain = ?",
        (user_id, domain_key)
    )
    rows = cursor.fetchall()
    completed_map = {r["task_id"]: bool(r["completed"]) for r in rows}

    completed_count = sum(1 for t in all_tasks if completed_map.get(t["id"], False))
    remaining_count = total_tasks - completed_count
    pct = round((completed_count / total_tasks) * 100)

    return {
        "percentage": pct,
        "completed": completed_count,
        "total": total_tasks,
        "remaining": remaining_count,
        "tasks_state": completed_map
    }


# ============================================================================
# HTTP SECURITY HEADERS & ERROR HANDLERS
# ============================================================================

@app.after_request
def set_security_headers(response):
    """Applies defense-in-depth HTTP security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'none';"
    )
    if is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.errorhandler(400)
def bad_request(error):
    return render_template("index.html", error_message="Bad Request (400): Invalid submission parameters."), 400

@app.errorhandler(403)
def forbidden(error):
    return render_template("index.html", error_message="Forbidden (403): You are not authorized to view this resource."), 403

@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", error_message="Page Not Found (404): The requested resource does not exist."), 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return render_template(
        "index.html",
        view_mode="login",
        error_message="Too many requests. For security reasons, please wait a minute before trying again."
    ), 429

@app.errorhandler(CSRFError)
def csrf_error_handler(error):
    return render_template(
        "index.html",
        error_message="Security token mismatch (CSRF). Please refresh the page and try again."
    ), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template("index.html", error_message="An unexpected server error occurred. Please try again shortly."), 500


# ============================================================================
# APPLICATION ROUTES
# ============================================================================

@app.route("/")
def index():
    """
    Main entry point:
    - Renders Landing Page (Home, About, SDGs, 5 Domains).
    - If user is logged in without completed profile, redirects to profile setup.
    - If user is logged in with profile, renders landing page with greeting and dashboard shortcuts.
    """
    user = get_current_user()
    if user:
        profile = get_user_profile(user["id"])
        if not profile or (not profile["technical_skills"] and not profile["interests"]):
            return redirect(url_for("profile"))

    return render_template("index.html", user=user, view_mode="landing")


@app.route("/about")
def about():
    """Direct route to Section 2: About CareerCompass."""
    user = get_current_user()
    return render_template("index.html", user=user, view_mode="landing", anchor="about")


@app.route("/sdgs")
def sdgs():
    """Direct route to Section 3: Our SDGs."""
    user = get_current_user()
    return render_template("index.html", user=user, view_mode="landing", anchor="sdgs")


@app.route("/domains")
def domains():
    """Direct route to explore the Five Core Tech Domains."""
    user = get_current_user()
    return render_template("index.html", user=user, view_mode="landing", anchor="domains")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handles student account creation with input validation and password hashing."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        college_name = request.form.get("college_name", "").strip()
        branch = request.form.get("branch", "").strip()
        academic_year = request.form.get("academic_year", "").strip()

        # Validation rules
        errors = []
        if not full_name or len(full_name) < 2:
            errors.append("Please provide your valid full name.")
        if not email or not is_valid_email(email):
            errors.append("Please provide a valid email address.")
        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            errors.append("Password must contain both letters and numbers.")
        if not college_name:
            errors.append("Please specify your college or university name.")
        if not branch:
            errors.append("Please enter your academic engineering branch.")
        if not academic_year:
            errors.append("Please select your current academic year.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template(
                "index.html",
                view_mode="register",
                form_data={
                    "full_name": full_name,
                    "email": email,
                    "college_name": college_name,
                    "branch": branch,
                    "academic_year": academic_year
                }
            )

        # Check existing account and create user record with robust transaction handling
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                flash("An account with this email address already exists. Please sign in.", "error")
                return render_template("index.html", view_mode="login", form_data={"email": email})

            # Secure password hash using pbkdf2 / scrypt
            pw_hash = generate_password_hash(password, method="scrypt")
            now_str = datetime.now(timezone.utc).isoformat()

            cursor.execute("""
                INSERT INTO users (full_name, email, password_hash, college_name, branch, academic_year, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (full_name, email, pw_hash, college_name, branch, academic_year, now_str))
            user_id = cursor.lastrowid

            # Initialize blank profile
            cursor.execute("""
                INSERT INTO profiles (user_id, technical_skills, interests, preferred_career, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, json.dumps([]), json.dumps([]), "", now_str))
            db.commit()

        except sqlite3.IntegrityError:
            db.rollback()
            flash("An account with this email address already exists. Please sign in.", "error")
            return render_template("index.html", view_mode="login", form_data={"email": email})
        except sqlite3.Error as e:
            db.rollback()
            app.logger.error("Database error during student registration: %s", str(e))
            flash("A temporary database error occurred while creating your account. Please try again.", "error")
            return render_template(
                "index.html",
                view_mode="register",
                form_data={
                    "full_name": full_name,
                    "email": email,
                    "college_name": college_name,
                    "branch": branch,
                    "academic_year": academic_year
                }
            )
        except Exception as e:
            db.rollback()
            app.logger.error("Unexpected error during student registration: %s", str(e))
            flash("An unexpected error occurred while processing your registration. Please try again.", "error")
            return render_template(
                "index.html",
                view_mode="register",
                form_data={
                    "full_name": full_name,
                    "email": email,
                    "college_name": college_name,
                    "branch": branch,
                    "academic_year": academic_year
                }
            )

        # Regenerate session on registration/login
        session.clear()
        session["user_id"] = user_id
        session.permanent = True

        flash(f"Welcome to CareerCompass, {full_name}! Please complete your quick profile.", "success")
        return redirect(url_for("profile"))

    return render_template("index.html", view_mode="register")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    """Handles secure student authentication with rate-limiting and session regeneration."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Invalid email or password.", "error")
            return render_template("index.html", view_mode="login", form_data={"email": email})

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        # Constant-time comparison check
        if not user or not check_password_hash(user["password_hash"], password):
            # Generic error message to prevent account enumeration
            flash("Invalid email or password.", "error")
            return render_template("index.html", view_mode="login", form_data={"email": email})

        # Session regeneration to prevent session fixation attacks
        session.clear()
        session["user_id"] = user["id"]
        session.permanent = True

        flash(f"Welcome back, {user['full_name']}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("index.html", view_mode="login")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Invalidates the student session safely."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Collects and updates technical skills, areas of interest, and preferred career."""
    user = get_current_user()
    current_profile = get_user_profile(user["id"])

    if request.method == "POST":
        selected_skills = request.form.getlist("technical_skills")
        selected_interests = request.form.getlist("interests")
        preferred_career = request.form.get("preferred_career", "").strip()

        # Sanitize selections against taxonomy
        valid_skills = [s for s in selected_skills if s in career_data.ALL_TECHNICAL_SKILLS]
        valid_interests = [i for i in selected_interests if i in career_data.ALL_INTERESTS]
        if preferred_career not in career_data.CAREER_DOMAINS and preferred_career != "":
            preferred_career = ""

        now_str = datetime.now(timezone.utc).isoformat()
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO profiles (user_id, technical_skills, interests, preferred_career, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    technical_skills = excluded.technical_skills,
                    interests = excluded.interests,
                    preferred_career = excluded.preferred_career,
                    updated_at = excluded.updated_at
            """, (
                user["id"],
                json.dumps(valid_skills),
                json.dumps(valid_interests),
                preferred_career,
                now_str
            ))
            db.commit()
            flash("Your profile details have been saved successfully!", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.Error as e:
            db.rollback()
            app.logger.error("Database error updating profile: %s", str(e))
            flash("A temporary database error occurred while updating your profile. Please try again.", "error")
            return render_template(
                "index.html",
                view_mode="profile",
                user=user,
                profile=current_profile,
                active_skills=valid_skills,
                active_interests=valid_interests,
                active_pref_career=preferred_career
            )

    return render_template(
        "index.html",
        view_mode="profile",
        user=user,
        profile=current_profile,
        all_skills=career_data.ALL_TECHNICAL_SKILLS,
        all_interests=career_data.ALL_INTERESTS,
        career_domains=career_data.CAREER_DOMAINS
    )


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Renders the simplified 4-section student dashboard:
    1. My Career: Recommended domain & description
    2. My Progress: Latest score, previous score, improvement indicator
    3. My Roadmap: Completion %, completed tasks, remaining tasks
    4. Retake Test: Eligibility & next eligible assessment date
    """
    user = get_current_user()
    profile = get_user_profile(user["id"])

    db = get_db()
    cursor = db.cursor()
    # Fetch last 2 attempts to compare progress
    cursor.execute("""
        SELECT * FROM assessments
        WHERE user_id = ?
        ORDER BY taken_at DESC
        LIMIT 2
    """, (user["id"],))
    attempts = cursor.fetchall()

    latest_attempt = attempts[0] if len(attempts) > 0 else None
    previous_attempt = attempts[1] if len(attempts) > 1 else None

    # Check 7-day retake eligibility
    is_eligible, next_eligible_date, _ = check_retake_eligibility(user["id"])

    # Roadmap progress and career metadata for the recommended career
    recommended_domain = latest_attempt["recommended_career"] if latest_attempt else None
    roadmap_stats = None
    rec_meta = None
    domain_scores = {}

    if recommended_domain:
        roadmap_stats = get_roadmap_stats(user["id"], recommended_domain)
        rec_meta = career_data.CAREER_DOMAINS.get(recommended_domain)

    if latest_attempt and latest_attempt["domain_scores_json"]:
        try:
            domain_scores = json.loads(latest_attempt["domain_scores_json"])
        except Exception:
            domain_scores = {}

    # Progress comparison indicator
    progress_comparison = None
    if latest_attempt and previous_attempt:
        delta = latest_attempt["score_total"] - previous_attempt["score_total"]
        pct_delta = round(latest_attempt["percentage_total"] - previous_attempt["percentage_total"], 1)
        progress_comparison = {
            "delta": delta,
            "pct_delta": pct_delta,
            "status": "improved" if delta > 0 else ("declined" if delta < 0 else "neutral")
        }

    active_domain_key = recommended_domain or (profile.get("preferred_career") if profile else None) or "data_analytics"
    verified_sources = career_data.VERIFIED_SOURCES.get(active_domain_key, [])
    youtube_resources = career_data.YOUTUBE_RESOURCES.get(active_domain_key, [])

    return render_template(
        "index.html",
        view_mode="dashboard",
        user=user,
        profile=profile,
        latest_attempt=latest_attempt,
        previous_attempt=previous_attempt,
        progress_comparison=progress_comparison,
        is_eligible=is_eligible,
        next_eligible_date=next_eligible_date,
        roadmap_stats=roadmap_stats,
        rec_meta=rec_meta,
        domain_scores=domain_scores,
        career_domains=career_data.CAREER_DOMAINS,
        active_domain_key=active_domain_key,
        verified_sources=verified_sources,
        youtube_resources=youtube_resources,
        all_verified_sources=career_data.VERIFIED_SOURCES,
        all_youtube_resources=career_data.YOUTUBE_RESOURCES
    )


@app.route("/assessment")
@login_required
def assessment():
    """
    Prepares and presents the 25-MCQ skill assessment:
    - Enforces the 7-day retake restriction on backend.
    - Samples exactly 25 questions (5 per domain, 3 basic + 2 practical).
    - Shuffles questions and stores question IDs in session.
    """
    user = get_current_user()
    is_eligible, next_date_str, _ = check_retake_eligibility(user["id"])

    if not is_eligible:
        flash(f"You can retake the assessment once every 7 days. Your next attempt is eligible on {next_date_str}.", "warning")
        return redirect(url_for("dashboard"))

    # Generate or reload active assessment question set
    # Sampling 25 questions: exactly 5 per domain (3 basic, 2 practical)
    sampled_questions = career_data.generate_assessment_question_set()
    question_ids = [q["id"] for q in sampled_questions]
    session["active_assessment_qids"] = question_ids

    # Strip correct answers and explanations before rendering to client
    clean_questions = []
    for q in sampled_questions:
        clean_questions.append({
            "id": q["id"],
            "domain": q["domain"],
            "domain_title": career_data.CAREER_DOMAINS[q["domain"]]["title"],
            "type": q["type"],
            "question": q["question"],
            "options": q["options"]
        })

    return render_template(
        "index.html",
        view_mode="assessment",
        user=user,
        questions=clean_questions,
        total_questions=len(clean_questions)
    )


@app.route("/assessment/submit", methods=["POST"])
@login_required
def submit_assessment():
    """
    Evaluates the submitted 25-MCQ assessment:
    - Validates 7-day retake rule on backend.
    - Evaluates each domain independently (0..5 score, percentage, level).
    - Determines top career recommendation with tie-breaking rules.
    - Persists attempt in SQLite database.
    - Redirects to results.html.
    """
    user = get_current_user()
    is_eligible, next_date_str, _ = check_retake_eligibility(user["id"])

    if not is_eligible:
        flash(f"Retake restriction active. Next assessment available on {next_date_str}.", "warning")
        return redirect(url_for("dashboard"))

    question_ids = session.get("active_assessment_qids")
    if not question_ids or len(question_ids) != 25:
        flash("Assessment session expired or invalid. Please start a fresh assessment.", "error")
        return redirect(url_for("assessment"))

    # Collect answers from request form
    submitted_answers = {}
    for qid in question_ids:
        answer_val = request.form.get(f"q_{qid}")
        if answer_val is not None:
            submitted_answers[qid] = answer_val

    profile = get_user_profile(user["id"])
    evaluation = career_data.evaluate_assessment(submitted_answers, question_ids, profile)

    # Save attempt in database with transaction safety
    now_str = datetime.now(timezone.utc).isoformat()
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO assessments (
                user_id, taken_at, recommended_career, alternative_career,
                score_total, percentage_total, domain_scores_json, explanation, question_ids_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user["id"],
            now_str,
            evaluation["recommended_career"],
            evaluation["alternative_career"],
            evaluation["total_score"],
            evaluation["overall_percentage"],
            json.dumps(evaluation["domain_scores"]),
            evaluation["recommendation_explanation"],
            json.dumps(question_ids)
        ))
        assessment_id = cursor.lastrowid

        # Auto-initialize roadmap task rows for recommended career
        rec_domain = evaluation["recommended_career"]
        domain_meta = career_data.CAREER_DOMAINS[rec_domain]
        for stage_data in domain_meta["roadmap"].values():
            for task in stage_data["tasks"]:
                cursor.execute("""
                    INSERT OR IGNORE INTO roadmap_progress (user_id, career_domain, task_id, completed, updated_at)
                    VALUES (?, ?, ?, 0, ?)
                """, (user["id"], rec_domain, task["id"], now_str))

        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        app.logger.error("Database error saving assessment attempt: %s", str(e))
        flash("A database error occurred while saving your assessment. Please try submitting again.", "error")
        return redirect(url_for("assessment"))

    # Clear session question IDs
    session.pop("active_assessment_qids", None)

    flash("Assessment submitted successfully! Here are your detailed results.", "success")
    return redirect(url_for("view_results", assessment_id=assessment_id))


@app.route("/results")
@app.route("/results/<int:assessment_id>")
@login_required
def view_results(assessment_id=None):
    """
    Renders results.html:
    - Career recommendations and proficiency level.
    - 5-domain score comparison.
    - 3-category skill gap analysis (Already Have, Need to Improve, Should Learn Next).
    - 3-stage personalized learning roadmap with interactive task checkboxes.
    """
    user = get_current_user()
    profile = get_user_profile(user["id"])
    db = get_db()
    cursor = db.cursor()

    if assessment_id:
        cursor.execute(
            "SELECT * FROM assessments WHERE id = ? AND user_id = ?",
            (assessment_id, user["id"])
        )
    else:
        cursor.execute(
            "SELECT * FROM assessments WHERE user_id = ? ORDER BY taken_at DESC LIMIT 1",
            (user["id"],)
        )
    attempt = cursor.fetchone()

    if not attempt:
        flash("No assessment results found. Please complete the skill assessment first.", "info")
        return redirect(url_for("assessment"))

    domain_scores = json.loads(attempt["domain_scores_json"])
    recommended_domain = attempt["recommended_career"]
    alternative_domain = attempt["alternative_career"]

    # If alternative is missing, dynamically pick runner up domain
    if not alternative_domain:
        other_domains = [k for k in career_data.CAREER_DOMAINS.keys() if k != recommended_domain]
        other_domains.sort(key=lambda k: domain_scores.get(k, {}).get("score", 0), reverse=True)
        if other_domains:
            alternative_domain = other_domains[0]

    rec_meta = career_data.CAREER_DOMAINS.get(recommended_domain)
    alt_meta = career_data.CAREER_DOMAINS.get(alternative_domain) if alternative_domain else None

    user_skills = profile.get("technical_skills", []) if profile else []

    def calculate_domain_skill_gap(meta, skills_list, score):
        if not meta:
            return {"already_have": [], "need_improvement": [], "should_learn_next": []}
        core = meta["core_skills"]
        have = [s for s in core if s in skills_list]
        if score < 4:
            improve = [s for s in core if s in have]
            learn = [s for s in core if s not in have]
            if not improve and core:
                improve = [core[0]]
                learn = core[1:]
        else:
            improve = [s for s in core if s not in have][:1]
            learn = [s for s in core if s not in have and s not in improve]
        return {"already_have": have, "need_improvement": improve, "should_learn_next": learn}

    rec_score = domain_scores.get(recommended_domain, {}).get("score", 0)
    skill_gap = calculate_domain_skill_gap(rec_meta, user_skills, rec_score)

    alt_score = domain_scores.get(alternative_domain, {}).get("score", 0) if alternative_domain else 0
    alt_skill_gap = calculate_domain_skill_gap(alt_meta, user_skills, alt_score) if alt_meta else None

    # Fetch roadmap progress for BOTH options
    roadmap_stats = get_roadmap_stats(user["id"], recommended_domain)
    alt_roadmap_stats = get_roadmap_stats(user["id"], alternative_domain) if alternative_domain else None

    # Check 7-day retake eligibility
    is_eligible, next_date_str, _ = check_retake_eligibility(user["id"])

    return render_template(
        "results.html",
        user=user,
        attempt=attempt,
        domain_scores=domain_scores,
        recommended_meta=rec_meta,
        alternative_meta=alt_meta,
        skill_gap=skill_gap,
        alt_skill_gap=alt_skill_gap,
        roadmap_stats=roadmap_stats,
        alt_roadmap_stats=alt_roadmap_stats,
        is_eligible=is_eligible,
        next_eligible_date=next_date_str,
        all_verified_sources=career_data.VERIFIED_SOURCES,
        all_youtube_resources=career_data.YOUTUBE_RESOURCES
    )


@app.route("/assessment/select-career", methods=["POST"])
@login_required
def select_career_track():
    """
    Allows the student to choose between the top two recommended career directions.
    Saves their active choice in both the assessment record and student profile.
    """
    user = get_current_user()
    assessment_id = request.form.get("assessment_id")
    chosen_career = request.form.get("chosen_career", "").strip()

    if not assessment_id or chosen_career not in career_data.CAREER_DOMAINS:
        flash("Invalid career choice.", "error")
        return redirect(url_for("view_results"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM assessments WHERE id = ? AND user_id = ?",
        (assessment_id, user["id"])
    )
    attempt = cursor.fetchone()
    if not attempt:
        flash("Assessment record not found.", "error")
        return redirect(url_for("view_results"))

    current_rec = attempt["recommended_career"]
    current_alt = attempt["alternative_career"]

    valid_options = [current_rec, current_alt]
    if chosen_career not in valid_options:
        flash("You can only select from your top two recommended career options.", "warning")
        return redirect(url_for("view_results", assessment_id=assessment_id))

    other_career = current_rec if chosen_career == current_alt else current_alt
    now_str = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute("""
            UPDATE assessments
            SET recommended_career = ?, alternative_career = ?
            WHERE id = ? AND user_id = ?
        """, (chosen_career, other_career, assessment_id, user["id"]))

        cursor.execute("""
            UPDATE profiles
            SET preferred_career = ?, updated_at = ?
            WHERE user_id = ?
        """, (chosen_career, now_str, user["id"]))

        # Initialize roadmap tasks for chosen career in case they are not yet initialized
        chosen_meta = career_data.CAREER_DOMAINS[chosen_career]
        for stage_data in chosen_meta["roadmap"].values():
            for task in stage_data["tasks"]:
                cursor.execute("""
                    INSERT OR IGNORE INTO roadmap_progress (user_id, career_domain, task_id, completed, updated_at)
                    VALUES (?, ?, ?, 0, ?)
                """, (user["id"], chosen_career, task["id"], now_str))

        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        app.logger.error("Database error updating career track: %s", str(e))
        flash("A temporary database error occurred while selecting your track. Please try again.", "error")
        return redirect(url_for("view_results", assessment_id=assessment_id))

    chosen_title = career_data.CAREER_DOMAINS[chosen_career]["title"]
    flash(f"Success! You have selected {chosen_title} as your active primary career roadmap and dashboard focus.", "success")
    return redirect(url_for("view_results", assessment_id=assessment_id))


@app.route("/roadmap/toggle", methods=["POST"])
@login_required
def toggle_roadmap_task():
    """Toggles completion status for a roadmap task, saving progress in SQLite."""
    user = get_current_user()
    domain_key = request.form.get("domain_key", "").strip()
    task_id = request.form.get("task_id", "").strip()
    completed_val = request.form.get("completed")

    if not domain_key or not task_id or domain_key not in career_data.CAREER_DOMAINS:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "error", "message": "Invalid task parameters."}), 400
        flash("Invalid task parameters.", "error")
        return redirect(url_for("dashboard"))

    # Convert to 1 or 0
    is_completed = 1 if completed_val in ["1", "true", "True", "on"] else 0
    now_str = datetime.now(timezone.utc).isoformat()

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO roadmap_progress (user_id, career_domain, task_id, completed, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, career_domain, task_id) DO UPDATE SET
                completed = excluded.completed,
                updated_at = excluded.updated_at
        """, (user["id"], domain_key, task_id, is_completed, now_str))
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        app.logger.error("Database error toggling task: %s", str(e))
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "error", "message": "Database error updating task."}), 500
        flash("A database error occurred while updating task progress.", "error")
        return redirect(url_for("dashboard"))

    stats = get_roadmap_stats(user["id"], domain_key)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "status": "success",
            "task_id": task_id,
            "completed": bool(is_completed),
            "percentage": stats["percentage"],
            "completed_count": stats["completed"],
            "total_count": stats["total"],
            "remaining_count": stats["remaining"]
        })

    flash("Roadmap task progress updated!", "success")
    return redirect(request.referrer or url_for("view_results"))


# ============================================================================
# RUN APPLICATION (LOCAL DEVELOPMENT)
# ============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=port, debug=debug_mode)
