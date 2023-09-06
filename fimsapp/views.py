from .models import (
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
)
from .serializers import (
    ServiceSerializer,
    StatisticsSerializer,
    MainCardSliderSerializer,
    WhyChooseUsSerializer,
    PatientTestimonialSerializer,
    ContactUsSerializer,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework import status, response


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
