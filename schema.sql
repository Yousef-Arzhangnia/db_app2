-- BizApp Authentication Database Schema

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_valid_role CHECK (role IN ('admin', 'user'))
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Optional: Create index on company_name for filtering
CREATE INDEX IF NOT EXISTS idx_users_company ON users(company_name);

-- Create index on role for faster filtering by access level
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
