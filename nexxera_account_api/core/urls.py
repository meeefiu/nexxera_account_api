from rest_framework import routers
from core.views import AccountView

router = routers.DefaultRouter()
router.register('accounts', AccountView)

urlpatterns = router.urls
