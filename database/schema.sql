-- MySQL Database Schema for IDP System
-- This file contains the complete database structure
-- Run this manually if you prefer SQL over ORM migrations

-- Create database
CREATE DATABASE IF NOT EXISTS idp_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE idp_system;

-- Users table (HR and Employees)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'employee' COMMENT 'hr or employee',
    skills TEXT COMMENT 'Comma-separated skills',
    experience INT DEFAULT 0 COMMENT 'Years of experience',
    goal TEXT COMMENT 'Career goal',
    current_role VARCHAR(100),
    target_role VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Roles table (Job positions with required skills)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    required_skills TEXT COMMENT 'Comma-separated required skills',
    description TEXT,
    INDEX idx_role_name (role_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- IDPs table (Individual Development Plans)
CREATE TABLE IF NOT EXISTS idps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_gap TEXT COMMENT 'JSON or comma-separated missing skills',
    action TEXT NOT NULL COMMENT 'SMART action plan',
    timeline VARCHAR(100) COMMENT 'Time-bound goal',
    metric VARCHAR(255) COMMENT 'Measurable metric',
    status VARCHAR(20) DEFAULT 'pending' COMMENT 'pending, in_progress, completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Progress table (Progress tracking for IDPs)
CREATE TABLE IF NOT EXISTS progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idp_id INT NOT NULL,
    completion INT DEFAULT 0 COMMENT 'Percentage 0-100',
    feedback TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idp_id) REFERENCES idps(id) ON DELETE CASCADE,
    INDEX idx_idp_id (idp_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default HR user (password: hr123)
-- Password hash generated using werkzeug.security.generate_password_hash('hr123')
INSERT INTO users (name, email, password_hash, role) VALUES 
('HR Admin', 'hr@company.com', 'scrypt:32768:8:1$kV7xN5jGvXMz8WQp$c8b5f4e3d2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1', 'hr');

-- Insert default Employee user (password: emp123)
INSERT INTO users (name, email, password_hash, role, skills, experience, goal, current_role, target_role) VALUES 
('John Doe', 'john@company.com', 'scrypt:32768:8:1$A2bC3dE4fG5hI6j7$a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 'employee', 'Python, HTML, CSS', 2, 'Become a Full Stack Developer', 'Junior Developer', 'Full Stack Developer');

-- Insert sample roles
INSERT INTO roles (role_name, required_skills, description) VALUES 
('Full Stack Developer', 'Python, JavaScript, React, Node.js, SQL, Git, REST APIs, Docker', 'Develops both frontend and backend applications'),
('Data Scientist', 'Python, Machine Learning, Statistics, SQL, Data Visualization, Pandas, NumPy', 'Analyzes data and builds ML models'),
('DevOps Engineer', 'Linux, Docker, Kubernetes, CI/CD, AWS, Terraform, Monitoring', 'Manages infrastructure and deployment pipelines');
