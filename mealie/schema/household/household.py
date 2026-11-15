from datetime import datetime
from typing import Annotated

from pydantic import UUID4, ConfigDict, StringConstraints, field_validator
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from universalrecipes.db.models.household import Household, HouseholdToRecipe
from universalrecipes.db.models.users.users import User
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesModel, UniversalRecipesOutModel
from universalrecipes.schema.household.webhook import WebhookOut
from universalrecipes.schema.response.pagination import PaginationBase

from .household_preferences import HouseholdPreferencesOut, HouseholdPreferencesUpdate


class HouseholdRecipeBase(UniversalRecipesModel):
    last_made: datetime | None = None


class HouseholdRecipeSummary(HouseholdRecipeBase, UniversalRecipesOutModel):
    recipe_id: UUID4
    model_config = ConfigDict(from_attributes=True)


class HouseholdRecipeCreate(HouseholdRecipeBase):
    household_id: UUID4
    recipe_id: UUID4


class HouseholdRecipeUpdate(HouseholdRecipeBase): ...


class HouseholdRecipeOut(HouseholdRecipeCreate, UniversalRecipesOutModel):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            joinedload(HouseholdToRecipe.household),
        ]


class HouseholdCreate(UniversalRecipesModel):
    group_id: UUID4 | None = None
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    model_config = ConfigDict(from_attributes=True)


class HouseholdSave(HouseholdCreate):
    group_id: UUID4


class HouseholdUpdate(HouseholdSave):
    id: UUID4
    slug: str


class HouseholdAdminUpdate(HouseholdSave):
    id: UUID4
    preferences: HouseholdPreferencesUpdate | None = None


class HouseholdSummary(HouseholdUpdate, UniversalRecipesOutModel):
    preferences: HouseholdPreferencesOut | None = None
    model_config = ConfigDict(from_attributes=True)


class HouseholdUserSummary(UniversalRecipesOutModel):
    id: UUID4
    full_name: str
    model_config = ConfigDict(from_attributes=True)


class HouseholdOut(HouseholdSummary, UniversalRecipesOutModel):
    group: str
    users: list[HouseholdUserSummary] | None = None
    webhooks: list[WebhookOut] = []
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            joinedload(Household.group),
            joinedload(Household.webhooks),
            joinedload(Household.preferences),
            selectinload(Household.users).joinedload(User.group),
            selectinload(Household.users).joinedload(User.tokens),
        ]

    @field_validator("group", mode="before")
    def convert_group_to_name(cls, v):
        if not v or isinstance(v, str):
            return v

        try:
            return v.name
        except AttributeError:
            return v


class HouseholdPagination(PaginationBase):
    items: list[HouseholdOut]
