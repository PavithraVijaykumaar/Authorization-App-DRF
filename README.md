# DRF Authentication App

This Django Rest Framework (DRF) Authentication app provides user registration, login, and logout functionality, utilizing JWT (JSON Web Tokens) for secure token-based authentication. The app uses **Django**, **DRF**, and **django-rest-framework-simplejwt** for managing tokens. It supports user registration with password validation, user login with token issuance, and secure logout with token invalidation (blacklisting).

## Libraries Used

- **Django**: A high-level Python web framework for rapid development and clean, pragmatic design.
- **Django Rest Framework (DRF)**: A powerful toolkit for building Web APIs in Django.
- **djangorestframework-simplejwt**: Provides a simple and secure way to implement JWT authentication with Django Rest Framework.
- **django.contrib.auth**: For managing user authentication, authorization, and user-related functionality.
  
## Installed Libraries

Ensure the following libraries are installed in your environment for the app to work correctly:

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

The app assumes you have a working Django project with the necessary configurations for DRF and JWT.

## Explanation of Views

### 1. **Registration** (`RegisterView`)
- **Endpoint**: `POST /register/`
- **Functionality**: Allows a new user to register by providing an email, username, and password. 
- **Flow**: 
  - Data is validated using the `RegisterSerializer`.
  - If valid, the user is created, and a response with the user data is returned (status `201 Created`).
  - If invalid, the errors are returned (status `400 Bad Request`).

**Code Explanation**:
```python
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 2. **Login** (`LoginAPIView`)
- **Endpoint**: `POST /login/`
- **Functionality**: Authenticates the user using the provided username and password and returns JWT tokens for authentication.
- **Flow**: 
  - Data is validated using the `LoginSerializer`.
  - If valid, JWT tokens (`access` and `refresh`) are returned in the response (status `200 OK`).
  - If invalid, error messages are returned (status `400 Bad Request` or `401 Unauthorized`).

**Code Explanation**:
```python
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 3. **Logout** (`LogoutAPIView`)
- **Endpoint**: `POST /logout/`
- **Functionality**: Logs out the user by blacklisting the provided refresh token, rendering it invalid.
- **Flow**: 
  - Only authenticated users can log out (requires a valid access token).
  - The `LogoutSerializer` processes the request and invalidates the provided refresh token.
  - A success message is returned with status `204 No Content` upon successful logout.

**Code Explanation**:
```python
class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## Explanation of Serializers

### 1. **RegisterSerializer**
- Handles user registration and ensures that the username is alphanumeric and meets the password length criteria.
- Creates a user object with the provided email, username, and password.

### 2. **LoginSerializer**
- Authenticates the user using their username and password.
- If valid, it generates and returns the JWT tokens (`access` and `refresh`).
- Raises an `AuthenticationFailed` error if authentication fails.

### 3. **LogoutSerializer**
- Takes a `refresh` token from the request and blacklists it using the `RefreshToken` from `django-rest-framework-simplejwt`.
- This renders the token invalid, effectively logging the user out.

## User Model

The custom **User model** extends Django's `AbstractUser` and adds an email field for unique identification. It also includes a method to generate JWT tokens (`tokens()`), which returns both `refresh` and `access` tokens.

### User Model Code:
```python
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
```

## API Flow

1. **Registration**: 
   - Endpoint: `/register/`
   - Required fields: `email`, `username`, `password`
   - Response: User data with status `201 Created` on success or error details on failure.

2. **Login**:
   - Endpoint: `/login/`
   - Required fields: `username`, `password`
   - Response: JWT tokens (`access`, `refresh`) with status `200 OK` on success or error details on failure.

3. **Logout**:
   - Endpoint: `/logout/`
   - Required field: `refresh` (the refresh token to invalidate)
   - Response: Success message on successful logout or error details on failure.

## Conclusion

This DRF Authentication app provides secure user authentication using JWTs, including the ability to register, log in, and log out users with token management. It can be easily integrated into any Django project requiring user authentication via a RESTful API. 
