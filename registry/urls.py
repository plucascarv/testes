from rest_framework.routers import DefaultRouter
from .views import MunicipioViewSet, PessoaViewSet, EnderecoViewSet

router = DefaultRouter()
router.register(r'municipios', MunicipioViewSet)
router.register(r'pessoas', PessoaViewSet)
router.register(r'enderecos', EnderecoViewSet)

urlpatterns = router.urls