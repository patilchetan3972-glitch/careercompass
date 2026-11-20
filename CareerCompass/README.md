# CareerCompass 🧭
### An Intelligent Student Career & Skill Gap Recommendation System
*A College SDG Project developed by Second-Year Artificial Intelligence & Data Science Engineering Students.*

---

## 1. Project Overview

**CareerCompass** is a secure, responsive, and beginner-friendly web application designed to guide undergraduate engineering students through career confusion and unstructured self-study.

Many students struggle to decide between competing technology specializations, lack awareness of real prerequisite skills, and follow scattered online tutorials without understanding where their genuine conceptual aptitudes lie. CareerCompass addresses this through:

1. **A Guided 25-MCQ Diagnostic Assessment:** Sampled from a technically rigorous 100-question pool across 5 key tech domains (15 foundational and 10 practical problem-solving questions).
2. **Transparent, Rule-Based Recommendations:** Clear proficiency breakdown (Beginner, Developing, Strong Foundation), highest-aptitude domain identification, and interest-aligned tie-breaking.
3. **Actionable Skill Gap Analysis:** Categorizing skills into *Already Have*, *Need to Improve*, and *Should Learn Next*.
4. **Personalized 3-Stage Learning Roadmaps:** Providing genuine, reputable free learning resources (Kaggle Learn, freeCodeCamp, SQLBolt, W3Schools, Python documentation) with persistent task completion tracking.
5. **Backend-Enforced 7-Day Retake Cooldown:** Encouraging deliberate practice before re-assessment.

### UN Sustainable Development Goals (SDG) Alignment:
- **SDG 4: Quality Education (Target 4.4):** Substantially increase the number of youth with relevant technical and vocational skills for employment and decent jobs.
- **SDG 8: Decent Work and Economic Growth (Target 8.6):** Substantially reduce the proportion of youth not in employment, education, or training by bridging the industry-academia skill gap.

---

## 2. Technology Stack

- **Backend:** Python 3.10+ / Flask 3.1
- **Database:** SQLite 3 with parameterized queries and foreign key cascades
- **Authentication & Security:** Werkzeug password hashing (scrypt / PBKDF2), Flask-WTF CSRF protection, Flask-Limiter rate-limiting
- **Frontend:** Semantic HTML5, Modern CSS3 (Flexbox & CSS Grid) with a Nature & Growth theme, minimal Vanilla JavaScript
- **WSGI / Production Servers:** Gunicorn (Linux/Cloud) / Waitress (Windows)

---

## 3. Project File Structure

```text
CareerCompass/
├── app.py                  # Main Flask application, routes, auth, security & DB operations
├── career_data.py          # 5 career domains, 100 original MCQs, roadmaps & scoring logic
├── requirements.txt        # Pinned project dependencies
├── .gitignore              # Version control exclusion rules (secrets, venv, DB, logs)
├── .env.example            # Safe template for required environment variables
├── README.md               # Complete setup, testing, security, and deployment documentation
├── templates/
│   ├── index.html          # Unified student template: Landing, SDGs, Auth, Profile & Dashboard
│   └── results.html        # Diagnostic results, 5-domain scores, skill gaps & roadmaps
├── static/
│   └── style.css           # Nature & Growth design system, responsive media queries
└── tests/
    └── test_app.py         # Automated test suite (12 comprehensive test cases)
```

---

## 4. Local Setup & Running Instructions (Windows & VS Code)

### Prerequisites:
- Python 3.10 or higher installed on your system.
- Visual Studio Code (or any modern code editor).

### Step 1: Open Project in VS Code
Open VS Code, navigate to `File > Open Folder...`, and select the `CareerCompass` directory.

### Step 2: Open Terminal & Create a Virtual Environment
Press ``Ctrl + ` `` to open the VS Code integrated terminal and run:

```powershell
# Create a dedicated virtual environment
python -m venv .venv

