from fastapi import Depends, HTTPException
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core import common
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.security_utils import get_rules_from_user
from zing_product_backend.core import exceptions


async def current_tp_sample_setting_change_user(user=Depends(current_active_user)) -> auth_model.User:
    user_rules = get_rules_from_user(user)
    if any([common.RuleName.TP_AUTO_SAMPLE_SETTINGS_CHANGE in user_rules, common.RuleName.IMS_DEV in user_rules,
            common.RuleName.ADMIN in user_rules]):
        return user

    else:
        raise exceptions.InsufficientPrivilegeError('User {user.name} does not have privilege'
                                                    ' to change tp sample settings')
