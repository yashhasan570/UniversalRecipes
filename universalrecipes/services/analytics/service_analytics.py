import uuid

from universalrecipes.core.settings.static import APP_VERSION
from universalrecipes.repos.repository_factory import AllRepositories
from universalrecipes.schema.analytics.analytics import UniversalRecipesAnalytics
from universalrecipes.services._base_service import BaseService


class AnalyticsService(BaseService):
    def __init__(self, repos: AllRepositories):
        self.repos = repos
        super().__init__()

    def _databate_type(self) -> str:
        return "sqlite" if "sqlite" in self.settings.DB_URL else "postgres"  # type: ignore

    def calculate_analytics(self) -> UniversalRecipesAnalytics:
        return UniversalRecipesAnalytics(
            # Site Wide Analytics
            installation_id=uuid.uuid4(),
            version=APP_VERSION,
            database_type=self._databate_type(),
            # Optional Configs
            using_ldap=self.settings.LDAP_ENABLED,
            using_email=self.settings.SMTP_ENABLE,
            # Stats
            api_tokens=0,
            users=0,
            groups=0,
            recipes=0,
            shopping_lists=0,
            cookbooks=0,
        )
