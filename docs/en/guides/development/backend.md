# Backend Development Guide

This guide provides comprehensive information about backend development in OperatorNext.

## Development Environment

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- VS Code (recommended)

### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "charliermarsh.ruff",
    "tamasfe.even-better-toml"
  ]
}
```

### Environment Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Set up pre-commit hooks:
```bash
pre-commit install
```

4. Set up environment variables:
```bash
cp .env.example .env
```

## Project Structure

```
backend/
├── api/                 # API endpoints
│   ├── browser.py      # Browser automation endpoints
│   ├── auth.py         # Authentication endpoints
│   └── deps.py         # Dependencies
├── core/               # Core business logic
│   ├── config.py       # Configuration
│   ├── security.py     # Security utilities
│   └── constants.py    # Constants
├── models/             # Data models
│   ├── user.py         # User model
│   └── task.py         # Task model
├── schemas/            # API schemas
│   ├── user.py         # User schemas
│   └── task.py         # Task schemas
├── services/           # Business services
│   ├── browser/        # Browser automation
│   └── ai/             # AI services
└── utils/              # Utilities
    ├── logger.py       # Logging
    └── helpers.py      # Helper functions
```

## Coding Standards

### Python Style

```python
from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    """User model with basic information."""
    
    id: str
    name: str
    email: str
    role: str = "user"
    is_active: bool = True

    class Config:
        """Pydantic model configuration."""
        
        from_attributes = True
```

### FastAPI Routes

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> List[UserResponse]:
    """Get list of users with pagination."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    users = await get_users_from_db(skip=skip, limit=limit)
    return users
```

### Database Operations

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> Optional[User]:
    """Get user by email from database."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()
```

## API Design

### Request Validation

```python
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    """User creation schema with validation."""
    
    email: EmailStr
    password: constr(min_length=8)
    name: constr(min_length=1, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "name": "John Doe"
            }
        }
```

### Response Models

```python
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    """User response schema."""
    
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

## Authentication

### JWT Implementation

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
```

### OAuth Integration

```python
from fastapi_oauth.clients import GitHubOAuth2, GoogleOAuth2

github_oauth = GitHubOAuth2(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET
)

google_oauth = GoogleOAuth2(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET
)
```

## Database

### Models

```python
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func

class User(Base):
    """User database model."""
    
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
```

### Migrations

```python
"""Add user table

Revision ID: abc123def456
"""

from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        unique=True
    )

def downgrade() -> None:
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

## Testing

### Unit Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
    db_session: AsyncSession
):
    """Test user creation endpoint."""
    response = await async_client.post(
        "/api/users",
        json={
            "email": "test@example.com",
            "password": "strongpass123",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_user_workflow(
    async_client: AsyncClient,
    test_user: User
):
    """Test complete user workflow."""
    # Login
    response = await async_client.post(
        "/api/auth/login",
        data={
            "username": test_user.email,
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Get user profile
    response = await async_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

## Error Handling

### Custom Exceptions

```python
from fastapi import HTTPException
from typing import Any, Optional, Dict

class APIError(HTTPException):
    """Base API error class."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )
```

### Error Handlers

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )
```

## Logging

### Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'app.log',
                maxBytes=10000000,
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

### Usage

```python
logger = logging.getLogger(__name__)

async def create_user(user: UserCreate) -> User:
    """Create new user with logging."""
    logger.info(f"Creating new user: {user.email}")
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        await db.commit()
        logger.info(f"User created successfully: {user.email}")
        return db_user
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}")
        raise
```

## Performance

### Caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@router.get("/users/{user_id}", response_model=UserResponse)
@cache(expire=300)  # Cache for 5 minutes
async def get_user(user_id: str) -> UserResponse:
    """Get user by ID with caching."""
    return await get_user_from_db(user_id)
```

### Database Optimization

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=0
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Testing Guide](../testing/index.md)
- [API Documentation](../api/reference.md) 