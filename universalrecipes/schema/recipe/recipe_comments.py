from datetime import datetime

from pydantic import UUID4, ConfigDict, field_validator
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from universalrecipes.db.models.recipe import RecipeComment
from universalrecipes.db.models.recipe.recipe import RecipeModel
from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel, UpdatedAtField
from universalrecipes.schema.response.pagination import PaginationBase


class RecipeCommentUser(UniversalRecipesModel):
    id: UUID4
    username: str | None = None
    admin: bool
    full_name: str | None = None
    model_config = ConfigDict(from_attributes=True)


def validate_comment_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be empty")
    return stripped


class RecipeCommentCreate(UniversalRecipesModel):
    recipe_id: UUID4
    text: str

    _validate_text = field_validator("text")(validate_comment_text)


class RecipeCommentSave(RecipeCommentCreate):
    user_id: UUID4


class RecipeCommentUpdate(UniversalRecipesModel):
    id: UUID4
    text: str

    _validate_text = field_validator("text")(validate_comment_text)


class RecipeCommentOut(UniversalRecipesOutModel):
    id: UUID4
    recipe_id: UUID4
    text: str
    created_at: datetime
    updated_at: datetime = UpdatedAtField(...)
    user_id: UUID4
    user: RecipeCommentUser
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            joinedload(RecipeComment.user),
            joinedload(RecipeComment.recipe).joinedload(RecipeModel.user),
        ]


class RecipeCommentPagination(PaginationBase):
    items: list[RecipeCommentOut]
