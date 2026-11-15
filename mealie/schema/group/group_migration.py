import enum

from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class SupportedMigrations(enum.StrEnum):
    nextcloud = "nextcloud"
    chowdown = "chowdown"
    copymethat = "copymethat"
    paprika = "paprika"
    universalrecipes_alpha = "universalrecipes_alpha"
    tandoor = "tandoor"
    plantoeat = "plantoeat"
    myrecipebox = "myrecipebox"
    recipekeeper = "recipekeeper"
    cookn = "cookn"


class DataMigrationCreate(UniversalRecipesModel):
    source_type: SupportedMigrations
