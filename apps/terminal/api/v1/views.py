from django.db.models import Q
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
import requests
from requests.auth import HTTPBasicAuth
import json

class AddPersonView(APIView):
    # http://127.0.0.1:8000/api/terminal/v1/add-person/

    def post(self, *args, **kwargs):

        url = 'http://10.69.69.120/ISAPI/AccessControl/UserInfo/Record?format=json'

        myobj = {
            "UserInfo": {
                "employeeNo": "881",
                "name": "test881",
                "userType": "normal"
            }
        }

        x = requests.post(url, data=myobj, auth=HTTPBasicAuth('admin', '12345678a'))

        print(x.text)
        return Response({"result": json.loads(x.text)})
