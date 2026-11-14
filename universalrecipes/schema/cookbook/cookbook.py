from typing import Annotated

import sqlalchemy as sa
from pydantic import UUID4, ConfigDict, Field, ValidationInfo, field_validator
from slugify import slugify
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from universalrecipes.core.root_logger import get_logger
from universalrecipes.db.models.household.cookbook import CookBook
from universalrecipes.db.models.recipe import RecipeModel
from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel
from universalrecipes.schema.response.pagination import PaginationBase
from universalrecipes.services.query_filter.builder import QueryFilterBuilder, QueryFilterJSON

logger = get_logger()


class CookbookHousehold(UniversalRecipesModel):
    id: UUID4
    name: str
    model_config = ConfigDict(from_attributes=True)


class CookBookCreate(UniversalRecipesModel):
    name: str
    description: str = ""
    slug: Annotated[str | None, Field(validate_default=True)] = None
    position: int = 1
    public: Annotated[bool, Field(validate_default=True)] = False
    query_filter_string: str = ""

    @field_validator("public", mode="before")
    def validate_public(cls, public: bool | None) -> bool:
        return False if public is None else public

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        name = name.strip()

        # we calculate the slug later leveraging the database,
        # but we still need to validate the name can be slugified
        possible_slug = slugify(name)
        if not (name and possible_slug):
            raise ValueError("Name cannot be empty")

        return name

    @field_validator("query_filter_string")
    def validate_query_filter_string(cls, value: str) -> str:
        # The query filter builder does additional validations while building the
        # database query, so we make sure constructing the query is successful
        builder = QueryFilterBuilder(value)

        try:
            builder.filter_query(sa.select(RecipeModel), RecipeModel)
        except Exception as e:
            raise ValueError("Invalid query filter string") from e

        return value


class CookBookSave(CookBookCreate):
    group_id: UUID4
    household_id: UUID4


class CookBookUpdate(CookBookSave):
    id: UUID4


class CookBookOut(CookBookUpdate, UniversalRecipesOutModel):
    query_filter: Annotated[QueryFilterJSON, Field(validate_default=True)] = None  # type: ignore
    household: CookbookHousehold | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("query_filter_string")
    def validate_query_filter_string(cls, value: str) -> str:
        # Skip validation since we are not updating the query filter string
        return value

    @field_validator("query_filter", mode="before")
    def validate_query_filter(cls, _, info: ValidationInfo) -> QueryFilterJSON:
        try:
            query_filter_string: str = info.data.get("query_filter_string") or ""
            builder = QueryFilterBuilder(query_filter_string)
            return builder.as_json_model()
        except Exception:
            logger.exception(f"Invalid query filter string: {query_filter_string}")
            return QueryFilterJSON()

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [joinedload(CookBook.household)]


class CookBookPagination(PaginationBase):
    items: list[CookBookOut]
