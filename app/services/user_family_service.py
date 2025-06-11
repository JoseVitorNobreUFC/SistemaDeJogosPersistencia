import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_family_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("user_family")

