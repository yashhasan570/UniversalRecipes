import shutil

from fastapi import File, Form
from fastapi.datastructures import UploadFile

from universalrecipes.core.dependencies import get_temporary_zip_path
from universalrecipes.routes._base import BaseUserController, controller
from universalrecipes.routes._base.routers import UserAPIRouter
from universalrecipes.schema.group.group_migration import SupportedMigrations
from universalrecipes.schema.reports.reports import ReportSummary
from universalrecipes.services.migrations import (
    BaseMigrator,
    ChowdownMigrator,
    CooknMigrator,
    CopyMeThatMigrator,
    UniversalRecipesAlphaMigrator,
    MyRecipeBoxMigrator,
    NextcloudMigrator,
    PaprikaMigrator,
    PlanToEatMigrator,
    RecipeKeeperMigrator,
    TandoorMigrator,
)

router = UserAPIRouter(prefix="/groups/migrations", tags=["Groups: Migrations"])


@controller(router)
class GroupMigrationController(BaseUserController):
    @router.post("", response_model=ReportSummary)
    def start_data_migration(
        self,
        add_migration_tag: bool = Form(False),
        migration_type: SupportedMigrations = Form(...),
        archive: UploadFile = File(...),
    ):
        with get_temporary_zip_path() as temp_path:
            # Save archive to temp_path
            with temp_path.open("wb") as buffer:
                shutil.copyfileobj(archive.file, buffer)

            args = {
                "archive": temp_path,
                "db": self.repos,
                "session": self.session,
                "user_id": self.user.id,
                "household_id": self.household_id,
                "group_id": self.group_id,
                "add_migration_tag": add_migration_tag,
                "translator": self.translator,
            }

            table: dict[SupportedMigrations, type[BaseMigrator]] = {
                SupportedMigrations.chowdown: ChowdownMigrator,
                SupportedMigrations.copymethat: CopyMeThatMigrator,
                SupportedMigrations.universalrecipes_alpha: UniversalRecipesAlphaMigrator,
                SupportedMigrations.nextcloud: NextcloudMigrator,
                SupportedMigrations.paprika: PaprikaMigrator,
                SupportedMigrations.tandoor: TandoorMigrator,
                SupportedMigrations.plantoeat: PlanToEatMigrator,
                SupportedMigrations.myrecipebox: MyRecipeBoxMigrator,
                SupportedMigrations.recipekeeper: RecipeKeeperMigrator,
                SupportedMigrations.cookn: CooknMigrator,
            }

            constructor = table.get(migration_type, None)

            if constructor is None:
                raise ValueError(f"Unsupported migration type: {migration_type}")

            migrator = constructor(**args)

            migration_result = migrator.migrate(f"{migration_type.value.title()} Migration")
        return migration_result
