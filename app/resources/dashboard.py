from .auth import auth_required
from flask_restful import Resource, reqparse
from app.utils import success_api, fail_api
from app.models import UserModels


class DasbBoardInitResource(Resource):

    @auth_required
    def get(self):
        data = {
            "total_task":"30"
        }
        return success_api(data=data)

