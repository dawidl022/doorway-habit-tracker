from http import HTTPStatus

from flask import Blueprint, jsonify, request
from validation import abort_with_habit_not_found, validate_uuid

from .dtos import CheckIn as CheckInDTO
from .models import CheckIn
from .service import CheckInService

bp = Blueprint("check_ins", __name__, url_prefix="/habits")

CHECK_IN_ENDPOINT = "/<id>/check-ins"
STREAK_ENDPOINT = "/<id>/streak"


@bp.get(CHECK_IN_ENDPOINT)
def get_check_ins(id: str, check_in_service: CheckInService):
    habit_id = validate_uuid(id)
    check_ins = check_in_service.get_check_ins(habit_id)
    if check_ins is None:
        abort_with_habit_not_found()
    return jsonify([CheckInDTO(check_in) for check_in in check_ins])


@bp.put(CHECK_IN_ENDPOINT)
def check_in(id: str, check_in_service: CheckInService):
    habit_id = validate_uuid(id)
    check_in = CheckIn.from_dict(request.json)
    check_in_service.check_in(habit_id, check_in)
    return "", HTTPStatus.NO_CONTENT


@bp.delete(CHECK_IN_ENDPOINT)
def delete_check_in(id: str, check_in_service: CheckInService):
    habit_id = validate_uuid(id)
    check_in = CheckIn.from_dict(request.json)
    check_in_service.delete_check_in(habit_id, check_in.date)
    return "", HTTPStatus.NO_CONTENT


@bp.get(STREAK_ENDPOINT)
def get_streaks(id: str, check_in_service: CheckInService):
    habit_id = validate_uuid(id)
    return jsonify(check_in_service.get_streaks(habit_id))
