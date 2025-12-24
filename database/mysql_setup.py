"""
MySQL Database Setup Script
This script creates the MySQL database if it doesn't exist
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_mysql_database():
    """Create MySQL database if it doesn't exist"""
    
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'idp_system')
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print(f"Connected to MySQL server at {MYSQL_HOST}:{MYSQL_PORT}")
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{MYSQL_DATABASE}' created or already exists")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"  - {db['Database']}")
        
        connection.commit()
        connection.close()
        print(f"\nMySQL setup complete! Database '{MYSQL_DATABASE}' is ready.")
        print("\nNext steps:")
        print("1. Run 'python app.py' to create tables and sample data")
        
        return True
        
    except pymysql.Error as e:
        print(f"\nError connecting to MySQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check your MySQL credentials in .env file")
        print("3. Verify MySQL host and port are correct")
        print("4. Ensure the MySQL user has database creation privileges")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection with current settings"""
    
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Successfully connected to MySQL!")
            print(f"MySQL version: {version}")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"Cannot connect to MySQL: {e}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("MySQL Database Setup for IDP System")
    print("="*60)
    print()
    
    # Test connection first
    print("Step 1: Testing MySQL connection...")
    if test_mysql_connection():
        print("\nStep 2: Creating database...")
        create_mysql_database()
    else:
        print("\nPlease fix the MySQL connection issues before proceeding.")
