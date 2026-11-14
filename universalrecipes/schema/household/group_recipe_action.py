from enum import Enum
from typing import Any

from pydantic import UUID4, ConfigDict, field_validator

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel
from universalrecipes.schema.response.pagination import PaginationBase

# ==================================================================================================================
# CRUD


class GroupRecipeActionType(Enum):
    link = "link"
    post = "post"


class GroupRecipeActionCreate(UniversalRecipesModel):
    action_type: GroupRecipeActionType
    title: str
    url: str

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("url")
    def validate_url_scheme(cls, url: str) -> str:
        """Validate that the URL uses a safe scheme to prevent XSS via javascript: URIs."""
        url_lower = url.lower().strip()
        if not (url_lower.startswith("http://") or url_lower.startswith("https://")):
            raise ValueError("URL must use http or https scheme")
        return url


class GroupRecipeActionSave(GroupRecipeActionCreate):
    group_id: UUID4
    household_id: UUID4


class GroupRecipeActionOut(GroupRecipeActionSave, UniversalRecipesOutModel):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)


class GroupRecipeActionPagination(PaginationBase):
    items: list[GroupRecipeActionOut]


# ==================================================================================================================
# Actions


class GroupRecipeActionPayload(UniversalRecipesModel):
    action: GroupRecipeActionOut
    content: Any
    recipe_scale: float
