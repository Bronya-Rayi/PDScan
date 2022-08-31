import os

from flask import request, jsonify, current_app
from flask_restful import Resource
from sqlalchemy import desc

from common.utils.http import fail_api, success_api, table_api
from common.utils.upload import upload_one, delete_photo_by_id
from extensions import db
from models import PhotoModels


class FilePhotosResource(Resource):

    def get(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        photo_paginate = PhotoModels.query.order_by(desc(PhotoModels.create_at)
                                                    ).paginate(page=page,
                                                             per_page=limit,
                                                             error_out=False)
        data = [
            {
                'id': item.id,
                'name': item.name,
                'href': item.href,
                'mime': item.mime,
                'size': item.size,
                'ext': item.ext if hasattr(item, 'ext') else "",
                'create_at': str(item.create_at),
            } for item in photo_paginate.items
        ]
        return table_api(result={'items': data,
                                 'total': photo_paginate.total, },
                         code=0)

    def post(self):
        if 'file' in request.files:
            photo = request.files['file']
            mime = request.files['file'].content_type
            file_url = upload_one(photo=photo, mime=mime)

            res = {
                "message": "上传成功",
                "code": 0,
                "success": True,
                "data":
                    {"src": file_url}
            }
            return jsonify(res)
        return fail_api()

    def delete(self):
        """图片批量删除"""
        # TODO bugs 图片删除失败
        ids = request.form.getlist('ids[]')
        photo_name = PhotoModels.query.filter(PhotoModels.id.in_(ids)).all()
        upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
        for p in photo_name:
            os.remove(upload_url + '/' + p.name)
        photo = PhotoModels.query.filter(PhotoModels.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        if photo:
            return success_api(message="删除成功")
        else:
            return fail_api(message="删除失败")


class FilePhotoResource(Resource):
    """图片数据"""

    def delete(self, photo_id):
        res = delete_photo_by_id(photo_id)
        if res:
            return success_api(message="删除成功")
        else:
            return fail_api(message="删除失败")
