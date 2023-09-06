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
)
from .permissions import (
    IsAuthenticated,
    UserPermission,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework import status, response
from rest_framework.decorators import action


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def get_permissions(self):
        user_permission_map = {
            "update": UserPermission,
            'list': IsAuthenticated,
            "reset_forget_password": UserPermission,
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

        user_serializer_data = UserSerializer(user).data
        return response.Response(user_serializer_data, status=status.HTTP_200_OK)

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
