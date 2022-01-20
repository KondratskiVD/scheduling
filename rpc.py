from typing import List
from pydantic import parse_obj_as

from .models.schedule import Schedule
from .models.security_pd import SecurityScheduleModel


def security_test_create(data: list, skip_validation_if_undefined: bool = True, **kwargs) -> dict:
    scheduling_data = parse_obj_as(List[SecurityScheduleModel], data)
    return {'scheduling': [i.dict() for i in scheduling_data]}


def create_schedule(data: dict) -> int:
    pd_obj = SecurityScheduleModel(**data)
    schedule_id = pd_obj.save()
    return schedule_id


def security_load_from_db_by_ids(ids: List[int]) -> List[dict]:
    if not ids:
        return []
    return [SecurityScheduleModel.from_orm(s).dict() for s in Schedule.query.filter(Schedule.id.in_(ids)).all()]


def delete_schedules(delete_ids: List[int]) -> List[int]:
    Schedule.query.filter(Schedule.id.in_(delete_ids)).delete()
    Schedule.commit()
    return delete_ids
