from rest_framework import routers
from .views import RestaurantViewSet, AddressViewSet, ScheduleViewSet, ContactViewSet

router = routers.SimpleRouter()

router.register(r'base', RestaurantViewSet)
router.register(r'address', AddressViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = router.urls
