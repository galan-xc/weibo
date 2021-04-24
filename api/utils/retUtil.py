from flask import jsonify


def InfoRet(data=None, msg="success", code=1, **kwargs):
    context = {
        "code": code,
        "msg": msg,
        "data": data,
    }
    context.update(kwargs)
    return jsonify(context)


def ErrorRet(data=None, msg="error", code=0, **kwargs):
    context = {
        "code": code,
        "msg": msg,
        "data": data,
    }
    context.update(kwargs)
    return jsonify(context)
