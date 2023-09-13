import jwt
from django.conf import settings

from .models import (
    User,
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
    Doctor,
)
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ServiceSerializer,
    StatisticsSerializer,
    MainCardSliderSerializer,
    WhyChooseUsSerializer,
    PatientTestimonialSerializer,
    ContactUsSerializer,
    DoctorSerializer,
)
from .permissions import (
    IsAuthenticated,
    UserPermission,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework import status, response
from rest_framework.decorators import action
from .utils import send_or_verify_otp


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def get_permissions(self):
        user_permission_map = {
            "update": UserPermission,
            'list': IsAuthenticated,
            "change_password": UserPermission,
        }
        if self.action in user_permission_map:
            self.permission_classes = [user_permission_map.get(self.action)]
        return super().get_permissions()

    def get_serializer_class(self):
        user_serializer_map = {
            "create": RegisterSerializer,
            "login": LoginSerializer,
            "change_password": ChangePasswordSerializer,
        }
        return user_serializer_map.get(self.action.lower(), UserSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        authenticated = user.check_password(password)
        if not authenticated:
            return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['post'])
    def forget_password(self, request):
        data = request.data
        email = data.get('email', '')
        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user, resent=True)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['post'])
    def token_login(self, request):
        data = request.data
        token = data.get('token')
        if not token:
            return response.Response({"status": "Token's field not provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.filter(email=payload['email']).first()
        if user:
            user_serializer_data = UserSerializer(user).data
            return response.Response(user_serializer_data, status=status.HTTP_200_OK)
        return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        data = request.data
        email = data.get('email', '')
        change_password = data.get('change_password', False)
        new_password = data.get('new_password', '')

        if not email:
            return response.Response({'error': 'Email cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        otp = data.get('otp', '')
        if not otp:
            return response.Response({'error': 'OTP cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user, otp)

        if change_password and resp_status == status.HTTP_200_OK:
            user.set_password(new_password)
            user.save()
            resp_data['message'] = 'Password changed successfully.'

        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['put'])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("password changed successfully ", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseViewSet(ModelViewSet):
    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ('showinmaincard',)


class StatisticsViewSet(BaseViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer


class MainCardSliderViewSet(BaseViewSet):
    queryset = MainCardSlider.objects.all()
    serializer_class = MainCardSliderSerializer


class WhyChooseUsViewSet(BaseViewSet):
    queryset = WhyChooseUs.objects.all()
    serializer_class = WhyChooseUsSerializer


class PatientTestimonialViewSet(BaseViewSet):
    queryset = PatientTestimonial.objects.all()
    serializer_class = PatientTestimonialSerializer


class ContactUsViewSet(BaseViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class DoctorViewSet(BaseViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
