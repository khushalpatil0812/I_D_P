# 🚀 Flask HR App - Deployment Guide for Windows

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Database Setup & Access](#database-setup--access)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Application Flow](#application-flow)
7. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements:
- **Operating System**: Windows 10 or Windows 11
- **Python**: Version 3.11 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB free space
- **Internet**: Required for AI features (Google Gemini API)

### Check Your Python Version:
```powershell
python --version
```

---

## 🔧 Installation Steps

### Step 1: Install Python (if not installed)

1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   ```

### Step 2: Copy Project Files

**Option A: Using Git**
```powershell
git clone <your-repository-url>
cd flask-hr-app
```

**Option B: Manual Copy**
1. Copy the entire `flask-hr-app` folder to your Windows system
2. Place it in a convenient location (e.g., `C:\Projects\`, `D:\downloads\`)

### Step 3: Create Virtual Environment

Navigate to project directory and create virtual environment:

**PowerShell (Recommended):**
```powershell
cd D:\downloads\flask-hr-app
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Command Prompt (CMD):**
```cmd
cd D:\downloads\flask-hr-app
python -m venv .venv
.venv\Scripts\activate.bat
```

**You'll see `(.venv)` prefix in terminal when activated**

**Note:** If PowerShell shows execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

With virtual environment activated:

```bash
pip install -r requirements.txt
```

**This installs:**
- Flask (web framework)
- Flask-Login (authentication)
- Flask-SQLAlchemy (database ORM)
- google-generativeai (AI integration)
- pandas (CSV processing)
- python-dotenv (environment variables)
- werkzeug (security utilities)

---

## 🗄️ Database Setup & Access

### Understanding the Database

This application uses **SQLite** (file-based database) by default:
- **Database File**: `instance/database.db`
- **Location**: Created automatically in `flask-hr-app/instance/` folder
- **Type**: SQLite3 (no server required)
- **Size**: Small (few MB)

### Database Tables Structure:

```
📊 Database Schema:

1. USERS Table
   - id (Primary Key)
   - name, email, password_hash
   - role (hr/employee)
   - skills, experience, current_role, target_role
   - goal, created_at

2. ROLES Table
   - id (Primary Key)
   - role_name (e.g., "Full Stack Developer")
   - required_skills (comma-separated)
   - description

3. IDPS Table
   - id (Primary Key)
   - user_id (Foreign Key → users.id)
   - skill_gap, action, timeline, metric
   - status (pending/in_progress/completed)
   - created_at

4. PROGRESS Table
   - id (Primary Key)
   - idp_id (Foreign Key → idps.id)
   - completion (0-100%)
   - feedback, updated_at
```

### Initialize Database
### Initialize Database

**First Time Setup:**

```powershell
.venv\Scripts\python.exe scripts\init_db.py
```
**What this does:**
- Creates `instance/database.db` file
- Creates all tables (users, roles, idps, progress)
- Adds sample data:
  - 2 default users (HR and Employee)
  - 3 sample roles (Full Stack Developer, Data Scientist, DevOps Engineer)

### Access Database

**Method 1: Using DB Browser for SQLite (GUI - Recommended)**

### 🔍 How to View & Access Database

The database is stored as a file: `D:\downloads\flask-hr-app\instance\database.db`

#### **Method 1: DB Browser for SQLite (GUI - EASIEST & RECOMMENDED)** ⭐

**Step-by-Step Guide:**

1. **Download DB Browser**
   - Go to: https://sqlitebrowser.org/dl/
   - Download "DB Browser for SQLite" for Windows
   - Choose the `.msi` installer (standard version)

2. **Install DB Browser**
   - Run the downloaded `.msi` file
   - Follow installation wizard
   - Click "Next" → "Next" → "Install"

3. **Open Your Database**
   - Launch "DB Browser for SQLite"
   - Click "Open Database" button (or File → Open Database)
   - Navigate to: `D:\downloads\flask-hr-app\instance\database.db`
   - Click "Open"

4. **View Tables & Data**
   - You'll see 4 tabs at the top:
     - **Database Structure** - See all tables and their columns
     - **Browse Data** - View and edit table data
     - **Edit Pragmas** - Database settings
     - **Execute SQL** - Run custom SQL queries

5. **Browse Data (Most Common Use)**
   - Click "Browse Data" tab
   - Select table from dropdown:
     - `users` - See all HR and employee accounts
     - `roles` - See all job roles
     - `idps` - See all development plans
     - `progress` - See progress updates
   - You can:
     - ✅ View all records
     - ✅ Sort by columns (click column header)
     - ✅ Edit data (double-click cell)
     - ✅ Add new records (Insert Record button)
     - ✅ Delete records (Delete Record button)
     - ✅ Search/filter data

### Database Backup

**Backup (before updates):**
```powershell
copy instance\database.db instance\database_backup.db
```

**Or use File Explorer:**
1. Navigate to `D:\downloads\flask-hr-app\instance\`
2. Right-click `database.db`
3. Select "Copy"
4. Right-click in same folder → "Paste"
5. Rename to `database_backup.db`

**Restore:**
```powershell
copy instance\database_backup.db instance\database.db
```
   -- Count total users
   SELECT COUNT(*) FROM users;
### Transfer Database to Another Windows System

**Option 1: Copy Database File**
1. Copy `instance\database.db` file from `D:\downloads\flask-hr-app\instance\`
2. Transfer via USB drive, network, or email
3. Place in new system's `flask-hr-app\instance\` folder
4. All data transfers (users, IDPs, roles, progress)

**Option 2: Fresh Start**
1. Don't copy database.db
2. Run `init_db.py` on new system
3. Creates clean database with sample data only

**Screenshot Guide:**
```
┌─────────────────────────────────────────────────────────┐
│  DB Browser for SQLite                          [_][□][X]│
├─────────────────────────────────────────────────────────┤
│ File  Edit  View  Tools  Help                           │
├─────────────────────────────────────────────────────────┤
│ [Open Database] [Write Changes] [Revert Changes]        │
├─────────────────────────────────────────────────────────┤
│ Database Structure | Browse Data | Edit Pragmas | ...   │
├─────────────────────────────────────────────────────────┤
│ Table: [users ▼]                                         │
├────┬──────────┬─────────────────┬──────┬────────────────┤
│ id │   name   │      email      │ role │  current_role  │
├────┼──────────┼─────────────────┼──────┼────────────────┤
│ 1  │ HR Admin │ hr@company.com  │  hr  │ HR Manager     │
│ 2  │ John Doe │john@company.com │ emp  │ Junior Dev     │
└────┴──────────┴─────────────────┴──────┴────────────────┘
```

#### **Method 2: Using Python Script (Quick View)**

Create `check_data.py` in your project folder:
```python
import sqlite3

conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# View all users
print("\n=== USERS ===")
cursor.execute("SELECT id, name, email, role FROM users")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Role: {row[3]}")

# View all IDPs
print("\n=== IDPs ===")
cursor.execute("SELECT id, user_id, skill_gap, status FROM idps")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, User: {row[1]}, Skill: {row[2]}, Status: {row[3]}")

# View all roles
print("\n=== ROLES ===")
cursor.execute("SELECT id, role_name FROM roles")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Role: {row[1]}")

conn.close()
```

Run it:
```powershell
python check_data.py
```

#### **Method 3: SQLite Command Line (Advanced)**

1. **Download SQLite Tools**
   - Go to: https://www.sqlite.org/download.html
   - Download "sqlite-tools-win32-x86-xxxxx.zip"
   - Extract to `C:\sqlite\`
   - Add to PATH or run from that folder

2. **Open Database**
   ```powershell
   cd D:\downloads\flask-hr-app
   sqlite3 instance\database.db
   ```

3. **Useful Commands**
   ```sql
   .tables                     -- List all tables
   .schema users              -- Show table structure
   SELECT * FROM users;       -- View all users
   SELECT * FROM idps;        -- View all IDPs
   .mode column               -- Better formatting
   .headers on                -- Show column names
   .quit                      -- Exit
   ```

#### **Method 4: Visual Studio Code Extension**

1. Open VS Code
2. Install "SQLite Viewer" extension
3. Right-click `instance/database.db`
4. Select "Open Database"
5. View/edit tables in VS Code

---

### 📍 Database File Location

**Full Path:** `D:\downloads\flask-hr-app\instance\database.db`

**How to Find It:**
1. Open File Explorer
2. Navigate to `D:\downloads\flask-hr-app`
3. Open `instance` folder
4. You'll see `database.db` file

**File Details:**
- **Type:** SQLite Database File
- **Size:** Usually 20-100 KB (depends on data)
- **Created:** When you run `init_db.py` or start the app
- **Backup:** Just copy this file to backup all dataackup (before updates):**
```bash
# Windows
copy instance\database.db instance\database_backup.db

# macOS/Linux
cp instance/database.db instance/database_backup.db
```

**Restore:**
```bash
# Windows
copy instance\database_backup.db instance\database.db

# macOS/Linux
cp instance/database_backup.db instance/database.db
```

### Transfer Database to Another System

**Option 1: Copy Database File**
1. Copy `instance/database.db` file
2. Place in new system's `flask-hr-app/instance/` folder
3. All data transfers (users, IDPs, etc.)

**Option 2: Fresh Start**
1. Don't copy database.db
2. Run `init_db.py` on new system
3. Creates clean database with sample data

---

## ⚙️ Configuration

### Configure Environment Variables

Edit `.env` file in project root:

```env
# Google Gemini AI Configuration
GEMINI_API_KEY=your_api_key_here

# Database Configuration
USE_MYSQL=False

# Security (Change for production!)
SECRET_KEY=your-secret-key-change-this-in-production

# Optional: Session Configuration
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=86400
```

### Get Gemini API Key (Free):

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Paste in `.env` file: `GEMINI_API_KEY=your_key_here`

**Note:** Without API key, AI IDP generation won't work (manual IDP will still work)

---

## ▶️ Running the Application

### Start the Server

**Windows (PowerShell):**
```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run application
python app.py
```

**macOS/Linux:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run application
python app.py
```

### Expected Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://10.x.x.x:5000  (your local IP)
Press CTRL+C to quit
```

### Access Application

**Local Access:**
- Open browser: `http://127.0.0.1:5000`
- Or: `http://localhost:5000`

**Network Access (same WiFi):**
- Find your IP address
- Other devices use: `http://YOUR_IP:5000`

**Default Login Credentials:**

| Role | Email | Password |
|------|-------|----------|
| HR/Admin | hr@company.com | hr123 |
| Employee | john@company.com | emp123 |

### Stop the Server

Press `CTRL + C` in terminal

---

## 🔄 Application Flow

### Complete System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ACCESS POINT                         │
│              http://127.0.0.1:5000                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    LOGIN PAGE                                │
│  • Email & Password Authentication                           │
│  • Role-based routing (HR/Employee)                          │
└───────────┬────────────────────────┬────────────────────────┘
            │                        │
    ┌───────▼────────┐      ┌───────▼────────┐
    │   HR LOGIN     │      │ EMPLOYEE LOGIN │
    │  (role='hr')   │      │ (role='employee')│
    └───────┬────────┘      └───────┬────────┘
            │                        │
            ▼                        ▼
```

### HR User Flow:

```
┌─────────────────────────────────────────────────────────────┐
│                    HR DASHBOARD                              │
│  Statistics: Total Employees, IDPs, Pending, Completed      │
│  Quick Actions: Add Employee, Upload CSV, View Reports      │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬─────────────────┐
        │               │               │                 │
        ▼               ▼               ▼                 ▼
┌──────────────┐ ┌─────────────┐ ┌────────────┐ ┌──────────────┐
│   EMPLOYEES  │ │    ROLES    │ │  REPORTS   │ │  ADD EMPLOYEE│
│              │ │             │ │            │ │              │
│ • View List  │ │ • View All  │ │ • IDP Stats│ │ • Manual Add │
│ • View Detail│ │ • Add Role  │ │ • Analytics│ │ • Bulk CSV   │
│ • Edit Info  │ │ • Required  │ │ • Progress │ │              │
│              │ │   Skills    │ │   Tracking │ │              │
└──────┬───────┘ └─────────────┘ └────────────┘ └──────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│              EMPLOYEE DETAIL PAGE                            │
│  Profile: Name, Email, Skills, Experience, Goals            │
│  Existing IDPs: List of all development plans               │
│                                                              │
│  Action Buttons:                                             │
│  ┌──────────────────────┐  ┌─────────────────────────────┐ │
│  │ ✏️ Create Manual IDP │  │ 🤖 AI Generate IDP         │ │
│  └──────────┬───────────┘  └─────────┬───────────────────┘ │
│             │                         │                      │
└─────────────┼─────────────────────────┼──────────────────────┘
              │                         │
              ▼                         ▼
┌──────────────────────────┐  ┌─────────────────────────────┐
│   MANUAL IDP CREATION    │  │   AI IDP GENERATION         │
│                          │  │                             │
│ HR Fills Form:           │  │ 1. Select Target Role       │
│ • Skill Gap              │  │ 2. System analyzes:         │
│ • Action Plan            │  │    - Current skills         │
│ • Timeline               │  │    - Required skills        │
│ • Success Metric         │  │    - Skill gaps             │
│ • Initial Status         │  │ 3. Google Gemini AI:        │
│                          │  │    - Generates action plan  │
│ Use Cases:               │  │    - Creates timeline       │
│ • Custom goals           │  │    - Sets metrics           │
│ • Soft skills            │  │    - Suggests resources     │
│ • Leadership             │  │ 4. Saves multiple IDPs      │
│ • Specific needs         │  │                             │
└────────────┬─────────────┘  └─────────┬───────────────────┘
             │                          │
             └──────────┬───────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  IDP SAVED TO DATABASE                       │
│              (idps table in database.db)                     │
│                                                              │
│  IDP Record:                                                 │
│  • user_id: Link to employee                                │
│  • skill_gap: What needs development                        │
│  • action: Steps to take                                    │
│  • timeline: Deadline                                       │
│  • metric: Success measurement                              │
│  • status: pending/in_progress/completed                    │
└─────────────────────────────────────────────────────────────┘
```

### Employee User Flow:

```
┌─────────────────────────────────────────────────────────────┐
│                  EMPLOYEE DASHBOARD                          │
│                                                              │
│  Profile Card: Name, Email, Current/Target Role             │
│  Statistics: Total IDPs, Pending, In Progress, Completed    │
│  Development Plans Table: All assigned IDPs                  │
│  Pro Tips: Career success guidance                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    IDP DETAIL PAGE                           │
│                                                              │
│  IDP Information:                                            │
│  • Skill Gap: What to learn                                 │
│  • Action Plan: Steps to follow                             │
│  • Timeline: Completion deadline                            │
│  • Success Metric: How to measure                           │
│  • Resources: Learning materials                            │
│                                                              │
│  Progress Tracking:                                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Update Progress Form:                              │    │
│  │  • Completion % (0-100)                             │    │
│  │  • Status (Pending/In Progress/Completed)           │    │
│  │  • Feedback/Notes                                   │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              PROGRESS SAVED TO DATABASE                      │
│            (progress table in database.db)                   │
│                                                              │
│  Progress Record:                                            │
│  • idp_id: Link to IDP                                      │
│  • completion: Percentage                                   │
│  • feedback: Employee notes                                 │
│  • updated_at: Timestamp                                    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow & Database Interactions:

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYERS                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Templates - HTML/CSS/JS)               │
│  • templates/*.html - User Interface                         │
│  • static/css/style.css - Styling                           │
│  • static/js/script.js - Client-side validation             │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP Request/Response
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER (Flask Routes - Business Logic)          │
│  • routes/auth.py - Login, Register, Logout                 │
│  • routes/hr.py - HR operations (add employee, IDP, etc.)   │
│  • routes/employee.py - Employee operations (view, update)  │
└───────────────────────┬─────────────────────────────────────┘
                        │ ORM (SQLAlchemy)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA ACCESS LAYER (Models - ORM)                           │
│  • models/models.py                                          │
│    - User class (employees, HR users)                       │
│    - Role class (job roles)                                 │
│    - IDP class (development plans)                          │
│    - Progress class (tracking)                              │
└───────────────────────┬─────────────────────────────────────┘
                        │ SQL Queries
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  DATABASE LAYER (SQLite)                                    │
│  • instance/database.db                                      │
│    - Stores all application data                            │
│    - File-based, no server needed                           │
│    - Automatic backup possible                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  AI INTEGRATION LAYER (External Service)                    │
│  • ai_engine/gemini_client.py                               │
│  • ai_engine/gap_analysis.py                                │
│  • ai_engine/recommender.py                                 │
│                                                              │
│  Flow: HR Request → Analyze Skills → Call Gemini API →      │
│        Generate Recommendations → Save to Database           │
└─────────────────────────────────────────────────────────────┘
```

### Request-Response Cycle Example:

**Example: HR Creates Manual IDP**

```
1. HR clicks "Create Manual IDP" button
   ↓
2. Browser sends GET request: /hr/create-manual-idp/2
   ↓
3. Flask routes to: hr.py → create_manual_idp(user_id=2)
   ↓
4. Route queries database: User.query.get_or_404(2)
   ↓
5. Returns template: hr_create_manual_idp.html with employee data
   ↓
6. HR fills form and submits (POST request)
   ↓
7. Flask receives form data: skill_gap, action, timeline, metric
   ↓
8. Creates IDP object: IDP(user_id=2, skill_gap=..., action=...)
   ↓
9. Saves to database: db.session.add(idp), db.session.commit()
   ↓
10. Redirects to employee detail page with success message
```

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 1. "Python not found" error
**Solution:**
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed, install Python 3.11+
# Make sure to add to PATH during installation
```

#### 2. "pip not found" error
**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

#### 3. Virtual environment not activating
**Windows PowerShell (Execution Policy Error):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

#### 4. "Port 5000 already in use"
**Solution:**
```bash
# Change port in app.py (last line):
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

#### 5. Database doesn't exist
**Solution:**
```bash
# Run database initialization
python scripts/init_db.py

# Check if instance folder exists
# Check if database.db file is created
```

#### 6. "No module named 'flask'" error
**Solution:**
```bash
# Make sure virtual environment is activated
# Look for (.venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt
```

#### 7. Gemini API errors (404 model not found)
**Solution:**
- AI features may not work (deprecated package)
- Manual IDP creation still works perfectly
- Option to update to new `google-genai` package in future

#### 8. Login not working
**Solution:**
```bash
# Reset database
python scripts/init_db.py

# Default credentials:
# HR: hr@company.com / hr123
# Employee: john@company.com / emp123
```

#### 9. CSS/JavaScript not loading
**Solution:**
```bash
# Clear browser cache: CTRL + F5
# Check static files exist in static/css/ and static/js/
# Restart Flask server
```

#### 10. Database locked error
**Solution:**
```bash
# Close all database connections
# Close DB Browser if open
# Restart Flask application
```

---

## 📦 Deployment Checklist

Before deploying to a new system:

- [ ] Python 3.11+ installed
- [ ] Project files copied
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API key
- [ ] Database initialized (`python scripts/init_db.py`)
- [ ] Flask server starts without errors
- [ ] Can access login page in browser
- [ ] Can login with default credentials
- [ ] Database file exists in `instance/database.db`

---

## 🌐 Production Deployment (Advanced)

For production servers (not localhost):

### Use Production WSGI Server:

```bash
# Install Gunicorn (Linux/Mac)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

```bash
# Install Waitress (Windows)
pip install waitress

# Run with Waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

### Change Configuration:

In `app.py`, set:
```python
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'generate-strong-random-key-here'
```

### Use Environment Variables:

Don't commit `.env` file to Git. Set on server:
```bash
export GEMINI_API_KEY=your_key
export SECRET_KEY=your_secret
```

---

## 📞 Support & Help

If you encounter issues:

1. Check the `USER_MANUAL.md` for usage guide
2. Review this `DEPLOYMENT_GUIDE.md` for setup help
3. Check terminal output for error messages
4. Verify all prerequisites are installed
5. Ensure virtual environment is activated
6. Try resetting database: `python scripts/init_db.py`

---

## 📝 Quick Reference Commands

```bash
# Activate virtual environment
# Windows: .venv\Scripts\Activate.ps1
# Mac/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run application
python app.py

# Access application
# http://127.0.0.1:5000

# Stop server
# Press CTRL + C
```

---

**Last Updated**: December 2025
**Version**: 1.0
