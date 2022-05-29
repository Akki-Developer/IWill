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

# # Create your views here.
# def home(request):
#     return HttpResponse('Hello, World!')

# def chatBot_darkmode(request):
#     context = {
#             # "data":"Gfg is the best",
#             # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         }
#         # return response with template and context
#     return render(request, "chatBot_darkmode.html", context)

# def chatBot_lightmode(request):
#     context = {
#             # "data":"Gfg is the best",
#             # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         }
#         # return response with template and context
#     return render(request, "chatBot_lightmode.html", context)


# class User(APIView):
#     permission_classes = (AllowAny,)
#     data = ""
def chatBot_lightmode(request):
    if request.method == 'GET':
        # import pdb;pdb.set_trace()
        status_code = status.HTTP_200_OK
        uId= request.GET.get('uId')
        # restart= request.GET.get('restart')
        # uId = request.GET.get('uId')
        # name = request.GET.get('name')
        # age = request.GET.get('age')
        # country = request.GET.get('country')
        # state = request.GET.get('state')
        # city = request.GET.get('city')
        category = request.GET.get('cat_id')
        # gender = request.GET.get('gender')
        level = request.GET.get('level')
        issue = request.GET.get('issue')
        # language = request.GET.get('language')
        # severity = request.GET.get('severity')
        url = "https://iwill.epsyclinic.com/index.php/Psybot/get_user_details"
        headers = {
            'cache-control': "no-cache"
            }
        payload = json.dumps({
                                "uId": uId
                                })
        response = requests.request("POST", url, headers=headers,data=payload)
        res = response.json()

        print(payload)

        print("res",res)
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
        # session_id = request.session.get('uId')
        # obj_session= Bot_sessions.objects.filter(user_id=uId).get()
        # session_id= obj_session.bot_session_id
        
        # if not session or restart == 1:
        # session_id = uuid.uuid1()
        # print(session_id)
        user = UserModel.objects.filter(userId=uId).exists()
        
        if not user:
            print("new User _______________________________________")
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
            print("dataaa",data)
            session_id = uuid.uuid1()
            print(session_id)
            data = Bot_sessions(user_id=uId,
                        bot_session_id=session_id,
                        category_id = cat_id
                        )
            data.save()
            if data:
                context = {
                    # 'success': 'True', 
                    # 'message': 'USER Added Successfully',
                    "user_id": uId,
                    "session_id": session_id
                    }
            # return Response(context,status=status_code)
        else:
            print("previous User --------------------------------------------------")
            obj_session= Bot_sessions.objects.filter(user_id=uId).last()
            print(obj_session)
            session_id= obj_session.bot_session_id
            print(session_id)
            print("dataaa else")
            context = {
            # 'success': 'True', 
            # 'message': 'User Exist',
            'user_id': uId,
            'session_id': session_id
            }
            # return Response(context,status=status_code)

        # context = {
        #     # "data":"Gfg is the best",
        #     # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # }
        # # return response with template and context
            
        data = User_exercise_status(exercise_id="1",
                    bot_session_id=session_id,
                    completion_status = False
                    )
        data.save()
        print(data)
        return render(request, "chatBot_lightmode.html", context)

