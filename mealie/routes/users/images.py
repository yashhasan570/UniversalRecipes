import shutil
from uuid import uuid4

from fastapi import File, HTTPException, UploadFile, status
from pydantic import UUID4

from universalrecipes.core.dependencies import get_temporary_path
from universalrecipes.pkgs import cache, img
from universalrecipes.routes._base import BaseUserController, controller
from universalrecipes.routes._base.routers import UserAPIRouter
from universalrecipes.routes.users._helpers import assert_user_change_allowed
from universalrecipes.schema.user import PrivateUser

router = UserAPIRouter(prefix="", tags=["Users: Images"])


@controller(router)
class UserImageController(BaseUserController):
    @router.post("/{id}/image")
    def update_user_image(
        self,
        id: UUID4,
        profile: UploadFile = File(...),
    ):
        """Updates a User Image"""
        with get_temporary_path() as temp_path:
            assert_user_change_allowed(id, self.user, self.user)

            # use a generated uuid and ignore the filename so we don't
            # need to worry about sanitizing user inputs.
            temp_img = temp_path.joinpath(str(uuid4()))

            with temp_img.open("wb") as buffer:
                shutil.copyfileobj(profile.file, buffer)

            image = img.PillowMinifier.to_webp(temp_img)
            dest = PrivateUser.get_directory(id) / "profile.webp"

            shutil.copyfile(image, dest)

        self.repos.users.patch(id, {"cache_key": cache.new_key()})

        if not dest.is_file():
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
