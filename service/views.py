from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework.exceptions import AuthenticationFailed

class RegisterView(APIView):
    def post(self, request):
        try:
            # Initialize the RegisterSerializer with the data
            serializer = RegisterSerializer(data=request.data)
            
            # Validate the data and save the user if valid
            if serializer.is_valid():
                serializer.save()
                user_data = serializer.data
                return Response(user_data, status=status.HTTP_201_CREATED)
            
            # If validation fails, return the errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Handle any unexpected errors that might occur during registration
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    def post(self, request):
        try:
            # Initialize the LoginSerializer with the request data
            serializer = LoginSerializer(data=request.data)
            
            # Validate and process the login if valid
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # If validation fails, return the serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthenticationFailed as auth_err:
            # Specific exception for invalid credentials
            return Response({"detail": str(auth_err)}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            # Catch any other unexpected errors
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            # Initialize the LogoutSerializer with the request data
            serializer = LogoutSerializer(data=request.data)
            
            # Validate the serializer and perform the logout logic
            if serializer.is_valid():
                serializer.save()  # Perform the actual logout action (e.g., blacklisting token)
                return Response({"detail": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)
            
            # If the serializer is not valid, return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthenticationFailed as auth_err:
            # Handle invalid token case (e.g., user already logged out)
            return Response({"detail": str(auth_err)}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            # Catch any other unexpected errors and return an internal server error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
