from typing import List, Dict, Tuple, Sequence, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload, selectinload
from zing_product_backend.core import exceptions
from zing_product_backend.models import auth, tp_auto_assign
from zing_product_backend.services.tp_auto_sample import schemas


class TPautoSampleDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    # rule setting
    async def get_all_sample_plan_info(self) -> Sequence[schemas.TpSamplePlanInfo]:
        stmt = (select(tp_auto_assign.SamplePlan).options(selectinload(
            tp_auto_assign.SamplePlan.containment_rule)).order_by(
            tp_auto_assign.SamplePlan.plan_priority))
        result = await self.session.execute(stmt)
        sample_info_list: List[schemas.TpSamplePlanInfo] = []
        for row in result.scalars():
            updated_user_name = (await self.session.execute(select(auth.User).filter(
                auth.User.id == row.updated_by))).scalar_one_or_none().user_name

            sample_info_list.append(schemas.TpSamplePlanInfo(
                id=row.id,
                sample_plan_name=row.sample_plan_name,
                key_1=row.key_1,
                key_2=row.key_2,
                key_3=row.key_3,
                sample_type=row.sample_type,
                frequency_type=row.frequency_type,
                frequency_value=row.frequency_value,
                must_include_seed_tail=row.must_include_seed_tail,
                plan_priority=row.plan_priority,
                containment_rule_id=row.containment_rule.id,
                containment_rule_name=row.containment_rule.rule_name,
                updated_by=row.updated_by,
                updated_user_name=updated_user_name,
                updated_time=row.updated_time,
            ))
        return sample_info_list

    async def get_sample_plan_info_by_id(self, plan_id: int) -> schemas.TpSamplePlanInfo:
        stmt = select(tp_auto_assign.SamplePlan).filter(schemas.TpSamplePlanInfo.id == plan_id)
        result = await self.session.execute(stmt)
        exist_orm = result.scalars().one_or_none()
        if exist_orm is None:
            raise exceptions.NotFoundError(rf"not found rule id: {plan_id}")
        else:
            updated_user_name = (await self.session.execute(select(auth.User).filter(
                auth.User.id == exist_orm.updated_by))).scalar_one_or_none().user_name
            return schemas.TpSamplePlanInfo(
                id=exist_orm.id,
                sample_plan_name=exist_orm.sample_plan_name,
                key_1=exist_orm.key_1,
                key_2=exist_orm.key_2,
                key_3=exist_orm.key_3,
                sample_type=exist_orm.sample_type,
                frequency_type=exist_orm.frequency_type,
                frequency_value=exist_orm.frequency_value,
                must_include_seed_tail=exist_orm.must_include_seed_tail,
                plan_priority=exist_orm.plan_priority,
                containment_rule_id=exist_orm.containment_rule.id,
                containment_rule_name=exist_orm.containment_rule.containment_rule_name,
                updated_by=exist_orm.updated_by,
                updated_user_name=updated_user_name,
                updated_time=exist_orm.updated_time,
            )

    async def insert_sample_plan(self, plan_info: schemas.InsertTpSamplePlan, user: auth.User
                                 ) -> int:
        exist_orm = (await self.session.execute(
            select(tp_auto_assign.SamplePlan).filter(
                tp_auto_assign.SamplePlan.sample_plan_name == plan_info.sample_plan_name,
            )
        )).scalar_one_or_none()

        if exist_orm is not None:
            updated_user_name = (await self.session.execute(select(auth.User).filter(
                auth.User.id == exist_orm.updated_by))).scalar_one_or_none().user_name


            raise exceptions.DuplicateError(rf"already exist rule name: "
                                            rf"{plan_info.sample_plan_name}, id: {exist_orm.id},"
                                            rf"updated by: {updated_user_name}")
        else:
            new_sample_plan = tp_auto_assign.SamplePlan(
                sample_plan_name=plan_info.sample_plan_name,
                key_1=plan_info.key_1,
                key_2=plan_info.key_2,
                key_3=plan_info.key_3,
                sample_type=plan_info.sample_type,
                frequency_type=plan_info.frequency_type,
                frequency_value=plan_info.frequency_value,
                must_include_seed_tail=plan_info.must_include_seed_tail,
                plan_priority=plan_info.plan_priority,
                containment_rule_id=plan_info.containment_rule_id,
                updated_by=user.id,
                updated_user_name=user.user_name,
            )
            self.session.add(new_sample_plan)
            await self.session.commit()
            await self.session.refresh(new_sample_plan)
            return new_sample_plan.id


    async def update_sample_plan(self, plan_info: schemas.UpdateTpSampleRuleInfo, user: auth.User) \
            -> schemas.TpSamplePlanInfo:
        exist_orm = (await self.session.execute(
            select(tp_auto_assign.SamplePlan).filter(
                tp_auto_assign.SamplePlan.id == plan_info.id,
            )
        )).scalar_one_or_none()

        if exist_orm is None:
            raise exceptions.NotFoundError(rf"not found rule id: {plan_info.id}")
        else:
            exist_orm.sample_plan_name = plan_info.sample_plan_name
            exist_orm.key_1 = plan_info.key_1
            exist_orm.key_2 = plan_info.key_2
            exist_orm.key_3 = plan_info.key_3
            exist_orm.sample_type = plan_info.sample_type
            exist_orm.frequency_type = plan_info.frequency_type
            exist_orm.frequency_value = plan_info.frequency_value
            exist_orm.must_include_seed_tail = plan_info.must_include_seed_tail
            exist_orm.plan_priority = plan_info.plan_priority
            exist_orm.last_updated_user = user
            await self.session.commit()
            await self.session.refresh(exist_orm)

            return schemas.TpSamplePlanInfo(
                id=exist_orm.id,
                sample_plan_name=exist_orm.sample_plan_name,
                key_1=exist_orm.key_1,
                key_2=exist_orm.key_2,
                key_3=exist_orm.key_3,
                sample_type=exist_orm.sample_type,
                frequency_type=exist_orm.frequency_type,
                frequency_value=exist_orm.frequency_value,
                must_include_seed_tail=exist_orm.must_include_seed_tail,
                plan_priority=exist_orm.plan_priority,
                containment_rule_id=exist_orm.containment_rule_id,
                containment_rule_name=exist_orm.containment_rule.containment_rule_name,
                updated_user_name=user.user_name,
                updated_by=user.id,
                updated_time=exist_orm.updated_time,

            )
