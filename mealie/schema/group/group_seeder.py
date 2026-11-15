from pydantic import field_validator

from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.validators import validate_locale


class SeederConfig(UniversalRecipesModel):
    locale: str

    @field_validator("locale")
    def valid_locale(cls, v):
        if not validate_locale(v):
            raise ValueError("invalid locale")
        return v
