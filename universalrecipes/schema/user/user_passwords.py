from pydantic import UUID4, ConfigDict
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from universalrecipes.schema._universalrecipes import UniversalRecipesModel

from ...db.models.users import PasswordResetModel, User
from .user import PrivateUser


class ForgotPassword(UniversalRecipesModel):
    email: str


class PasswordResetToken(UniversalRecipesModel):
    token: str


class ValidateResetToken(UniversalRecipesModel):
    token: str


class ResetPassword(ValidateResetToken):
    email: str
    password: str
    passwordConfirm: str


class PasswordResetTokenSave(UniversalRecipesModel):
    user_id: UUID4
    token: str


class PrivatePasswordResetToken(PasswordResetTokenSave):
    user: PrivateUser
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            selectinload(PasswordResetModel.user).joinedload(User.group),
            selectinload(PasswordResetModel.user).joinedload(User.household),
            selectinload(PasswordResetModel.user).joinedload(User.tokens),
        ]
