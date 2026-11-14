from functools import cached_property

from fastapi import APIRouter, HTTPException

from universalrecipes.routes._base.base_controllers import BaseUserController
from universalrecipes.routes._base.controller import controller
from universalrecipes.routes._base.permissions import Perm, require
from universalrecipes.schema.group.group_seeder import SeederConfig
from universalrecipes.schema.response.responses import ErrorResponse, SuccessResponse
from universalrecipes.services.seeder.seeder_service import SeederService

router = APIRouter(prefix="/groups/seeders", tags=["Groups: Seeders"])


@controller(router)
class DataSeederController(BaseUserController):
    @cached_property
    def service(self) -> SeederService:
        return SeederService(self.repos)

    def _wrap(self, func):
        try:
            func()
        except Exception as e:
            raise HTTPException(status_code=500, detail=ErrorResponse.respond("Seeding Failed")) from e

        return SuccessResponse.respond("Seeding Successful")

    @router.post("/foods", response_model=SuccessResponse, dependencies=[require(Perm.GROUP_ORGANIZE)])
    def seed_foods(self, data: SeederConfig) -> dict:
        return self._wrap(lambda: self.service.seed_foods(data.locale))

    @router.post("/units", response_model=SuccessResponse, dependencies=[require(Perm.GROUP_ORGANIZE)])
    def seed_units(self, data: SeederConfig) -> dict:
        return self._wrap(lambda: self.service.seed_units(data.locale))
