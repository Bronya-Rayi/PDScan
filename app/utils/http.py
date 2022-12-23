def success_api(message: str = "Success", code: int = 0, data = {}):
    """ 成功响应 默认值”成功“ """
    json_message = {
            "status": code,
            "msg": message,
            "data": data
        }
    return json_message


def fail_api(message: str = "Fail", code: int = 400, data={}):
    """ 失败响应 默认值“失败” """
    json_message = {
            "status": code,
            "msg": message,
            "data": data
        }
    return json_message

