from rest_framework import routers
from .views import RestaurantViewSet, AddressViewSet, RestaurantInformationViewSet, ScheduleViewSet

router = routers.SimpleRouter()

router.register(r'base', RestaurantViewSet)
router.register(r'address', AddressViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'information', RestaurantInformationViewSet)

urlpatterns = router.urls
