"""
Automated Test Suite for CareerCompass Web Application.

Tests all key requirements:
1. Application initialization and configuration.
2. User registration and email normalization.
3. Duplicate registration rejection.
4. Secure password hashing (Werkzeug scrypt/pbkdf2, no plain text).
5. User authentication with valid credentials.
6. Rejection of invalid credentials.
7. Logout and session invalidation.
8. Student data isolation (preventing unauthorized access to another student's data).
9. Assessment generation: exactly 25 questions, exactly 5 per domain (3 basic, 2 practical).
10. Assessment evaluation and domain score calculation accuracy.
11. Career recommendation logic and tie-breaking.
12. Backend enforcement of the 7-day retake cooldown.
13. Roadmap progress persistence in SQLite database.
14. CSRF protection verification for state-changing POST requests.
"""

import os
import json
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

# Ensure project root is in path
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import app as flask_app
import career_data


class CareerCompassTestCase(unittest.TestCase):
    def setUp(self):
        """Creates a dedicated isolated temporary SQLite database for each test."""
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        flask_app.app.config["DATABASE_PATH"] = self.db_path
        flask_app.app.config["TESTING"] = True
        flask_app.app.config["WTF_CSRF_ENABLED"] = False  # Disabled by default for functional tests
        flask_app.app.config["SECRET_KEY"] = "test-secret-key-for-automated-verification"
        
        # Initialize schema in clean temporary database
        with flask_app.app.app_context():
            flask_app.init_db()

        self.client = flask_app.app.test_client()

    def tearDown(self):
        """Cleans up and removes temporary database files."""
        os.close(self.db_fd)
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    # ------------------------------------------------------------------------
    # 1. APPLICATION & HOMEPAGE
    # ------------------------------------------------------------------------
    def test_application_starts_and_renders_landing(self):
        """Verify app starts successfully and renders landing page with 4 main nav sections."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        content = response.data.decode("utf-8")
        self.assertIn("CareerCompass", content)
        self.assertIn("Find Your Direction. Build Your Future.", content)
        self.assertIn("SDG 4: Quality Education", content)
        self.assertIn("SDG 8: Decent Work", content)

    # ------------------------------------------------------------------------
    # 2. USER REGISTRATION & EMAIL NORMALIZATION
    # ------------------------------------------------------------------------
    def test_user_registration_success(self):
        """Verify student registration succeeds with the 6 required fields."""
        post_data = {
            "full_name": "Aarav Sharma",
            "email": "  Aarav.Sharma@College.EDU  ",  # Mixed case and spaces to test normalization
            "password": "Password123",
            "college_name": "Government Engineering College",
            "branch": "Artificial Intelligence & Data Science",
            "academic_year": "Second Year (SE)"
        }
        response = self.client.post("/register", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check user exists in DB with normalized email
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT * FROM users WHERE email = 'aarav.sharma@college.edu'").fetchone()
        conn.close()

        self.assertIsNotNone(user)
        self.assertEqual(user["full_name"], "Aarav Sharma")
        self.assertEqual(user["college_name"], "Government Engineering College")

    # ------------------------------------------------------------------------
    # 3. DUPLICATE REGISTRATION REJECTION
    # ------------------------------------------------------------------------
    def test_duplicate_email_registration_rejected(self):
        """Verify duplicate email registration is rejected."""
        user_data = {
            "full_name": "Student One",
            "email": "duplicate@test.com",
            "password": "Password123",
            "college_name": "Test College",
            "branch": "AI & DS",
            "academic_year": "Second Year (SE)"
        }
        # First registration
        self.client.post("/register", data=user_data, follow_redirects=True)

        # Clear session to act as new user registering
        self.client.get("/logout", follow_redirects=True)

        # Second registration with same email
        resp2 = self.client.post("/register", data=user_data, follow_redirects=True)
        self.assertIn("already exists", resp2.data.decode("utf-8"))

    # ------------------------------------------------------------------------
    # 4. SECURE PASSWORD HASHING
    # ------------------------------------------------------------------------
    def test_passwords_are_stored_as_secure_hashes(self):
        """Verify plain passwords are never stored in the database."""
        raw_password = "StrictlySecretPassword99"
        self.client.post("/register", data={
            "full_name": "Security Tester",
            "email": "security@test.com",
            "password": raw_password,
            "college_name": "Security Institute",
            "branch": "Cybersecurity",
            "academic_year": "Third Year (TE)"
        }, follow_redirects=True)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT password_hash FROM users WHERE email = 'security@test.com'").fetchone()
        conn.close()

        stored_hash = user["password_hash"]
        self.assertNotEqual(stored_hash, raw_password)
        self.assertNotIn(raw_password, stored_hash)
        self.assertTrue(stored_hash.startswith("scrypt:") or stored_hash.startswith("pbkdf2:"))

    # ------------------------------------------------------------------------
    # 5 & 6. LOGIN WITH VALID & INVALID CREDENTIALS
    # ------------------------------------------------------------------------
    def test_login_and_invalid_credentials_handling(self):
        """Verify login works with correct credentials and rejects incorrect ones."""
        # Register user
        self.client.post("/register", data={
            "full_name": "Pooja Patel",
            "email": "pooja@college.edu",
            "password": "CorrectPassword123",
            "college_name": "Engineering College",
            "branch": "Data Science",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Logout
        self.client.post("/logout", follow_redirects=True)

        # Attempt login with WRONG password
        bad_resp = self.client.post("/login", data={
            "email": "pooja@college.edu",
            "password": "WrongPassword999"
        }, follow_redirects=True)
        self.assertIn("Invalid email or password", bad_resp.data.decode("utf-8"))

        # Attempt login with CORRECT password
        good_resp = self.client.post("/login", data={
            "email": "pooja@college.edu",
            "password": "CorrectPassword123"
        }, follow_redirects=True)
        self.assertEqual(good_resp.status_code, 200)
        self.assertIn("Welcome back, Pooja Patel!", good_resp.data.decode("utf-8"))

    # ------------------------------------------------------------------------
    # 7. LOGOUT AND SESSION TERMINATION
    # ------------------------------------------------------------------------
    def test_logout_invalidates_session(self):
        """Verify logout invalidates the user session."""
        self.client.post("/register", data={
            "full_name": "Rohan Mehra",
            "email": "rohan@test.com",
            "password": "Password123",
            "college_name": "Tech Institute",
            "branch": "AI",
            "academic_year": "Final Year (BE)"
        }, follow_redirects=True)

        # Ensure dashboard accessible while logged in
        dash_resp = self.client.get("/dashboard")
        self.assertEqual(dash_resp.status_code, 200)

        # Logout
        self.client.post("/logout", follow_redirects=True)

        # Dashboard should redirect to login when logged out
        dash_after = self.client.get("/dashboard")
        self.assertEqual(dash_after.status_code, 302)
        self.assertIn("/login", dash_after.headers["Location"])

    # ------------------------------------------------------------------------
    # 8. DATA ISOLATION BETWEEN STUDENTS
    # ------------------------------------------------------------------------
    def test_student_data_isolation(self):
        """Verify Student A cannot view or tamper with Student B's assessment results."""
        # Create Student A
        self.client.post("/register", data={
            "full_name": "Student A",
            "email": "student_a@test.com",
            "password": "PasswordA123",
            "college_name": "College A",
            "branch": "Branch A",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Insert assessment record for Student A in DB
        now_str = datetime.now(timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = 'student_a@test.com'")
        user_a_id = cursor.fetchone()[0]

        domain_scores_sample = {
            "data_analytics": {"title": "Data Analytics", "score": 5, "total": 5, "percentage": 100.0, "level": "Strong Foundation"},
            "machine_learning_ai": {"title": "Machine Learning", "score": 3, "total": 5, "percentage": 60.0, "level": "Developing"},
            "data_science": {"title": "Data Science", "score": 4, "total": 5, "percentage": 80.0, "level": "Strong Foundation"},
            "deep_learning_genai": {"title": "Deep Learning", "score": 2, "total": 5, "percentage": 40.0, "level": "Developing"},
            "full_stack": {"title": "Full-Stack", "score": 2, "total": 5, "percentage": 40.0, "level": "Developing"}
        }

        cursor.execute("""
            INSERT INTO assessments (
                user_id, taken_at, recommended_career, alternative_career,
                score_total, percentage_total, domain_scores_json, explanation, question_ids_json
            ) VALUES (?, ?, 'data_analytics', 'data_science', 16, 64.0, ?, 'Explanation A', '[]')
        """, (user_a_id, now_str, json.dumps(domain_scores_sample)))
        assessment_a_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Logout Student A
        self.client.post("/logout", follow_redirects=True)

        # Register and login Student B
        self.client.post("/register", data={
            "full_name": "Student B",
            "email": "student_b@test.com",
            "password": "PasswordB123",
            "college_name": "College B",
            "branch": "Branch B",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Student B attempts to access Student A's result via /results/<assessment_a_id>
        resp = self.client.get(f"/results/{assessment_a_id}", follow_redirects=True)
        # Should NOT display Student A's result, should flash info and redirect
        self.assertNotIn("Explanation A", resp.data.decode("utf-8"))
        self.assertIn("No assessment results found", resp.data.decode("utf-8"))

    # ------------------------------------------------------------------------
    # 9. ASSESSMENT QUESTION BANK & SAMPLING INTEGRITY
    # ------------------------------------------------------------------------
    def test_assessment_sampling_exact_counts(self):
        """Verify sampling generates exactly 25 questions: 5 per domain (3 basic, 2 practical)."""
        sampled = career_data.generate_assessment_question_set()
        self.assertEqual(len(sampled), 25, "Assessment must contain exactly 25 questions.")

        domains = {}
        types = {"basic": 0, "practical": 0}
        for q in sampled:
            dom = q["domain"]
            domains[dom] = domains.get(dom, 0) + 1
            types[q["type"]] += 1

        self.assertEqual(len(domains), 5, "All 5 domains must be represented.")
        for dom, count in domains.items():
            self.assertEqual(count, 5, f"Domain {dom} must have exactly 5 questions.")

        self.assertEqual(types["basic"], 15, "Total basic questions must be exactly 15.")
        self.assertEqual(types["practical"], 10, "Total practical questions must be exactly 10.")

    # ------------------------------------------------------------------------
    # 10 & 11. SCORING ACCURACY & CAREER RECOMMENDATION LOGIC
    # ------------------------------------------------------------------------
    def test_scoring_and_recommendation_evaluation(self):
        """Verify domain percentage calculations and recommendation tie-breaking."""
        # Sample question set with fixed seed
        sampled = career_data.generate_assessment_question_set(seed=42)
        qids = [q["id"] for q in sampled]

        # Formulate answers: answer all Data Analytics correctly, half of others
        answers = {}
        for q in sampled:
            if q["domain"] == "data_analytics":
                answers[q["id"]] = q["answer"]  # Correct answer (5/5 = 100%)
            else:
                answers[q["id"]] = (q["answer"] + 1) % 4  # Deliberately incorrect

        profile = {
            "technical_skills": ["SQL", "Power BI"],
            "interests": ["Data Analysis & Visualization"],
            "preferred_career": "data_analytics"
        }

        evaluation = career_data.evaluate_assessment(answers, qids, profile)

        # Check Data Analytics domain score
        da_eval = evaluation["domain_scores"]["data_analytics"]
        self.assertEqual(da_eval["score"], 5)
        self.assertEqual(da_eval["percentage"], 100.0)
        self.assertEqual(da_eval["level"], "Strong Foundation")

        # Check Recommended Career
        self.assertEqual(evaluation["recommended_career"], "data_analytics")
        self.assertIsNotNone(evaluation["alternative_career"])

        # Check Skill Gap Analysis output
        sg = evaluation["skill_gap"]
        self.assertIn("SQL", sg["already_have"])
        self.assertIn("Power BI", sg["already_have"])

    # ------------------------------------------------------------------------
    # 12. RETAKE RESTRICTION (7-DAY COOLDOWN ENFORCEMENT)
    # ------------------------------------------------------------------------
    def test_retake_restriction_7_day_rule_enforced(self):
        """Verify backend blocks assessment retake within 7 days of previous attempt."""
        # Register user
        self.client.post("/register", data={
            "full_name": "Cooldown Tester",
            "email": "cooldown@test.com",
            "password": "Password123",
            "college_name": "Cooldown College",
            "branch": "AI & DS",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Insert recent assessment attempt (2 days ago)
        recent_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = 'cooldown@test.com'")
        uid = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO assessments (
                user_id, taken_at, recommended_career, alternative_career,
                score_total, percentage_total, domain_scores_json, explanation, question_ids_json
            ) VALUES (?, ?, 'full_stack', 'data_science', 18, 72.0, '{}', 'Exp', '[]')
        """, (uid, recent_date))
        conn.commit()
        conn.close()

        # Student attempts to navigate to /assessment
        resp = self.client.get("/assessment", follow_redirects=True)
        content = resp.data.decode("utf-8")
        self.assertIn("You can retake the assessment once every 7 days", content)

        # Attempt to POST answers to /assessment/submit
        post_resp = self.client.post("/assessment/submit", data={}, follow_redirects=True)
        self.assertIn("Retake restriction active", post_resp.data.decode("utf-8"))

    # ------------------------------------------------------------------------
    # 13. ROADMAP PROGRESS PERSISTENCE
    # ------------------------------------------------------------------------
    def test_roadmap_progress_toggle_and_persistence(self):
        """Verify roadmap tasks save completion status in SQLite database."""
        self.client.post("/register", data={
            "full_name": "Roadmap Learner",
            "email": "learner@test.com",
            "password": "Password123",
            "college_name": "Learning Academy",
            "branch": "Computer Engineering",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Toggle roadmap task 'da_s1_t1' as completed
        toggle_data = {
            "domain_key": "data_analytics",
            "task_id": "da_s1_t1",
            "completed": "1"
        }
        resp = self.client.post("/roadmap/toggle", data=toggle_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # Verify record in database
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("""
            SELECT completed FROM roadmap_progress
            WHERE career_domain = 'data_analytics' AND task_id = 'da_s1_t1'
        """).fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row["completed"], 1)

    # ------------------------------------------------------------------------
    # 14. TOP TWO CAREER OPTIONS & USER SELECTION
    # ------------------------------------------------------------------------
    def test_select_career_path_between_top_two_options(self):
        """Verify student can choose between the top two suggested career directions."""
        self.client.post("/register", data={
            "full_name": "Career Chooser",
            "email": "chooser@test.com",
            "password": "Password123",
            "college_name": "Test College",
            "branch": "AI & DS",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # Insert an assessment with Option 1: data_analytics, Option 2: data_science
        now_str = datetime.now(timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = 'chooser@test.com'")
        uid = cursor.fetchone()[0]

        scores_dict = {
            "data_analytics": {"title": "Data Analytics", "score": 5, "total": 5, "percentage": 100.0, "level": "Strong Foundation"},
            "data_science": {"title": "Data Science", "score": 4, "total": 5, "percentage": 80.0, "level": "Strong Foundation"},
            "machine_learning_ai": {"title": "ML", "score": 2, "total": 5, "percentage": 40.0, "level": "Developing"},
            "deep_learning_genai": {"title": "DL", "score": 2, "total": 5, "percentage": 40.0, "level": "Developing"},
            "full_stack": {"title": "FS", "score": 1, "total": 5, "percentage": 20.0, "level": "Beginner"}
        }

        cursor.execute("""
            INSERT INTO assessments (
                user_id, taken_at, recommended_career, alternative_career,
                score_total, percentage_total, domain_scores_json, explanation, question_ids_json
            ) VALUES (?, ?, 'data_analytics', 'data_science', 14, 56.0, ?, 'Explanation', '[]')
        """, (uid, now_str, json.dumps(scores_dict)))
        aid = cursor.lastrowid
        conn.commit()
        conn.close()

        # Student selects Option 2: data_science as their primary track
        resp = self.client.post("/assessment/select-career", data={
            "assessment_id": aid,
            "chosen_career": "data_science"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Success! You have selected Data Science", resp.data.decode("utf-8"))

        # Verify DB updated
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        updated_assessment = conn.execute("SELECT * FROM assessments WHERE id = ?", (aid,)).fetchone()
        updated_profile = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (uid,)).fetchone()
        conn.close()

        self.assertEqual(updated_assessment["recommended_career"], "data_science")
        self.assertEqual(updated_assessment["alternative_career"], "data_analytics")
        self.assertEqual(updated_profile["preferred_career"], "data_science")

    # ------------------------------------------------------------------------
    # 14. ASSESSMENT WITH DEFAULT "UNVERSED" ANSWERS
    # ------------------------------------------------------------------------
    def test_assessment_evaluation_with_unversed_answers(self):
        """Verify student submitting assessment with 'unversed' default options evaluates safely without penalty."""
        # 1. Register student
        self.client.post("/register", data={
            "full_name": "Rohan Deshmukh",
            "email": "rohan.deshmukh@college.edu",
            "password": "Password123",
            "college_name": "Engineering College",
            "branch": "Computer Engineering",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)

        # 2. Login
        self.client.post("/login", data={
            "email": "rohan.deshmukh@college.edu",
            "password": "Password123"
        }, follow_redirects=True)

        # 3. Complete profile with preferred career 'full_stack'
        self.client.post("/profile", data={
            "technical_skills": ["HTML", "CSS"],
            "interests": ["Web Applications & APIs"],
            "preferred_career": "full_stack"
        }, follow_redirects=True)

        # 4. Access assessment to populate session question set
        get_resp = self.client.get("/assessment")
        self.assertEqual(get_resp.status_code, 200)

        with self.client.session_transaction() as sess:
            q_ids = sess.get("active_assessment_qids", [])

        self.assertEqual(len(q_ids), 25)

        # 5. Submit all 25 questions with 'unversed' (as pre-checked in the UI)
        post_answers = {f"q_{qid}": "unversed" for qid in q_ids}
        submit_resp = self.client.post("/assessment/submit", data=post_answers, follow_redirects=True)
        self.assertEqual(submit_resp.status_code, 200)
        html_content = submit_resp.data.decode("utf-8")

        # 6. Verify result page contains 0/25 score, beginner level, and unversed explanation
        self.assertIn("Total Assessment Score: <strong>0 / 25</strong>", html_content)
        self.assertIn("Unversed", html_content)
        self.assertIn("marked as Unversed", html_content)

        # Verify DB records
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT id FROM users WHERE email = 'rohan.deshmukh@college.edu'").fetchone()
        attempt = conn.execute("SELECT * FROM assessments WHERE user_id = ?", (user["id"],)).fetchone()
        conn.close()

        self.assertIsNotNone(attempt)
        self.assertEqual(attempt["score_total"], 0)
        self.assertEqual(attempt["percentage_total"], 0.0)
        # Tie break falls back to preferred_career
        self.assertEqual(attempt["recommended_career"], "full_stack")
        self.assertIn("You selected 'Unversed' on 25 questions", attempt["explanation"])

    # ------------------------------------------------------------------------
    # 15. VERIFIED SOURCES & YOUTUBE RESOURCES VERIFICATION
    # ------------------------------------------------------------------------
    def test_verified_sources_data_integrity(self):
        """Verify each of the 5 domains has exactly 5 verified sources with at least 2 free and remaining paid."""
        for dom_key in career_data.CAREER_DOMAINS.keys():
            sources = career_data.VERIFIED_SOURCES.get(dom_key, [])
            yt_res = career_data.YOUTUBE_RESOURCES.get(dom_key, [])
            self.assertEqual(len(sources), 5, f"{dom_key} must have exactly 5 verified sources")
            free_count = sum(1 for s in sources if s["is_free"] and s["type"] == "Free")
            paid_count = sum(1 for s in sources if not s["is_free"] and s["type"] == "Paid")
            self.assertGreaterEqual(free_count, 2, f"{dom_key} must have at least 2 free sources")
            self.assertEqual(free_count + paid_count, 5, f"{dom_key} sources must all be classified as Free or Paid")
            self.assertGreaterEqual(len(yt_res), 3, f"{dom_key} must have YouTube resources")

    def test_navigation_tabs_have_no_number_series(self):
        """Verify navigation links and tab titles do not contain numbers like '1. Home'."""
        response = self.client.get("/")
        content = response.data.decode("utf-8")
        self.assertIn('>Home</a>', content)
        self.assertIn('>About CareerCompass</a>', content)
        self.assertIn('>Our SDGs</a>', content)
        self.assertNotIn('>1. Home</a>', content)
        self.assertNotIn('>2. About CareerCompass</a>', content)
        self.assertNotIn('>3. Our SDGs</a>', content)

    def test_unversed_not_checked_by_default_in_assessment(self):
        """Verify assessment MCQs have 'unversed' unselected by default like other options."""
        # Register and login
        self.client.post("/register", data={
            "full_name": "Kavita Rao",
            "email": "kavita.rao@college.edu",
            "password": "Password123",
            "college_name": "Tech Institute",
            "branch": "AI & DS",
            "academic_year": "Second Year (SE)"
        }, follow_redirects=True)
        self.client.post("/login", data={
            "email": "kavita.rao@college.edu",
            "password": "Password123"
        }, follow_redirects=True)
        self.client.post("/profile", data={
            "technical_skills": ["Python"],
            "interests": ["Data Analysis & Visualization"],
            "preferred_career": "data_analytics"
        }, follow_redirects=True)

        resp = self.client.get("/assessment")
        self.assertEqual(resp.status_code, 200)
        content = resp.data.decode("utf-8")
        self.assertIn('value="unversed"', content)
        # Verify value="unversed" is NOT pre-checked
        self.assertNotIn('value="unversed" checked', content)

    def test_verified_sources_and_youtube_on_dashboard(self):
        """Verify dashboard displays Top 5 Verified Sources (with Free & Paid badges) and YouTube Best Resources."""
        # Register, login, profile
        self.client.post("/register", data={
            "full_name": "Sameer Joshi",
            "email": "sameer.joshi@college.edu",
            "password": "Password123",
            "college_name": "Engineering College",
            "branch": "Computer Science",
            "academic_year": "Third Year (TE)"
        }, follow_redirects=True)
        self.client.post("/login", data={
            "email": "sameer.joshi@college.edu",
            "password": "Password123"
        }, follow_redirects=True)
        self.client.post("/profile", data={
            "technical_skills": ["Python", "SQL"],
            "interests": ["Business Intelligence & Reporting"],
            "preferred_career": "data_analytics"
        }, follow_redirects=True)

        dash_resp = self.client.get("/dashboard")
        self.assertEqual(dash_resp.status_code, 200)
        content = dash_resp.data.decode("utf-8")
        self.assertIn("Top 5 Verified Sources", content)
        self.assertIn("Verified Free", content)
        self.assertIn("Verified Paid", content)
        self.assertIn("YouTube Best Resources", content)

    # ------------------------------------------------------------------------
    # 16. CSRF PROTECTION ACTIVE ON STATE-CHANGING FORMS
    # ------------------------------------------------------------------------
    def test_csrf_protection_active(self):
        """Verify POST requests without valid CSRF token are rejected with 400 when CSRF is enabled."""
        flask_app.app.config["WTF_CSRF_ENABLED"] = True
        try:
            bad_post = self.client.post("/register", data={
                "full_name": "Hacker Attempt",
                "email": "hacker@test.com",
                "password": "Password123",
                "college_name": "None",
                "branch": "None",
                "academic_year": "First Year (FE)"
            })
            self.assertEqual(bad_post.status_code, 400)
            self.assertIn("Security token mismatch (CSRF)", bad_post.data.decode("utf-8"))
        finally:
            flask_app.app.config["WTF_CSRF_ENABLED"] = False


if __name__ == "__main__":
    unittest.main()
