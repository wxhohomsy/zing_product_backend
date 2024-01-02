from fastapi import Depends, HTTPException
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core import common
from zing_product_backend.models import auth
from zing_product_backend.core.security.security_utils import get_rules_from_user


async def current_tp_sample_setting_change_user(user=Depends(current_active_user)) -> auth.User:
    user_rules = get_rules_from_user(user)
    if any([common.RuleName.PRODUCT_SETTINGS_CHANGE in user_rules, common.RuleName.IMS_DEV in user_rules,
            common.RuleName.ADMIN in user_rules]):
        return user

    else:
        raise HTTPException(status_code=403, detail=common.ErrorMessages.INSUFFICIENT_PRIVILEGE)
