from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import requests
from .models import UserModel ,Bot_sessions
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings   
import json          
import uuid

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def chatBot_lightmode(request):
    if request.method == 'GET':
        # import pdb;pdb.set_trace()
        status_code = status.HTTP_200_OK
        uId= request.GET.get('uId')
        category = request.GET.get('cat_id')
        level = request.GET.get('level')
        issue = request.GET.get('issue')
        url = "https://iwill.epsyclinic.com/index.php/Psybot/get_user_details"
        headers = {
            'cache-control': "no-cache"
            }
        payload = json.dumps({
                                "uId": uId
                                })
        response = requests.request("POST", url, headers=headers,data=payload)
        res = response.json()

        name= res['Data']['name']
        gender= res['Data']['gender']['label']
        age= res['Data']['age']['id']
        country= res['Data']['country']
        cat_id = res['Data']['issue_id']
        state= res['Data']['state']
        city= res['Data']['city']
        language= res['Data']['language']
        severity= res['Data']['level']['label']
        request.session["uId"] = uId
        user = UserModel.objects.filter(userId=uId).exists()
        
        if not user:
            data = UserModel(userId=uId,
                    name=name,
                    gender=gender,
                    age=age,
                    country=country,
                    state=state,
                    city=city,
                    cat_id=cat_id,
                    # level=level,
                    # issue=issue,
                    language=language,
                    severity=severity
                    # is_staff="True"
                    )
            data.save()
            session_id = uuid.uuid1()
            data_session = Bot_sessions(user_id=uId,
                        bot_session_id=session_id,
                        category_id = cat_id
                        )
            data_session.save()
            data_status = User_exercise_status(exercise_id="1",
                        bot_session_id=session_id,
                        completion_status = False
                        )
            data_status.save()
            if data:
                context = {
                    "user_id": uId,
                    "session_id": session_id
                    }
        else:
            obj_session= Bot_sessions.objects.filter(user_id=uId).last()
            session_id= obj_session.bot_session_id
            data_status = User_exercise_status(exercise_id="1",
                        bot_session_id=session_id,
                        completion_status = False
                        )
            data_status.save()
            context = {
                'user_id': uId,
                'session_id': session_id
            }

        # print(data)
        return render(request, "chatBot_lightmode.html", context)

class botAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        user_id = request.data['user_id']
        message = request.data['message']
        restart = request.data['restart']
        sender = request.data['sender']

        user = UserModel.objects.filter(userId=user_id).exists()
        if restart == True:
            obj_session= Bot_sessions.objects.filter(user_id=user_id).last()
            category = obj_session.category_id
            session_id = uuid.uuid1()
            data = Bot_sessions(user_id=user_id,
                        bot_session_id=session_id,
                        category_id = category
                        )
            data.save()
        else:
            obj_session= Bot_sessions.objects.filter(user_id=user_id).last()
            session_id= obj_session.bot_session_id  

        # if sender  "135":
        session = Bot_sessions.objects.filter(bot_session_id=session_id).get()

        category = session.category_id
        uId = session.user_id
        if category in [1,3,4,7]:
            bot = "Depression"
        else:
            bot = "Anxiety"    

        if bot == "Depression":
            url = "http://localhost:5005/webhooks/rest/webhook"
        elif bot == "Anxiety":
            url = "http://localhost:5006/webhooks/rest/webhook"    
        payload = json.dumps({
        "sender": sender,
        "message": message
        })

        headers = {
        'Content-Type': 'application/json'
        }
        # response.json()[0]["buttons"] = ""
        response = requests.request("POST", url, headers=headers, data=payload)
        print("response                __________", response.json()[0])
        if "buttons" in response.json()[0]:
            next_response = response.json()[0]["buttons"]
        else:
            next_response = ""
        print("response__________",next_response)
        output_text = response.json()[0]["text"]
        print("response__________",output_text)
        data = Bot_conversation(user_id=uId,
                    bot_session_id=session_id,
                    category_id = category,
                    input_text= message ,
                    response_text = output_text,
                    next_response = str(next_response)
                    )
        data.save()
        # print(data)
        
        if output_text in ["Bye!"]:
            data = User_exercise_status(exercise_id="1",
                    bot_session_id=session_id,
                    completion_status = True
                    )
            data.save()
        # print(data)
        return Response(response.json())


class chathistory(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        session_id = request.data['session_id']
        user_id = request.data['user_id']

        chat = Bot_conversation.objects.filter(bot_session_id=session_id).values()
        # next_response=list(Bot_conversation.objects.filter(bot_session_id=session_id,user_id=user_id).values('next_response').order_by('id'))    
        # print(next_response)
        all_messages=list(Bot_conversation.objects.filter(bot_session_id=session_id,user_id=user_id).values('input_text','response_text','next_response').order_by('id'))    
        print(all_messages)
        return JsonResponse(all_messages,safe=False)


class check_status(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        session_id = request.data['session_id']
        user_id = request.data['user_id']
        print(session_id)
        status = User_exercise_status.objects.filter(bot_session_id=session_id,exercise_id="1")
        print(status)
        all_status=list(User_exercise_status.objects.filter(bot_session_id=session_id,exercise_id="1").values('completion_status'))[-1]
        print(all_status)
        return JsonResponse(all_status,safe=False)       