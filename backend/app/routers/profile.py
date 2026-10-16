from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..core.clock import valid_timezone
from ..core.security import current_user
from ..db.connection import get_db
from ..db.models import User
from ..services.plans import get_plan

router = APIRouter(prefix="/api", tags=["profile"])


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=40)
    timezone: str | None = None
    daily_goal: int | None = Field(default=None, ge=1, le=20)
    plan: Literal["topic", "random", "sprint"] | None = None


def user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "display_name": user.display_name or user.name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "timezone": user.timezone,
        "daily_goal": user.daily_goal,
        "plan": get_plan(user.plan).id,
    }


@router.get("/me")
def get_me(user: User = Depends(current_user)):
    return user_payload(user)


@router.patch("/me")
def update_me(body: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if body.display_name is not None:
        name = body.display_name.strip()
        if not name:
            raise HTTPException(422, "Name required")
        user.display_name = name
    if body.timezone is not None:
        if not valid_timezone(body.timezone):
            raise HTTPException(422, "Unknown timezone")
        user.timezone = body.timezone
    if body.daily_goal is not None:
        user.daily_goal = body.daily_goal
    if body.plan is not None:
        user.plan = body.plan
    db.commit()
    return user_payload(user)
