from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi_users.password import PasswordHelper
from zing_product_backend.models import auth_model
from zing_product_backend.app_db.connections import AsyncSession
from zing_product_backend.core.common import RuleName
from zing_product_backend.models.auth_model import PrivilegeGroup, User, PrivilegeRules
from zing_product_backend.reporting import system_log
from zing_product_backend.core.security import schema


async def create_default_user(admin_user, session: AsyncSession):
    # Check if a privilege group already exists

    hash_helper = PasswordHelper()
    user_info_list_m1 = [
        ('E00381', 'shuibin.chen@zingsemi.com'), # shuibin
        ('E00716', 'kwanghun.kim@zingsemi.com'), # dr kim
        ('A00052', 'consultant1@zingsemi.com'), # c1
        ('E00886', 'jiahui.lu@zingsemi.com'),  # lujiahui
        ('E00123', 'Sherky.Xiao@zingsemi.com'), # sherky
        ('E00448', 'julie.li@zingsemi.com'), # julie
        ('E01941','ying.wang@zingsemi.com'), # wangying
        ('E00078', 'yinfeng.li@zingsemi.com'), # yinfeng
        ('E00273', 'jasmin.cui@zingsemi.com'), # jasmin
        ('E01186', 'yang.li@zingsemi.com'), # liyang
        ('E02300', 'wenli.li@zingsemi.com') # liwenli
    ]
    user_name_list_m1_key_user = [
        ('E00886', 'jiahui.lu@zingsemi.com'),  # lujiahui
        ('E00123', 'Sherky.Xiao@zingsemi.com'), # sherky
        ('E00448', 'julie.li@zingsemi.com'), # julie
        ('E00078', 'yinfeng.li@zingsemi.com'), # yinfeng
        ('E00273', 'jasmin.cui@zingsemi.com'), # jasmin
        ('E01186', 'yang.li@zingsemi.com'), # liyang
    ]
    user_name_list_pc = [
        ('E00098', 'qin.he@zingsemi.com'), # heqin
        ('E00710', 'ming.yao@zingsemi.com'), # yaomin
        ('E02076', 'yayuan.xu@zingsemi.com'), # xuyayuan
        ('E01654', 'kay.wang@zingsemi.com') , # wanglianghui
    ]
    user_name_list_ims = [
        ('E02586', 'xinteng.luo@zingsemi.com'),  # xinteng,
        ('E00963', 'xun.wang@zingsemi.com'), # wangxun
        ('E02652', 'xiang.yu@zingsemi.com'), # yuxiang
    ]

    # If no group exists, create an admin group and add this user to it
    ims_dev_rule = auth.PrivilegeRules(rule_name=RuleName.IMS_DEV, rule_description='ims_dev')
    product_assign_view = auth.PrivilegeRules(rule_name=RuleName.PRODUCT_ASSIGN_VIEW,
                                              rule_description='product_assign_view')
    product_assign_change = auth.PrivilegeRules(rule_name=RuleName.PRODUCT_ASSIGN_CHANGE,
                                                rule_description='product_assign_change')
    product_setting_change = auth.PrivilegeRules(rule_name=RuleName.PRODUCT_SETTINGS_CHANGE,
                                                 rule_description='product_setting_change')
    tp_sample_settings_change = auth.PrivilegeRules(rule_name=RuleName.TP_AUTO_SAMPLE_SETTINGS_CHANGE,
                                                    rule_description='tp_sample_setting_change')
    containment_rule_setting_change = auth.PrivilegeRules(rule_name=RuleName.CONTAINMENT_RULE_SETTINGS_CHANGE)

    pc_group = auth.PrivilegeGroup(group_name='product_control', created_by=admin_user.id, created_time=func.now())
    pc_group.privilege_rules.append(product_assign_view)
    pc_group.privilege_rules.append(product_assign_change)

    ims_dev_group = auth.PrivilegeGroup(group_name='ims_dev', created_by=admin_user.id, created_time=func.now())
    ims_dev_group.privilege_rules.append(ims_dev_rule)
    ims_dev_group.privilege_rules.append(product_assign_view)
    ims_dev_group.privilege_rules.append(product_assign_change)
    ims_dev_group.privilege_rules.append(product_setting_change)
    ims_dev_group.privilege_rules.append(tp_sample_settings_change)
    ims_dev_group.privilege_rules.append(containment_rule_setting_change)

    m1_group = auth.PrivilegeGroup(group_name='m1', created_by=admin_user.id, created_time=func.now())
    m1_group.privilege_rules.append(product_assign_view)

    m1_key_user_group = auth.PrivilegeGroup(group_name='m1_key_user', created_by=admin_user.id,
                                            created_time=func.now())
    m1_key_user_group.privilege_rules.append(product_assign_view)
    m1_key_user_group.privilege_rules.append(product_assign_change)
    m1_key_user_group.privilege_rules.append(product_setting_change)
    m1_key_user_group.privilege_rules.append(tp_sample_settings_change)

    for (user_name, user_email) in user_info_list_m1:
        user_create_dict = {
            'user_name': user_name,
            'email': user_email,
            'hashed_password': hash_helper.hash(user_name),
            'is_active': True,
            'is_superuser': False,
        }
        exist_data = await session.execute(select(User).where(User.user_name == user_name))
        user = exist_data.scalars().first()
        if user:
            user.privilege_groups.append(m1_group)
        else:
            user = auth.User(**user_create_dict)
            user.privilege_groups.append(m1_group)
            session.add(user)

    for (user_name, user_email) in user_name_list_m1_key_user:
        user_create_dict = {
            'user_name': user_name,
            'email': user_email,
            'hashed_password': hash_helper.hash(user_name),
            'is_active': True,
            'is_superuser': False,
        }
        exist_data = await session.execute(select(User).where(User.user_name == user_name))
        user = exist_data.scalars().first()
        if user:
            user.privilege_groups.append(m1_key_user_group)
        else:
            user = auth.User(**user_create_dict)
            user.privilege_groups.append(m1_key_user_group)
            session.add(user)

    for (user_name, user_email) in user_name_list_pc:
        user_create_dict = {
            'user_name': user_name,
            'email': user_email,
            'hashed_password': hash_helper.hash(user_name),
            'is_active': True,
            'is_superuser': False,
        }
        exist_data = await session.execute(select(User).where(User.user_name == user_name))
        user = exist_data.scalars().first()
        if user:
            user.privilege_groups.append(pc_group)
        else:
            user = auth.User(**user_create_dict)
            user.privilege_groups.append(pc_group)
            session.add(user)

    for (user_name, user_email) in user_name_list_ims:
        user_create_dict = {
            'user_name': user_name,
            'email': user_email,
            'hashed_password': hash_helper.hash(user_name),
            'is_active': True,
            'is_superuser': False,
        }

        exist_data = await session.execute(select(User).where(User.user_name == user_name))
        user = exist_data.scalars().first()
        if user:
            user.privilege_groups.append(ims_dev_group)
        else:
            user = auth.User(**user_create_dict)
            user.privilege_groups.append(ims_dev_group)
            session.add(user)

    await session.commit()

