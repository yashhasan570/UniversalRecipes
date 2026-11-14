# Test cases for authz.yml. Run with `mise run py:semgrep`.
from fastapi import HTTPException, status

from universalrecipes.routes._base.permissions import forbidden, not_found
from universalrecipes.schema.response import ErrorResponse


def flag_checks(self, user, target_user, permissions):
    # ruleid: universalrecipes-permission-flag-in-handler
    if not self.user.can_invite:
        raise forbidden()

    # ruleid: universalrecipes-permission-flag-in-handler
    if self.user.admin or user.can_manage_household:
        pass

    # ok: universalrecipes-permission-flag-in-handler
    target_user.can_organize = permissions.can_organize


def raw_errors():
    # ruleid: universalrecipes-use-forbidden-not-found
    raise HTTPException(status.HTTP_403_FORBIDDEN)

    # ruleid: universalrecipes-use-forbidden-not-found
    raise HTTPException(status_code=404)

    # ruleid: universalrecipes-use-forbidden-not-found
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=ErrorResponse.respond(message="Not found."))

    # ruleid: universalrecipes-use-forbidden-not-found
    raise HTTPException(status_code=403, detail=ErrorResponse(message="Permission Denied"))

    # ok: universalrecipes-use-forbidden-not-found
    raise HTTPException(404, "food not found")

    # ok: universalrecipes-use-forbidden-not-found
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=ErrorResponse.respond("Bad request"))

    # ok: universalrecipes-use-forbidden-not-found
    raise not_found("Not found.")
