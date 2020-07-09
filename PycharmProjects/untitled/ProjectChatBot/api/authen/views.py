# File: requester.views.py
# Description:
# Author             Date                       Change Description
# bcdai            8/7/2020                     Create new function
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from . import contains, models
from ProjectChatBot import jwt_authen


@api_view(['POST'])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def login(request):
    print(request.META)
    try:
        obj_login = {}
        response = contains.get_response_authen(None)
        data_input = request.data
        obj_login = {
            "user_name": data_input['user_name'],
            "password": data_input['password']
        }

        ip_request = request.META['REMOTE_ADDR']
        browser_request = request.META['HTTP_USER_AGENT']
        menu_access = ""
        token = ""

        data_output = models.login(obj_login)

        user_id = data_output['user_id']
        code_output = data_output['code']
        if code_output == 0:
            token = jwt_authen.create_token(user_id,obj_login['user_name'],obj_login['password'], menu_access, ip_request, browser_request)
        contains.get_response_authen(code_output)
        response['token'] = token
        response['code'] = code_output
    except Exception as e:
        print("authen.views -> login -> ex", e)

    return Response(response)