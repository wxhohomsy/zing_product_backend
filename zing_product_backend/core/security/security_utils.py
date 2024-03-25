from typing import Set, List
from zing_product_backend.models import auth_model
from zing_product_backend.core.security import schema


def get_rules_from_user(user_orm: auth_model.User) -> Set[str]:
    rule_set = set()
    for group in user_orm.privilege_groups:
        for rule in group.privilege_rules:
            if rule.is_active:
                rule_set.add(rule.rule_name)
    return rule_set


def get_user_info_from_user(user: auth_model.User) -> schema.UserInfo:
    privilege_group_info_list: List[schema.PrivilegeGroupInfo] = []
    privilege_rule_info_list: List[schema.PrivilegeRuleInfo] = []
    for privilege_group in user.privilege_groups:
        if privilege_group.group_deleted:
            continue
        privilege_group_info_list.append(schema.PrivilegeGroupInfo(
            group_name=privilege_group.group_name,
            group_description=privilege_group.group_description,
            id=privilege_group.id,
        ))
        for privilege_rule in privilege_group.privilege_rules:
            if not privilege_rule.is_active:
                continue
            privilege_rule_info_list.append(schema.PrivilegeRuleInfo(
                rule_name=privilege_rule.rule_name,
                rule_description=privilege_rule.rule_description,
                id=privilege_rule.id,
            ))
    user_info = schema.UserInfo(
        id=user.id,
        user_name=user.user_name,
        email=user.email,
        is_active=user.is_active,
        privilege_groups=privilege_group_info_list,
        privilege_rules=privilege_rule_info_list,
    )
    return user_info