def chatBot_darkmode(request):
    if request.method == 'GET':
        # import pdb;pdb.set_trace()
        status_code = status.HTTP_200_OK

        # uId = request.GET.get('uId')
        # name = request.GET.get('name')
        # age = request.GET.get('age')
        # country = request.GET.get('country')
        # state = request.GET.get('state')
        # city = request.GET.get('city')
        # cat_id = request.GET.get('cat_id')
        # gender = request.GET.get('gender')
        # # level = request.GET.get('level')
        # # issue = request.GET.get('issue')
        # language = request.GET.get('language')
        # severity = request.GET.get('severity')
        url = "https://iwill.epsyclinic.com/index.php/Psybot/get_user_details"
        headers = {
            'cache-control': "no-cache"
            }
        uId= request.GET.get('uId')
        payload = json.dumps({
                                "uId": uId
                                })
        response = requests.request("POST", url, headers=headers,data=payload)
        res = response.json()

        print(payload)

        print("res",res)
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
        # session_id = request.session.get('uId')
        # session_id = uuid.uuid1()
        # print(session_id)
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
            print("dataaa",data)

            session_id = uuid.uuid1()
            print(session_id)
            data = Bot_sessions(user_id=uId,
                        bot_session_id=session_id,
                        category_id = cat_id
                        )
            data.save()
            if data:
                context = {
                    # 'success': 'True', 
                    # 'message': 'USER Added Successfully',
                    "user_id": uId,
                    "session_id": session_id
                    }
            # return Response(context,status=status_code)
        else:
            obj_session= Bot_sessions.objects.filter(user_id=uId).last()
            print(obj_session)
            session_id= obj_session.bot_session_id
            print(session_id)
            print("dataaa else")
            context = {
            # 'success': 'True', 
            # 'message': 'User Exist',
            'user_id': uId,
            'session_id': session_id
            }
            # return Response(context,status=status_code)

        # context = {
        #     # "data":"Gfg is the best",
        #     # "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # }
        # # return response with template and context
        
        data = User_exercise_status(exercise_id="1",
                    bot_session_id=session_id,
                    completion_status = False
                    )
        data.save()
        return render(request, "chatBot_darkmode.html", context)


        

class botAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        user_id = request.data['user_id']
        message = request.data['message']
        restart = request.data['restart']
        sender = request.data['sender']
        print("user_id",user_id)
        print("restart",restart)
        print("sender",sender)

        user = UserModel.objects.filter(userId=user_id).exists()
        if restart == True:
            obj_session= Bot_sessions.objects.filter(user_id=user_id).last()
            print(obj_session)
            category = obj_session.category_id
            session_id = uuid.uuid1()
            print("new session ",session_id)
            print("new session -----------------------",session_id)
            data = Bot_sessions(user_id=user_id,
                        bot_session_id=session_id,
                        category_id = category
                        )
            data.save()
        else:
            obj_session= Bot_sessions.objects.filter(user_id=user_id).last()
            print(obj_session)
            session_id= obj_session.bot_session_id
            print("old session -----------------------",session_id)
            print("sender", sender)    
    


        # if sender  "135":
        session = Bot_sessions.objects.filter(bot_session_id=session_id).get()

        print("sessionid ------------------------",session_id)
        print("session-----",session)
        print("sessionid-----",session.id)
        print("session",session.category_id)
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

        response = requests.request("POST", url, headers=headers, data=payload)
        output_text = response.json()[0]["text"]
        print("response__________",output_text)
        data = Bot_conversation(user_id=uId,
                    bot_session_id=session_id,
                    category_id = category,
                    input_text= message ,
                    response_text = output_text
                    )
        data.save()
        print(data)
        
        if output_text in ["Bye!"]:
            data = User_exercise_status(exercise_id="1",
                    bot_session_id=session_id,
                    completion_status = True
                    )
            data.save()
        print(data)
        return Response(response.json())


class chathistory(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        session_id = request.data['session_id']
        user_id = request.data['user_id']
        print("session_id", session_id)
        print("user_id", user_id)

        chat = Bot_conversation.objects.filter(bot_session_id=session_id).values()

        print(chat)
        # return chat

        # user=request.GET['user_id']
        # print(user)
    
        all_messages=list(Bot_conversation.objects.filter(bot_session_id=session_id,user_id=user_id).values('input_text','response_text').order_by('id'))    
        return JsonResponse(all_messages,safe=False)


class check_status(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        session_id = request.data['session_id']
        user_id = request.data['user_id']
        print("session_id", session_id)
        print("user_id", user_id)

        status = User_exercise_status.objects.filter(bot_session_id=session_id,exercise_id="1").values('completion_status')

        print(status)
        # return chat

        # user=request.GET['user_id']
        # print(user)
    
        all_status=list(User_exercise_status.objects.filter(bot_session_id=session_id,exercise_id="1").values('completion_status').order_by('id'))    
        return JsonResponse(all_status,safe=False)       