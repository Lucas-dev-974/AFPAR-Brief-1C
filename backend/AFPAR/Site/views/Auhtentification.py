from django.http import JsonResponse

# Rest Permissions
from rest_framework.permissions import IsAuthenticated
# Simple JWT 
from rest_framework_simplejwt.tokens import RefreshToken
# Rest decorators
from rest_framework.decorators import *
# Auth 
from django.contrib.auth import authenticate
# Serializer
from Site.Serializers import *


'''
    This method will check if token is valid or not

    @param request
    @return Json with status
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkToken(request):
    return JsonResponse({'status': True})

'''
    This method will connect an user if the credentials he given is correct, else if not return an error 401 with an message
    @param request
    @return Json with the data user just connected and its token
'''
@api_view(['POST'])
def login(request):
        login_form = LoginSerializer(data=request.data)
        
        if login_form.is_valid():
            username = request.data['username']
            password = request.data['password']
           
            authenticated_user = authenticate(username = username, password = password)
            
            if authenticated_user is not None:
                # puis on instancie un object user qui contient les infos de l'utilisateur 
                _user = {
                    "id":       authenticated_user.id,
                    "username": authenticated_user.username,
                    "email":    authenticated_user.email
                }

                # ensuite on génère un token de connexion qui seras utiliser dans toutes les requêtes au niveau du front end 
                token = RefreshToken.for_user(authenticated_user)
                return JsonResponse({'token': str(token.access_token), 'user': _user})
            else:
                return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)
        else: 
            return JsonResponse({'error': 'Veuillez transmetre un nom d\'utilisateur et un mot de passe !'}, status = 403)
