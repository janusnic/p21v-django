from django.conf.urls import url, include
from rest_framework import routers
from .views import PostViewSet, CategoryViewSet, ListViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'lists', ListViewSet)
urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

urlpatterns += router.urls