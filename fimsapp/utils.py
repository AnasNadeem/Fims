import jwt

from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import login

from .serializers import UserSerializer
from .models import UserOTP, User

from rest_framework import status, exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        if b' ' in auth_header:
            prefix, token = auth_header.decode('utf-8').split(' ')
        else:
            token = auth_header.decode('utf-8')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.filter(email=payload['email']).first()
            request.user = user
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(f'Token has been expired. Login again {ex}')

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(f'Invalid Token. {ex}')

        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(f'No such user exist. {no_user}')

        return super().authenticate(request)


def send_or_verify_otp(request, user, otp=None, resent=False):
    resp_data = UserSerializer(user).data
    user_otp = UserOTP.objects.filter(user=user).first()
    if not user_otp:
        random_str = get_random_string(6)
        user_otp = UserOTP()
        user_otp.user = user
        user_otp.otp = random_str
        user_otp.save()
        send_otp(user, user_otp)
        resp_data['message'] = f'OTP has been sent to {user.email}.'
        resp_status = status.HTTP_200_OK
        return resp_data, resp_status

    if resent:
        random_str = get_random_string(6)
        user_otp.otp = random_str
        user_otp.is_verified = False
        user_otp.save()

    auth_token = jwt.encode({'email': user.email}, settings.SECRET_KEY, algorithm='HS256')
    if (not otp) and (user_otp.is_verified):
        if not user.is_active:
            user.is_active = True
            user.save()

        login(request, user)
        resp_data = UserSerializer(user).data
        resp_data['token'] = auth_token
        resp_status = status.HTTP_200_OK
        return resp_data, resp_status

    if (not otp) and (not user_otp.is_verified):
        send_otp(user, user_otp)
        resp_data['message'] = f'OTP has been sent to {user.email}.'
        resp_status = status.HTTP_200_OK
        return resp_data, resp_status

    if user_otp.otp == otp:
        user_otp.is_verified = True
        user_otp.save()

        user.is_active = True
        user.save()

        login(request, user)
        resp_data = UserSerializer(user).data
        resp_data['token'] = auth_token
        resp_status = status.HTTP_200_OK
        return resp_data, resp_status
    else:
        user_otp.otp = get_random_string(6)
        user_otp.save()
        send_otp(user, user_otp)
        resp_data = {'error': 'Invalid OTP. Resending OTP. Check email.'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return resp_data, resp_status


def send_otp(user, user_otp):
    subject = "Verify your email address.."
    message = f"{user_otp.otp} is your OTP."
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email],
              fail_silently=False)
