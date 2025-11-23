from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime


class FileCategoryCreateSchema(BaseModel):
    """File category creation schema"""
    code: str = Field(..., min_length=1, max_length=50, description="Unique code for the category (e.g., '1099', 'CHECKS')")
    name: Optional[str] = Field(None, max_length=100, description="Display name for the category")
    description: Optional[str] = None
    status: Literal['active', 'inactive'] = 'active'


class FileCategoryUpdateSchema(BaseModel):
    """File category update schema"""
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    status: Optional[Literal['active', 'inactive']] = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        """Ensure at least one field is provided"""
        if not any([
            self.code, self.name, self.description, self.status
        ]):
            raise ValueError('At least one field must be provided for update')
        return self


class FileCategoryQuerySchema(BaseModel):
    """File category query parameters schema"""
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None
    status: Optional[Literal['active', 'inactive']] = None
    sort: str = 'code'
    order: Literal['asc', 'desc'] = 'asc'
    model_config = {
        'extra': 'forbid'
    }


class FileCategoryResponseSchema(BaseModel):
    """File category response schema"""
    id: str
    code: str
    name: Optional[str]
    description: Optional[str]
    status: str
    created_date: Optional[datetime]
    last_updated: Optional[datetime]
    user_count: int
    model_config = {
        'from_attributes': True
    }

