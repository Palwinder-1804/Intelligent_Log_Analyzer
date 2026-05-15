from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    TokenResponse
)

from app.models.user_model import user_collection

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserRegister):

    existing_user = await user_collection.find_one(
        {
            "$or": [
                {"email": user.email},
                {"username": user.username}
            ]
        }
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "role": "viewer"
    }

    result = await user_collection.insert_one(user_data)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login_user(user: UserLogin):

    db_user = await user_collection.find_one(
        {"email": user.email}
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user["_id"]),
            "email": db_user["email"],
            "role": db_user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }