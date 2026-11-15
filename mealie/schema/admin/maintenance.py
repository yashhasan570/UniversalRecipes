from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel


class MaintenanceSummary(UniversalRecipesOutModel):
    data_dir_size: str
    cleanable_images: int
    cleanable_dirs: int


class MaintenanceStorageDetails(UniversalRecipesModel):
    temp_dir_size: str
    backups_dir_size: str
    groups_dir_size: str
    recipes_dir_size: str
    user_dir_size: str
