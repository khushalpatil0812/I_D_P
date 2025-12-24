# AI-Based IDP System - User Manual & Setup Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [How to Run](#how-to-run)
5. [Application Flow](#application-flow)
6. [User Roles & Features](#user-roles--features)
7. [Step-by-Step Usage Guide](#step-by-step-usage-guide)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**AI-Based Intelligent Recommendation System for Personalized Individual Development Plans (IDPs)**

This application helps HR professionals and employees manage career development through:
- AI-powered skill gap analysis
- Personalized development recommendations using Google Gemini AI
- SMART goal tracking
- Progress monitoring
- Bulk employee management via CSV

---

## ✅ Prerequisites

- **Python 3.11+** installed
- **Internet connection** (for Google Gemini AI)
- **Web browser** (Chrome, Firefox, Edge, etc.)
- **Text editor** (VS Code, Notepad++, etc.)

---

## 🚀 Installation & Setup

### Step 1: Verify Virtual Environment
The project already has a virtual environment in `.venv` folder.

### Step 2: Verify Dependencies
All required packages are already installed:
- Flask (web framework)
- Flask-Login (authentication)
- Flask-SQLAlchemy (database)
- Google Generative AI (Gemini integration)
- Pandas (CSV processing)
- python-dotenv (environment variables)

### Step 3: Verify Configuration
The `.env` file contains all necessary configurations:
```
GEMINI_API_KEY=AIzaSyAQ9ydTgkgKs09iOU4_oQgK8AzZQGF60Rw
USE_MYSQL=False
SECRET_KEY=dev-secret-key-change-in-production-ab123cd456ef789
```

---

## ▶️ How to Run

### Method 1: Using PowerShell (Recommended)

1. **Open PowerShell**
   ```powershell
   cd D:\downloads\flask-hr-app
   ```

2. **Start the Application**
   ```powershell
   D:/downloads/flask-hr-app/.venv/Scripts/python.exe app.py
   ```

3. **Access in Browser**
   - Open your browser
   - Navigate to: `http://127.0.0.1:5000`

### Method 2: Using Command Prompt

1. **Open CMD**
   ```cmd
   cd D:\downloads\flask-hr-app
   ```

2. **Start the Application**
   ```cmd
   .venv\Scripts\python.exe app.py
   ```

### Expected Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## 🔄 Application Flow

### Complete System Flow:

```
┌─────────────────────────────────────────────────────────────┐
│                     LOGIN PAGE                              │
│  Email: hr@company.com or john@company.com                 │
│  Password: hr123 or emp123                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Authentication  │
         └─────────┬────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
         ▼                    ▼
┌────────────────┐    ┌──────────────────┐
│  HR DASHBOARD  │    │ EMPLOYEE DASHBOARD│
└────────┬───────┘    └────────┬─────────┘
         │                     │
         │                     │
         ▼                     ▼
┌──────────────────┐   ┌──────────────────┐
│  HR Features:    │   │ Employee Features│
│                  │   │                  │
│ • View All       │   │ • View My IDPs   │
│   Employees      │   │                  │
│                  │   │ • Update Progress│
│ • Add Employee   │   │                  │
│   (Manual)       │   │ • Edit Profile   │
│                  │   │                  │
│ • Upload CSV     │   │ • View Skill Gaps│
│   (Bulk Import)  │   │                  │
│                  │   │ • Track Goals    │
│ • Define Roles   │   │                  │
│   & Skills       │   └──────────────────┘
│                  │
│ • Generate IDP   │
│   ┌──────────────┴──┐
│   │ AI Processing:  │
│   │                 │
│   │ 1. Analyze      │
│   │    Current      │
│   │    Skills       │
│   │                 │
│   │ 2. Compare      │
│   │    with Target  │
│   │    Role         │
│   │                 │
│   │ 3. Identify     │
│   │    Skill Gaps   │
│   │                 │
│   │ 4. Generate     │
│   │    SMART        │
│   │    Actions via  │
│   │    Gemini AI    │
│   │                 │
│   │ 5. Create IDP   │
│   └─────────────────┘
│                  │
│ • View Reports   │
│   & Analytics    │
└──────────────────┘
```

---

## 👥 User Roles & Features

### 🔵 HR/Admin Role

**Access Level:** Full system control

**Features:**
1. **Dashboard**
   - View statistics (Total Employees, IDPs, Status)
   - Quick action buttons
   - Recent employee list

2. **Employee Management**
   - View all employees
   - Add employee manually
   - Upload CSV for bulk import
   - Edit employee details
   - View employee profiles

3. **Role Management**
   - Define job roles
   - Set required skills per role
   - Add role descriptions

4. **IDP Generation**
   - Select employee
   - Choose target role
   - AI generates personalized plan
   - Review and save recommendations

5. **Reports & Analytics**
   - View IDP statistics
   - Track completion rates
   - Monitor progress

### 🟢 Employee Role

**Access Level:** Personal data only

**Features:**
1. **Dashboard**
   - View my IDPs
   - See progress summary
   - Check pending tasks

2. **Profile Management**
   - View profile
   - Edit skills
   - Update experience
   - Set career goals

3. **IDP Tracking**
   - View assigned IDPs
   - Check skill gaps
   - See SMART actions
   - Read timelines & metrics

4. **Progress Updates**
   - Update completion percentage
   - Add feedback/notes
   - Mark tasks complete
   - Track achievements

---

## 📖 Step-by-Step Usage Guide

### For HR Users:

#### 🔹 Scenario 1: Adding a New Employee Manually

1. **Login**
   - Email: `hr@company.com`
   - Password: `hr123`

2. **Navigate to Add Employee**
   - Click "Add Employee" button
   - Or go to: `http://127.0.0.1:5000/hr/employee/add`

3. **Fill Employee Details**
   - Name: e.g., "Sarah Johnson"
   - Email: e.g., "sarah@company.com"
   - Password: Set initial password
   - Skills: "Python, JavaScript, SQL"
   - Experience: 3 years
   - Current Role: "Junior Developer"
   - Target Role: "Full Stack Developer"
   - Goal: "Master full-stack development"

4. **Submit**
   - Click "Add Employee"
   - Employee is created
   - Redirects to employee list

#### 🔹 Scenario 2: Bulk Upload via CSV

1. **Navigate to Upload CSV**
   - Click "Upload CSV" button
   - Or go to: `http://127.0.0.1:5000/hr/upload-csv`

2. **Download Template**
   - Click "Download Sample Template"
   - Opens: `sample_employees_template.csv`

3. **Prepare CSV File**
   ```csv
   name,email,skills,experience,goal,current_role,target_role,password
   Alice Smith,alice@company.com,"Python, Data Analysis",2,Become Data Scientist,Analyst,Data Scientist,password123
   Bob Williams,bob@company.com,"Java, Spring Boot",4,Lead Developer,Developer,Senior Developer,password123
   ```

4. **Upload File**
   - Click "Choose File"
   - Select your CSV
   - Click "Upload and Process"

5. **Review Results**
   - Success message shows: "X employees added, Y skipped"
   - Duplicates are automatically skipped

#### 🔹 Scenario 3: Generate IDP for Employee

**Option A: AI-Generated IDP (Automated)**

1. **Select Employee**
   - Go to "Employees" page
   - Click "View" on any employee
   - Or click "🤖 AI IDP" directly

2. **Choose Target Role**
   - Select from dropdown (e.g., "Full Stack Developer")
   - Or enter custom role

3. **AI Processing**
   - System analyzes current skills
   - Compares with required skills
   - Identifies skill gaps
   - **Gemini AI generates:**
     - Specific actions to take
     - Timeline for completion
     - Measurable metrics
     - Learning resources

4. **Review Generated IDP**
   - Example output:
     ```
     Skill Gap: React, Node.js
     Action: Complete online React course and build 2 projects
     Timeline: 3 months
     Metric: Deploy 2 full-stack applications
     Status: Pending
     ```

5. **Save IDP**
   - Click "Generate IDP"
   - IDP is saved to database
   - Employee can now view it

**Option B: Manual IDP Creation (Custom)**

1. **Access Manual IDP Form**
   - Go to "Employees" page
   - Click "✏️ Manual IDP" on employee row
   - Or from employee detail page, click "Create Manual IDP"

2. **Fill in SMART Goal Components**
   - **Skill Gap:** What skill needs development (e.g., "Kubernetes container orchestration")
   - **Action Plan:** Specific steps to take (e.g., "Complete CKA certification, deploy 3 microservices")
   - **Timeline:** Timeframe (e.g., "4 months")
   - **Success Metric:** How to measure success (e.g., "Pass CKA exam, maintain production cluster")
   - **Status:** Initial status (Not Started, In Progress, or Pending)

3. **Review SMART Framework**
   - Page includes helpful SMART goals guide
   - Examples for technical and soft skills
   - Tips for creating effective IDPs

4. **Save Custom IDP**
   - Click "Create IDP"
   - IDP is saved to database
   - View in employee's detail page

**When to Use Each Option:**
- **AI-Generated:** Quick, data-driven, based on role requirements
- **Manual:** Custom goals, soft skills, specific organizational needs

#### 🔹 Scenario 4: View Reports

1. **Navigate to Reports**
   - Click "Reports" in navigation
   - Or go to: `http://127.0.0.1:5000/hr/reports`

2. **View Analytics**
   - Total employees
   - Total IDPs created
   - Pending IDPs
   - In-progress IDPs
   - Completed IDPs

### For Employee Users:

#### 🔹 Scenario 1: View My IDPs

1. **Login**
   - Email: `john@company.com`
   - Password: `emp123`

2. **Dashboard**
   - Automatically shows all your IDPs
   - See status of each goal

3. **View Details**
   - Click on any IDP
   - See full details:
     - Skill gap identified
     - Actions to take
     - Timeline
     - Success metrics
     - Current status

#### 🔹 Scenario 2: Update Progress

1. **Open IDP**
   - Click "View Details" on any IDP

2. **Update Progress**
   - Click "Update Progress" button
   - Enter completion percentage (0-100)
   - Add feedback/notes
   - Change status:
     - Pending → In Progress
     - In Progress → Completed

3. **Submit**
   - Click "Update Progress"
   - Changes are saved
   - HR can see your progress

#### 🔹 Scenario 3: Edit Profile

1. **Navigate to Profile**
   - Click "My Profile"
   - Or go to: `http://127.0.0.1:5000/employee/profile`

2. **Edit Details**
   - Click "Edit Profile"
   - Update:
     - Skills
     - Experience
     - Career goals
     - Current role
     - Target role

3. **Save Changes**
   - Click "Save"
   - Profile is updated

---

## 🔍 Key Features Explained

### 1. AI-Powered IDP Generation

**How It Works:**
1. System retrieves employee current skills
2. Gets required skills for target role
3. Calculates skill gaps
4. Sends data to Google Gemini AI
5. AI generates SMART recommendations:
   - **S**pecific: Clear action items
   - **M**easurable: Trackable metrics
   - **A**chievable: Realistic goals
   - **R**elevant: Job-related
   - **T**ime-bound: Clear deadlines

**Example Prompt to Gemini:**
```
Employee: John Doe
Current Skills: Python, HTML, CSS
Target Role: Full Stack Developer
Required Skills: Python, JavaScript, React, Node.js, SQL, Docker

Generate SMART development actions for missing skills.
```

**AI Response:**
```json
{
  "skill_gap": "JavaScript, React, Node.js, SQL, Docker",
  "action": "Complete JavaScript fundamentals course, build 3 React projects, learn Node.js backend development",
  "timeline": "6 months",
  "metric": "Deploy 3 full-stack web applications with database integration"
}
```

### 2. CSV Bulk Import

**Supported Columns:**
- `name` (required)
- `email` (required)
- `skills` (optional)
- `experience` (optional)
- `goal` (optional)
- `current_role` (optional)
- `target_role` (optional)
- `password` (optional, default: password123)

**Validation:**
- Email uniqueness check
- Duplicate prevention
- Format validation
- Error reporting

### 3. Progress Tracking

**Metrics:**
- Completion percentage (0-100%)
- Status transitions
- Feedback notes
- Update history
- Timeline tracking

---

## 🗂️ Database Structure

### Tables:

**users**
- id, name, email, password_hash, role
- skills, experience, goal
- current_role, target_role, created_at

**roles**
- id, role_name, required_skills, description

**idps**
- id, user_id, skill_gap, action
- timeline, metric, status, created_at

**progress**
- id, idp_id, completion, feedback, updated_at

---

## ⚙️ Configuration Files

### .env (Environment Variables)
```
GEMINI_API_KEY=AIzaSyAQ9ydTgkgKs09iOU4_oQgK8AzZQGF60Rw
USE_MYSQL=False
SECRET_KEY=dev-secret-key-change-in-production-ab123cd456ef789
```

### config.py (Application Config)
- Database settings
- Session configuration
- API keys
- Security settings

---

## 🛠️ Troubleshooting

### Issue 1: Application Won't Start

**Problem:** Flask doesn't start
**Solution:**
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if found
taskkill /PID <process_id> /F

# Restart application
D:/downloads/flask-hr-app/.venv/Scripts/python.exe app.py
```

### Issue 2: Login Not Working

**Problem:** Can't login after entering credentials
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito/private window
- Verify credentials:
  - HR: `hr@company.com` / `hr123`
  - Employee: `john@company.com` / `emp123`

### Issue 3: IDP Not Generating

**Problem:** AI doesn't generate recommendations
**Solution:**
- Check internet connection
- Verify Gemini API key in `.env`
- Check API quota at: https://aistudio.google.com
- Review error in terminal output

### Issue 4: CSV Upload Fails

**Problem:** CSV file rejected
**Solution:**
- Verify CSV format matches template
- Check required columns: `name`, `email`
- Ensure UTF-8 encoding
- File size under 5MB
- No special characters in email

### Issue 5: Changes Not Reflecting

**Problem:** Updates not showing
**Solution:**
- Flask auto-reloads in debug mode
- Check terminal for reload message
- Refresh browser (F5 or Ctrl+R)
- Clear browser cache if needed

---

## 📝 Demo Accounts

### HR/Admin Account
- **Email:** hr@company.com
- **Password:** hr123
- **Capabilities:** Full access to all features

### Employee Account
- **Email:** john@company.com
- **Password:** emp123
- **Capabilities:** Personal dashboard and IDP tracking

---

## 🎓 Best Practices

1. **For HR:**
   - Define all job roles before generating IDPs
   - Keep required skills updated
   - Review AI recommendations before finalizing
   - Monitor employee progress regularly
   - Use bulk CSV for large-scale onboarding

2. **For Employees:**
   - Update progress weekly
   - Add detailed feedback
   - Keep skills current
   - Set realistic goals
   - Communicate with HR if targets seem unrealistic

3. **For System Admin:**
   - Backup database regularly
   - Monitor API usage
   - Update dependencies
   - Review security settings
   - Check error logs

---

## 📞 Support & Resources

- **Gemini AI Studio:** https://aistudio.google.com
- **Flask Documentation:** https://flask.palletsprojects.com
- **Project Location:** `D:\downloads\flask-hr-app`

---

## 🚀 Quick Start Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Gemini API key configured
- [ ] Database initialized
- [ ] Application running on port 5000
- [ ] Browser opened to http://127.0.0.1:5000
- [ ] Demo credentials tested
- [ ] Ready to use!

---

**Last Updated:** December 20, 2025
**Version:** 1.0.0
**Status:** Production Ready ✅
