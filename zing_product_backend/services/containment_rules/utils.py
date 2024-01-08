from zing_product_backend.core.common import RuleName
from zing_product_backend.models import auth
from zing_product_backend.core.security.security_utils import get_rules_from_user


def check_containment_setting_privilege(user: auth.User):
    user_rules = get_rules_from_user(user)
    if any([RuleName.CONTAINMENT_RULE_SETTINGS_CHANGE in user_rules, RuleName.IMS_DEV in user_rules,
            RuleName.ADMIN in user_rules]):
        return True
    else:
        return False