# Activate the virtual environment on Windows
.venv\Scripts\Activate.ps1
```
*(If PowerShell execution policies restrict script activation, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then re-run the activate command).*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the safe example environment file:
```powershell
copy .env.example .env
```
Generate a secure random secret key by running:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Paste that generated string into `.env` as the value for `SECRET_KEY`.

### Step 5: Start the Local Development Server
```powershell
python app.py
```
Open your web browser and navigate to:
**http://127.0.0.1:5000**

---

## 5. Automated Testing

The project includes an automated test suite verifying 12 key functional and security specifications:

- Application boot and homepage rendering
- 6-field student registration and email normalization
- Prevention of duplicate account registration
- Verification that passwords are encrypted with secure hashes (never stored in plain text)
- Login authentication with valid and invalid credentials
- Session invalidation upon logout
- Student data isolation (preventing Student A from inspecting Student B's results)
- Assessment sampling of exactly 25 questions (5 per domain: 3 foundational, 2 practical)
- Domain percentage calculation and recommendation tie-breaking
- Strict backend enforcement of the 7-day retake cooldown
- Interactive roadmap task persistence across sessions
- CSRF protection rejection on state-changing requests without valid tokens

To execute the test suite:
```powershell
python -m unittest discover -s tests -v
```

---

## 6. Comprehensive Security Architecture

| Security Category | Implementation Detail |
| :--- | :--- |
| **Secret Management** | `SECRET_KEY` is loaded strictly from environment variables (`os.environ`). Never hardcoded or committed to git. |
| **Password Security** | Passwords hashed using Werkzeug's `scrypt` / `PBKDF2` algorithm with cryptographic salts. Plaintext passwords are never stored, logged, or returned. |
| **Session Fixation Defense** | User sessions are explicitly cleared with `session.clear()` upon authentication and regenerated. |
| **CSRF Defense** | Every state-changing HTML form includes `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` validated by `Flask-WTF`. Unauthorized requests receive HTTP 400. |
| **Rate Limiting** | Authentication endpoints are protected by `Flask-Limiter` (`5 per minute`) to defend against brute-force attacks. |
| **Cookie Hardening** | `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, and `SESSION_COOKIE_SECURE = True` in production. |
| **Defense-in-Depth Headers** | All responses include `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy`. |
| **SQL Injection Prevention** | All database operations strictly employ parameterized SQLite queries (`?` placeholders). User input is never concatenated into SQL strings. |
| **Data Privacy** | Only necessary academic fields are requested. No third-party tracking or external telemetry scripts are included. |

---

## 7. Cloud Deployment & Persistent Storage Guide

### Critical Deployment Note: SQLite on Ephemeral Hosting
Platforms such as Render (Free tier), Heroku, or basic containers employ **ephemeral filesystems**. Any database file created on the local filesystem will reset whenever the application container sleeps, restarts, or deploys a new build.

**Solution for Production:**
1. **Persistent Disks:** Attach a Persistent Disk volume in your cloud dashboard (e.g. Render Disk or Railway Volume mounted at `/var/data`) and configure:
   ```env
   DATABASE_PATH=/var/data/careercompass.db
   ```
2. **Relational Cloud Databases:** For high-volume multi-node deployments, point backend connection strings to a managed PostgreSQL instance using standard SQLAlchemy or psycopg drivers.

### Deploying to Render.com:
1. Create a **Web Service** linked to your Git repository.
2. Select **Python 3** environment.
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`
4. In the **Environment Variables** tab, add:
   - `SECRET_KEY`: `(Paste a secure 64-character random hex string)`
   - `FLASK_ENV`: `production`
   - `DATABASE_PATH`: `/var/data/careercompass.db` (if using a persistent disk)

### Deploying with Docker:
A standard production Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:5000"]
```

---

## 8. Known Limitations & Future Roadmap

1. **Rule-Based Diagnostic Scope:** The recommendation algorithm is transparently rule-based and deterministic. It evaluates foundational and logical aptitude without claiming to be an uninterpretable machine learning model.
2. **Single Server Concurrency:** SQLite is well-suited for low-to-medium concurrent college student traffic with WAL mode enabled. For enterprise-scale concurrent deployments exceeding thousands of simultaneous writes, migrating the DB connector to PostgreSQL is recommended.
3. **Password Recovery:** To eliminate phishing vulnerabilities and unauthenticated reset attacks, automated password recovery via email is omitted in this MVP. Administrators can reset passwords via the backend CLI.

---

## 9. Academic Project Credits
- **Project Name:** CareerCompass – An Intelligent Student Career & Skill Gap Recommendation System
- **Academic Department:** Artificial Intelligence and Data Science Engineering
- **Academic Year:** Second Year (SE) Project Initiative
- **Project Focus:** UN Sustainable Development Goals (SDG 4 & SDG 8)

