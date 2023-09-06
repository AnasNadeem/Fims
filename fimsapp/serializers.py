from .models import (
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
)
from rest_framework.serializers import ModelSerializer


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


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
