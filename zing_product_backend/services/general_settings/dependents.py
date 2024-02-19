from fastapi import Depends
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.common import RuleName, ErrorMessages
from zing_product_backend.core import exceptions
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.security_utils import get_rules_from_user


async def current_setting_change_user(user=Depends(current_active_user)) -> auth_model.User:
    user_rules = get_rules_from_user(user)
    if any([RuleName.PRODUCT_SETTINGS_CHANGE in user_rules, RuleName.IMS_DEV in user_rules,
            RuleName.ADMIN in user_rules]):
        return user

    else:
        raise exceptions.InsufficientPrivilegeError(detail=f'User {user.name}'
                                                           f' does not have privilege to change product settings')
