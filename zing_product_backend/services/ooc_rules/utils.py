from zing_product_backend.core.common import RuleName
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.security_utils import get_rules_from_user


def check_containment_setting_privilege(user: auth_model.User):
    user_rules = get_rules_from_user(user)
    for user_rule in user_rules:
        print(user_rule)
    if any([RuleName.CONTAINMENT_RULE_SETTINGS_CHANGE in user_rules, RuleName.IMS_DEV in user_rules,
            RuleName.ADMIN in user_rules]):
        return True
    else:
        return False
