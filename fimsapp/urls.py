from .views import (
    # UserViewset,
)
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.SimpleRouter(trailing_slash=False)
# router.register(r"user", UserViewset, basename="user")


urlpatterns = []
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
