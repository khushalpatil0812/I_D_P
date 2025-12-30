# 🎯 AI-Based IDP System

An intelligent web application for generating personalized Individual Development Plans (IDPs) using AI-powered skill gap analysis and SMART recommendations.

## ✨ Features

- 🎯 **Role-based Authentication**: Separate dashboards for HR/Admin and Employees
- 🤖 **AI-Powered Recommendations**: Uses Google Gemini API to generate SMART development plans
- 📊 **Skill Gap Analysis**: Automatically identifies missing skills based on target roles
- 📈 **Progress Tracking**: Employees can update their progress and provide feedback
- 👥 **Employee Management**: HR can manage employees, roles, and development plans
- 📤 **CSV Bulk Import**: Upload multiple employees at once
- 📱 **Responsive Design**: Modern, clean UI that works on all devices
- 🎨 **Enhanced UI**: Beautiful gradients, cards, and interactive components

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Internet connection (for Gemini AI)

### Run Application

```powershell
# Navigate to project folder
cd D:\downloads\flask-hr-app

# Run the application
D:/downloads/flask-hr-app/.venv/Scripts/python.exe app.py
```

### Access Application
Open browser: **http://127.0.0.1:5000**

### Demo Credentials
- **HR Admin:** `hr@company.com` / `hr123`
- **Employee:** `john@company.com` / `emp123`

## 📚 Documentation

See **[USER_MANUAL.md](USER_MANUAL.md)** for complete documentation including:
- Detailed setup instructions
- Complete application flow
- Step-by-step usage guide
- Troubleshooting
- Best practices

## 🔧 Technology Stack

- **Backend**: Python 3.11+ with Flask
- **Database**: SQLite (default) or MySQL
- **AI Engine**: Google Gemini API
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login with session management
- **Frontend**: HTML5, CSS3, JavaScript, Jinja2 templates
- **CSV Processing**: Pandas

## ⚙️ Configuration

Application is pre-configured with:
- ✅ Gemini API Key: `AIzaSyAQ9ydTgkgKs09iOU4_oQgK8AzZQGF60Rw`
- ✅ Database: SQLite (`instance/database.db`)
- ✅ Session Security: Enabled
- ✅ Debug Mode: On (for development)

All settings in: `.env` file

### 2. Database Setup

#### Option A: Using MySQL (Recommended for Production)

**Step 1: Install MySQL**

- **Windows**: Download from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
- **Mac**: `brew install mysql`
- **Linux**: `sudo apt-get install mysql-server`

**Step 2: Start MySQL Service**

```bash
# Windows
net start MySQL80

# Mac
brew services start mysql

# Linux
sudo service mysql start
```

**Step 3: Configure Environment Variables**

Create a `.env` file in the project root:

```env
USE_MYSQL=True
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=idp_system
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-here
```

**Step 4: Create MySQL Database**

Run the MySQL setup script:

```bash
python database/mysql_setup.py
```

This will:
- Test your MySQL connection
- Create the `idp_system` database
- Verify the setup is complete

#### Option B: Using SQLite (Quick Start)

Set in `.env` file:

```env
USE_MYSQL=False
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-here
```

SQLite requires no additional setup and will auto-create the database file.

### 3. Get Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to your `.env` file

### 4. Run the Application

```bash
python app.py
```

The app will automatically:
- Create all database tables
- Insert sample data (2 users, 3 roles)
- Start the Flask server

### 5. Access the Application

Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

**HR Account**:
- Email: `hr@company.com`
- Password: `hr123`

**Employee Account**:
- Email: `john@company.com`
- Password: `emp123`

## Project Structure

```
idp_ai_system/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings (MySQL/SQLite)
├── requirements.txt       # Python dependencies
├── database/
│   └── mysql_setup.py    # MySQL database setup script
├── models/
│   └── models.py         # Database models
├── routes/
│   ├── auth.py          # Authentication routes
│   ├── hr.py            # HR dashboard routes
│   └── employee.py      # Employee dashboard routes
├── ai_engine/
│   ├── gemini_client.py # Gemini API integration
│   ├── gap_analysis.py  # Skill gap analysis
│   └── recommender.py   # SMART recommendation generator
├── templates/            # HTML templates
├── data/
│   └── sample_employees.csv # Sample data
└── scripts/
    └── init_db.py       # Database initialization
```

## How It Works

1. **HR adds employees** with their current skills, experience, and career goals
2. **HR defines roles** with required skills for each position
3. **HR generates IDPs** by selecting an employee and target role
4. **AI engine analyzes gaps** between current and required skills
5. **Gemini API generates** personalized SMART action plans
6. **Employees view IDPs** and track their progress
7. **HR monitors reports** on overall development status

## Database Configuration

### MySQL Connection String Format

The app uses the following format for MySQL:

```
mysql+pymysql://username:password@host:port/database?charset=utf8mb4
```

### Switching Between Databases

Edit `config.py` or set environment variables:

**For MySQL**:
```python
USE_MYSQL = True
```

**For SQLite**:
```python
USE_MYSQL = False
```

## Troubleshooting

### MySQL Connection Issues

1. **Error: Can't connect to MySQL server**
   - Check if MySQL service is running
   - Verify host and port in `.env` file
   - Test with: `mysql -u root -p`

2. **Error: Access denied for user**
   - Check MySQL username and password
   - Grant privileges: `GRANT ALL PRIVILEGES ON idp_system.* TO 'root'@'localhost';`

3. **Error: Unknown database**
   - Run `python database/mysql_setup.py` to create the database

### Gemini API Issues

1. **Error: API key not found**
   - Add your API key to `.env` file
   - Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)

2. **Error: API quota exceeded**
   - Gemini has free tier limits
   - Wait for quota reset or upgrade plan

## Database Schema

- **Users**: Employee profiles with skills and goals
- **Roles**: Job roles with required skills
- **IDPs**: Generated development plans
- **Progress**: Progress tracking entries

## Customization

- Modify `config.py` to change database or add settings
- Update `models/models.py` to extend the database schema
- Customize AI prompts in `ai_engine/recommender.py`
- Adjust styling in `templates/base.html`

## Production Deployment

For production use:

1. Change `SECRET_KEY` to a secure random value
2. Use MySQL instead of SQLite
3. Set `DEBUG=False` in Flask
4. Use a production WSGI server (gunicorn, uWSGI)
5. Enable HTTPS
6. Set up proper logging and monitoring
7. Use environment variables for sensitive data

## Requirements

### Python Packages

All required packages are listed in `requirements.txt`:
- Flask - Web framework
- Flask-SQLAlchemy - ORM
- Flask-Login - Authentication
- PyMySQL - MySQL connector
- google-generativeai - Gemini API
- python-dotenv - Environment variables

### System Requirements

- Python 3.8 or higher
- MySQL 8.0+ (optional, for production)
- 2GB RAM minimum
- Modern web browser

## License

This project is for educational purposes as part of a Mini Project for F.Y. MCA.

## Authors

- Nupur Amol Joshi (Roll No: 2501078)

Maharashtra Education Society's Institute of Management and Career Courses (IMCC), Pune

-khushal patil 
MIT WPU PUNE 
