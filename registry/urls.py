from rest_framework.routers import DefaultRouter
from .views import MunicipalityViewSet, PersonViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'municipalities', MunicipalityViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = router.urls