from .views import (
    UserViewset,
    ServiceViewSet,
    StatisticsViewSet,
    MainCardSliderViewSet,
    WhyChooseUsViewSet,
    PatientTestimonialViewSet,
    ContactUsViewSet,
    DoctorViewSet,
)
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"user", UserViewset, basename="user")
router.register(r"service", ServiceViewSet, basename="service")
router.register(r"statistics", StatisticsViewSet, basename="statistics")
router.register(r"maincardslider", MainCardSliderViewSet, basename="maincardslider")
router.register(r"whychooseus", WhyChooseUsViewSet, basename="whychooseus")
router.register(r"patienttestimonial", PatientTestimonialViewSet, basename="patienttestimonial")
router.register(r"contactus", ContactUsViewSet, basename="contactus")
router.register(r"doctor", DoctorViewSet, basename="doctor")

urlpatterns = []
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
