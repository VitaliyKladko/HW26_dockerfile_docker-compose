from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas import RequestParamsListSchema

main_bp = Blueprint('main', __name__)


@main_bp.route('/perform_query', methods=['POST'])
def perform_query():
    try:
        params = RequestParamsListSchema().load(request.json)
    except ValidationError as error:
        return error.messages, '400'

    return jsonify(params)
