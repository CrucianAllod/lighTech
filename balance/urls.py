from rest_framework.routers import DefaultRouter
from balance.views import BalanceViewSet

router = DefaultRouter()
router.register(r'', BalanceViewSet, basename='balance')
urlpatterns = router.urls