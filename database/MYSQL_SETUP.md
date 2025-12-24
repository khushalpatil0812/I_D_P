# MySQL Database Setup Guide

This guide explains how to set up MySQL for the IDP System.

## Quick Setup (Automated)

Run the automated setup script:

```bash
python database/mysql_setup.py
```

This will:
1. Test your MySQL connection
2. Create the `idp_system` database
3. Verify the setup

Then run the Flask app to create tables:

```bash
python app.py
```

## Manual Setup

### Step 1: Install MySQL

#### Windows
1. Download MySQL Installer from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
2. Run the installer and select "Developer Default"
3. Set root password during installation
4. Complete the installation

#### macOS
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### Step 2: Login to MySQL

```bash
mysql -u root -p
```

Enter your root password when prompted.

### Step 3: Create Database

```sql
CREATE DATABASE idp_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4: Create MySQL User (Optional but Recommended)

```sql
CREATE USER 'idp_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON idp_system.* TO 'idp_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 5: Verify Database

```sql
SHOW DATABASES;
USE idp_system;
```

### Step 6: Configure Application

Create `.env` file in project root:

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

### Step 7: Create Tables

#### Option A: Using Flask (Recommended)

```bash
python app.py
```

The app will automatically create all tables and sample data.

#### Option B: Using SQL Script

```bash
mysql -u root -p idp_system < database/schema.sql
```

## Verify Setup

### Check Tables

```bash
mysql -u root -p idp_system
```

```sql
SHOW TABLES;
```

You should see:
- users
- roles
- idps
- progress

### Check Sample Data

```sql
SELECT * FROM users;
SELECT * FROM roles;
```

## Connection String

The application uses this format:

```
mysql+pymysql://username:password@host:port/database?charset=utf8mb4
```

Example:
```
mysql+pymysql://root:password123@localhost:3306/idp_system?charset=utf8mb4
```

## Troubleshooting

### Error: Can't connect to MySQL server

**Solution:**
1. Check if MySQL is running:
   ```bash
   # Windows
   net start MySQL80
   
   # Mac
   brew services start mysql
   
   # Linux
   sudo service mysql start
   ```

2. Test connection:
   ```bash
   mysql -u root -p
   ```

### Error: Access denied for user

**Solution:**
1. Reset MySQL root password:
   ```bash
   # Stop MySQL
   sudo service mysql stop
   
   # Start in safe mode
   sudo mysqld_safe --skip-grant-tables &
   
   # Login without password
   mysql -u root
   
   # Reset password
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   ```

2. Update `.env` with correct password

### Error: Unknown database 'idp_system'

**Solution:**
Run the database creation:
```bash
python database/mysql_setup.py
```

Or manually:
```sql
CREATE DATABASE idp_system;
```

### Error: Package 'pymysql' not found

**Solution:**
```bash
pip install pymysql
```

### Error: Lost connection to MySQL server

**Solution:**
Increase MySQL timeouts in `my.cnf` or `my.ini`:
```ini
[mysqld]
wait_timeout = 28800
interactive_timeout = 28800
max_allowed_packet = 64M
```

## Performance Tips

### Indexing

The schema includes indexes on frequently queried columns:
- `users.email`
- `users.role`
- `idps.user_id`
- `idps.status`

### Connection Pooling

For production, configure SQLAlchemy pool:

```python
# In config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

### Backup

Regular backup command:
```bash
mysqldump -u root -p idp_system > backup_$(date +%Y%m%d).sql
```

Restore from backup:
```bash
mysql -u root -p idp_system < backup_20250120.sql
```

## Switching to MySQL from SQLite

If you're migrating from SQLite:

1. Export data from SQLite (optional)
2. Set `USE_MYSQL=True` in `.env`
3. Run `python app.py` to create tables
4. Import data if needed

## Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy MySQL Guide](https://docs.sqlalchemy.org/en/14/dialects/mysql.html)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
