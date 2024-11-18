from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import UserSerializer, get_user_model, LoginSerializer

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


# Create your views here.
# data_signal = dispatch.Signal()

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter().order_by('-date_joined')
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'role']
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                User.objects.create_user(**serializer.validated_data)
            except Exception as e:
                return Response({'message': str(e)}, status=500)
            
            data = {
                "message": "User Successfully Created"
            }
            return Response(data, status=201)
        
        return Response(serializer.errors)
    
    
    
@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view(['POST'])
def user_login(request):
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)

            if user:
                if user.is_active==True:
                
                    try:
                        
                        refresh = RefreshToken.for_user(user)

                        user_detail = {}
                        user_detail['id']   = user.id
                        user_detail['email'] = user.email
                        user_detail['role'] = user.role
                        user_detail['access'] = str(refresh.access_token)
                        user_detail['refresh'] = str(refresh)
                        
                            
                        data = {
        
                            "message":"success",
                            'data' : user_detail,
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    

                    except Exception as e:
                        raise e
                
                else:
                    data = {
                        'error': 'This account has not been activated'
                    }

                    return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    'error': 'Please provide a valid email and a password'
                }

                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                'error': serializer.errors
            }
            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

# class UserLogin(APIView):
    
        
    
#     def post(self, request):
        
#         if request.method == "POST":
#             serializer = LoginSerializer(data=request.data)
#             if serializer.is_valid():
#                 data = serializer.validated_data
#                 print(data['email'], data['password'])
#                 try:
                
#                     user = User.objects.get(email=data['email'])
#                 except User.DoesNotExist:
#                     return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
#                 if not user.check_password(data['password']):
#                     return Response({'message': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
                
#                 login(request, user)
                
                
                
                
#                 if user:
#                     if user.is_active==True:
                    
#                         try:
#                             refresh = RefreshToken.for_user(user)

#                             user_detail = {}
#                             user_detail['id']   = user.id
#                             user_detail['email'] = user.email
#                             user_detail['role'] = user.role
#                             user_detail['access'] = str(refresh.access_token)
#                             user_detail['refresh'] = str(refresh)
                            
                                
#                             data = {
            
#                                 "message": "success",
#                                 'data': user_detail,
#                             }
#                             return Response(data, status=status.HTTP_200_OK)
                        

#                         except Exception as e:
#                             raise e
                    
#                     else:
#                         data = {
#                             'error': 'This account has not been activated'
#                         }

#                         return Response(data, status=status.HTTP_403_FORBIDDEN)

#                 else:
#                     data = {
#                         'error': 'Please provide a valid email and a password'
#                     }

#                     return Response(data, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 data = {
#                     'error': serializer.errors
#                 }
                
#                 return Response(data, status=status.HTTP_400_BAD_REQUEST)