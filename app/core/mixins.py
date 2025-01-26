# backend/app/core/mixins.py
from datetime import datetime
from pydantic import Field


class TimestampMixin:
    """
    Mixin class to add `created_at` and `updated_at` fields to models.
    """
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)
