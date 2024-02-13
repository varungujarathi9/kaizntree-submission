from django.urls import path
from .views import (
    ItemListApiView,
    LoginApiView,
    SignupApiView,
    LogoutApiView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Kaizntree API",
        default_version='v1',
        description="API documentation for the Kaizntree app",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('signup/', SignupApiView.as_view(), name='signup'),
    path('item/', ItemListApiView.as_view(), name='item-list'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui')
]
