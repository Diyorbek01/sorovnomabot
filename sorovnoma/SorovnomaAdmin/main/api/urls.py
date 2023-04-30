from django.urls import path
from rest_framework.routers import DefaultRouter

from main.api.views import SorovnomaViewSet, RequiredChannelViewSet

router = DefaultRouter()
router.register('sorovnoma', SorovnomaViewSet, basename='sorovnoma')
router.register('required-channel', RequiredChannelViewSet, basename='required-channel')

urlpatterns = router.urls + [
    # path('create-querter/', create_querter)
]
