from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, TreinoViewSet, PagamentoViewSet, PresencaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'treinos', TreinoViewSet)
router.register(r'pagamentos', PagamentoViewSet)
router.register(r'presencas', PresencaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
