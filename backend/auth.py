import os
from typing import Optional
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel

# Environment variables - FIXED for Better Auth compatibility
JWT_SECRET = os.getenv(
    "BETTER_AUTH_SECRET",  # Changed from JWT_SECRET
    os.getenv("JWT_SECRET", "your-super-secret-key-at-least-32-characters-long")
)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()


class TokenPayload(BaseModel):
    """JWT token payload structure - Better Auth compatible"""
    userId: Optional[str] = None  # Better Auth uses 'userId'
    sub: Optional[str] = None     # Standard JWT field (fallback)
    email: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """
    Verify JWT token and extract payload.
    Compatible with both Better Auth and standard JWT formats.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        TokenPayload with user_id and other claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        
        # Support both Better Auth (userId) and standard JWT (sub) formats
        user_id = payload.get("userId") or payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user ID (userId or sub claim)"
            )

        return TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user_id(
    payload: TokenPayload = Depends(verify_token)
) -> str:
    """
    Dependency to get current user ID from JWT.
    Works with both Better Auth (userId) and standard JWT (sub) formats.

    Args:
        payload: Verified token payload

    Returns:
        user_id string
    """
    # Better Auth uses 'userId', standard JWT uses 'sub'
    user_id = payload.userId or payload.sub
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token: no user ID found"
        )
    
    return user_id


async def verify_user_access(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
) -> str:
    """
    Verify that the user is accessing their own data.

    Args:
        user_id: User ID from URL path
        current_user_id: User ID from JWT token

    Returns:
        user_id if access is allowed

    Raises:
        HTTPException: If user is trying to access another user's data
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot access other user's data"
        )
    return user_id


# Optional: Alternative verification using Authorization header directly
async def verify_token_from_header(
    authorization: str = Header(None)
) -> TokenPayload:
    """
    Alternative token verification that accepts Authorization header directly.
    Useful if HTTPBearer is causing issues.

    Args:
        authorization: Authorization header value (Bearer <token>)

    Returns:
        TokenPayload with user_id and other claims

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header"
        )

    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format. Expected: Bearer <token>"
        )

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        
        user_id = payload.get("userId") or payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user ID"
            )

        return TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Please login again."
        )
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )