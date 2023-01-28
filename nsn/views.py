
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from profiles.models import *
from rest_framework.authtoken.models import Token
from .tokens import account_activation_token


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            # first_name = data['firstName'] if data['firstName'] != None else ''
            # last_name = data['lastName'] if data['lastName'] != None else ''
            first_name = ''
            last_name = ''
            email = data['email']
            password = data['password']
            password2 = data['password2']
            username = data['username']

            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            if password != password2:
                return Response({'error': 'Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'},)
            else:
                if len(password) >= 8:
                    if not User.objects.filter(username=username, email=email).exists():
                        user = User.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            first_name=first_name,
                            last_name=last_name)

                        user.save()
                        subject = 'Account Activation'
                        activate_url = "https://api.orangewaves.tech/"+'activate/' + \
                            str(user.pk) + '/' + \
                            account_activation_token.make_token(user)+'/'
                        message = f"""
                       Hey there{username},
                       Thank you for signing up for NSNCO,
                          Please click on the link below to activate your account
                            {activate_url}

                        Regards,
                        Team NsN


                        """
                        #user.email_user(subject, message)

                        if User.objects.filter(username=username).exists():
                            return Response({'success': 'User created successfully'},status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'User already exists'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Password must be at least 8 characters'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        token = data['token']

        if Token.objects.filter(key=token).exists():
            return Response({
                'status': 'success',
                'msg': 'Token is valid',
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failed',
                'msg': 'Token is invalid',
            },status=status.HTTP_400_BAD_REQUEST)
