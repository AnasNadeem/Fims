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
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

######################
# ---- USER ---- #
######################


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_active",
            "date_joined",
        )


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=4, write_only=True)
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': ('User already exist with this email')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=4)
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'password')
        read_only_fields = ('password', )


class ChangePasswordSerializer(ModelSerializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password was entered incorrectly. Please enter it again. ")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'Confirm_password': _("The password fields didn't match.")})
        password_validation.validate_password(data['password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceSerializerWithDoctor(ModelSerializer):
    doctors = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "description",
            "image",
            "doctors",
            "showinmaincard",
            "tags",
            "is_featured",
        )

    def get_doctors(self, obj):
        doctors = Doctor.objects.filter(service=obj.id)
        serializer = DoctorSerializer(doctors, many=True)
        return serializer.data


class StatisticsSerializer(ModelSerializer):
    class Meta:
        model = Statistics
        fields = "__all__"


class MainCardSliderSerializer(ModelSerializer):
    class Meta:
        model = MainCardSlider
        fields = "__all__"


class WhyChooseUsSerializer(ModelSerializer):
    class Meta:
        model = WhyChooseUs
        fields = "__all__"


class PatientTestimonialSerializer(ModelSerializer):
    class Meta:
        model = PatientTestimonial
        fields = "__all__"


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class DoctorSerializer(ModelSerializer):
    service = ServiceSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"
