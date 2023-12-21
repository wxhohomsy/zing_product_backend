from fastapi import Depends, HTTPException
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.common import RuleName, ErrorMessages
from zing_product_backend.models import auth
from zing_product_backend.core.security.security_utils import get_rules_from_user


async def current_containment_rule_change_user(user=Depends(current_active_user)) -> auth.User:
    user_rules = get_rules_from_user(user)
    if any([RuleName.PRODUCT_SETTINGS_CHANGE in user_rules, RuleName.IMS_DEV in user_rules,
            RuleName.ADMIN in user_rules]):
        return user

    else:
        raise HTTPException(status_code=403, detail=ErrorMessages.INSUFFICIENT_PRIVILEGE)
