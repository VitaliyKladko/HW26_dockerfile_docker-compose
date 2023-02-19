from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from schemas import RequestParamsListSchema
from sqlalchemy import text
from utils import build_query
from db import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/perform_query', methods=['POST'])
def perform_query():
    try:
        params = RequestParamsListSchema().load(request.json)
    except ValidationError as error:
        return error.messages, '400'

    result = None
    for query in params['queries']:
        result = build_query(
            cmd=query['cmd'],
            param=query['value'],
            filename=params['filename'],
            data=result,
        )

    return jsonify(result), '200'


@main_bp.route('/test_db')
def test_db():
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
    except Exception as e:
        return jsonify(
            {
                'error': f'{e}',
            }
        )

    return jsonify(
        {
            'result': result,
            'add_test_str': 'test_str_commit'
        }
    )
