"""
Local database read/write script
Run this in VS Code to interact with your PostgreSQL database
"""

import psycopg2
import os
from datetime import datetime

# Database connection settings
# Option 1: Use DATABASE_URL directly
DATABASE_URL = os.environ.get('DATABASE_URL')

# Option 2: Or set individual variables here
if not DATABASE_URL:
    DB_NAME = "opdo_auth_db_v2"
    DB_USER = "postgres"
    DB_PASSWORD = "your_password_here"  # Replace with your actual password
    DB_HOST = "your_host_here"  # Replace with your actual host
    DB_PORT = "5432"
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"


def get_connection():
    """Get a database connection"""
    return psycopg2.connect(DATABASE_URL)


def read_all_users():
    """Read all users from database"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, last_name, email, company_name, role, created_at FROM users ORDER BY created_at DESC")
            users = cur.fetchall()

            print(f"\n{'='*80}")
            print(f"TOTAL USERS: {len(users)}")
            print(f"{'='*80}\n")

            for user in users:
                user_id, name, last_name, email, company_name, role, created_at = user
                print(f"ID: {user_id}")
                print(f"Name: {name} {last_name}")
                print(f"Email: {email}")
                print(f"Company: {company_name}")
                print(f"Role: {role}")
                print(f"Created: {created_at}")
                print("-" * 80)

            return users
    finally:
        conn.close()


def read_user_by_email(email):
    """Read a specific user by email"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, last_name, email, company_name, role FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()

            if user:
                print(f"\nUser found:")
                print(f"ID: {user[0]}")
                print(f"Name: {user[1]} {user[2]}")
                print(f"Email: {user[3]}")
                print(f"Company: {user[4]}")
                print(f"Role: {user[5]}")
            else:
                print(f"\nNo user found with email: {email}")

            return user
    finally:
        conn.close()


def write_test_user():
    """Write a test user to database"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Create a test user
            test_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"

            cur.execute(
                """
                INSERT INTO users (name, last_name, email, password, company_name, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                ("Test", "User", test_email, "dummy_hash", "Test Company", "user")
            )

            user_id = cur.fetchone()[0]
            conn.commit()

            print(f"\n✓ Test user created successfully!")
            print(f"ID: {user_id}")
            print(f"Email: {test_email}")

            return user_id
    finally:
        conn.close()


def update_user_role(email, new_role):
    """Update user role"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET role = %s WHERE email = %s RETURNING id",
                (new_role, email)
            )
            result = cur.fetchone()
            conn.commit()

            if result:
                print(f"\n✓ User role updated to '{new_role}' for {email}")
                return True
            else:
                print(f"\n✗ No user found with email: {email}")
                return False
    finally:
        conn.close()


def delete_user(email):
    """Delete a user by email"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE email = %s RETURNING id",
                (email,)
            )
            result = cur.fetchone()
            conn.commit()

            if result:
                print(f"\n✓ User deleted: {email}")
                return True
            else:
                print(f"\n✗ No user found with email: {email}")
                return False
    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 80)
    print("DATABASE LOCAL TEST SCRIPT")
    print("=" * 80)

    # Example usage - uncomment the functions you want to run:

    # 1. Read all users
    read_all_users()

    # 2. Read specific user
    # read_user_by_email("user@example.com")

    # 3. Write a test user
    # write_test_user()

    # 4. Update user role
    # update_user_role("test@example.com", "admin")

    # 5. Delete a user
    # delete_user("test@example.com")

    print("\nDone!")
