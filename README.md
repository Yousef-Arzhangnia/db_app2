# BizApp Authentication Backend

Flask-based authentication backend with sign-up and sign-in functionality for business applications.

## Features

- User registration with name, last name, email, and optional company name
- Role-based access control (admin/user)
- Password hashing with bcrypt
- JWT-based authentication with role information
- PostgreSQL database
- CORS enabled for cross-origin requests
- Health check endpoint

## User Fields

- **name** (required): User's first name
- **last_name** (required): User's last name
- **email** (required): User's email address (unique)
- **password** (required): User's password (hashed)
- **company_name** (optional): User's company name
- **role** (auto-assigned): User access level ('user' or 'admin') - defaults to 'user'

## Access Levels

The system supports two access levels:
- **user**: Default role for all new signups. Standard access level.
- **admin**: Administrative access. Must be manually set in the database.

To promote a user to admin, update the database directly:
```sql
UPDATE users SET role = 'admin' WHERE email = 'user@example.com';
```

## Database Setup

Create a PostgreSQL database and run the following SQL to create the users table:

```sql
CREATE TABLE users (
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

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

Or run the `schema.sql` file provided in the repository.

## Environment Variables

Set the following environment variables:

- `SECRET_KEY`: JWT signing secret
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port (default: 5432)

Or use a single `DATABASE_URL` variable:
- `DATABASE_URL`: Full PostgreSQL connection string

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in a `.env` file or export them

3. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "ok",
  "db": true
}
```

### Sign Up
```
POST /signup
Content-Type: application/json

{
  "name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123",
  "company_name": "Acme Inc"  // optional
}
```

Success Response (201):
```json
{
  "message": "User created successfully",
  "role": "user"
}
```

Error Responses:
- 400: Missing required fields
- 409: Email already registered

### Sign In
```
POST /signin
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

Success Response (200):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "company_name": "Acme Inc",
    "role": "user"
  }
}
```

Note: The JWT token also includes the user's role in its payload for easy access control.

Error Responses:
- 400: Missing email or password
- 401: Invalid email or password

## Deployment to Render

1. Create a new PostgreSQL database on Render
2. Note the database credentials
3. Update `render.yaml` with your database credentials
4. Push to GitHub
5. Connect your repository to Render
6. Deploy!

## Security Notes

- Passwords are hashed using bcrypt
- JWT tokens expire after 2 hours
- SSL/TLS is enforced for database connections
- Email addresses are stored in lowercase
- CORS is enabled (configure as needed for production)

## License

MIT
