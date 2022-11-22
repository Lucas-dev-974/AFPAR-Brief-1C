from django.http import JsonResponse

# Rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Auth 
from django.contrib.auth import authenticate, login

# Serializer
from Site.Serializers import *

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Authentification(APIView):
    
    def post(self, request):
        login_form = LoginSerializer(data=request.data)

        if login_form.is_valid():
            username = request.data['username']
            password = request.data['password']
            
            authenticated_user = authenticate(username = username, password = password)

            if authenticated_user is not None:

                # Si oui alors on le connect
                # Une fois cette fonction appeler les informations de l'utilisateur se retrouve dans le var request -> request.user
                login(request, authenticated_user)

                # puis on instancie un object user qui contient les infos de l'utilisateur 
                _user = {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                }

                # ensuite on génère un token de connexion qui seras utiliser dans toutes les requêtes au niveau du front end 
                token = RefreshToken.for_user(authenticated_user)
                return JsonResponse({'token': str(token.access_token), 'user': _user})
            else:
                return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)
