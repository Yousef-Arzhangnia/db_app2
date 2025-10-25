-- Migration: Add role column to users table

-- Add role column with default value 'user'
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) NOT NULL DEFAULT 'user';

-- Create index on role for faster filtering
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Update any existing users to have 'user' role (if they don't already have one)
UPDATE users SET role = 'user' WHERE role IS NULL OR role = '';

-- Add check constraint to ensure only valid roles
ALTER TABLE users ADD CONSTRAINT check_valid_role CHECK (role IN ('admin', 'user'));
