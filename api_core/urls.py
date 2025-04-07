"""
URL configuration for api_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from apps.book.api.book.viewsets import BookViewSet
from apps.book.api.comment.viewsets import CommentViewSet
from apps.course.api.course.viewsets import CourseViewSet
from apps.ecommerce.api.order.viewsets import OrderViewSet
from apps.ecommerce.api.product.viewsets import ProductViewSet
from apps.notifications.api.notification.viewsets import NotificationViewSet
from apps.permissions.api.permission.viewsets import (AdminOnlyView,
                                                      SupportOnlyView,
                                                      UserOnlyView)
from apps.presence.api.presence.viewsets import OnlineUsersView
from apps.report.api.report.viewstes import ReportRequestViewSet
from apps.tenants.api.project.viewsets import ProjectViewSet
from apps.throttle.api.viewsets import UploadViewSet
from apps.users.api.auth.viewsets import AuthenticationApiView  # noqa501
from apps.users.api.auth.viewsets import (ChangePasswordView, ConfirmEmailView,
                                          CreateUserView, ForgotPasswordView,
                                          MfaApiView, UnsubscribeApiView,
                                          UserDeleteApiView, UserInfoApiView)
from apps.users.api.healthcheck.viewsets import HealthcheckViewSet
from apps.users.api.profile.viewsets import (ProfessionalApiView,
                                             ProfessionalParamApiView,
                                             ProfileApiView,
                                             ProfileDataApiView)
from apps.users.api.upload.viewsets import FileUploadApiView

schema_view = get_schema_view(
    openapi.Info(
        title="Emannar API",
        default_version='v1',
        description="API da aplicação Emannar",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="robertolima.izphera@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


admin.site.site_header = 'Template Admin'

#  ADMIN
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/health-check/', HealthcheckViewSet.as_view(), name='health-check'), # noqa E501
    path("summernote/", include("django_summernote.urls")),
    path("select2/", include("django_select2.urls")),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), # noqa501
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # noqa501
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # noqa501
]
# + static(settings.MEDIA_URL, document_root=settings.STATIC_URL)
#  ADMIN

route_api_v1 = routers.DefaultRouter()
route_api_v1.register(r'books', BookViewSet, basename='books')  # noqa E501
route_api_v1.register(r'comments', CommentViewSet, basename='comments')  # noqa E501
route_api_v1.register(r'orders', OrderViewSet, basename='orders')  # noqa E501
route_api_v1.register(r'products', ProductViewSet, basename='products')  # noqa E501
route_api_v1.register(r'reports', ReportRequestViewSet, basename='reports')  # noqa E501
route_api_v1.register(r'courses', CourseViewSet, basename='courses')  # noqa E501
route_api_v1.register(r'projects', ProjectViewSet, basename='projects')  # noqa E501
route_api_v1.register(r'uploads', UploadViewSet, basename='uploads')  # noqa E501
route_api_v1.register(r'notifications', NotificationViewSet, basename='notifications')  # noqa E501

urlpatterns.append(path("api/v1/", include(route_api_v1.urls)))

#  AUTH
urlpatterns.append(
    path("api/v1/register-user/", CreateUserView.as_view(), name='register-user') # noqa E501
)
urlpatterns.append(
    path('api/v1/auth-user/', AuthenticationApiView.as_view(), name='auth-user'), # noqa E501
)
urlpatterns.append(
    path('api/v1/auth-mfa/', MfaApiView.as_view(), name='auth-mfa'), # noqa E501
)
urlpatterns.append(
    path('api/v1/me/', UserInfoApiView.as_view(), name='me'), # noqa E501
)
urlpatterns.append(
    path('api/v1/confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'), # noqa E501
)
urlpatterns.append(
    path('api/v1/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'), # noqa E501
)
urlpatterns.append(
    path('api/v1/change-password/', ChangePasswordView.as_view(), name='change-password'), # noqa E501
)
urlpatterns.append(
    path('api/v1/unsubscribe/', UnsubscribeApiView.as_view(), name='unsubscribe'), # noqa E501
)
urlpatterns.append(
    path('api/v1/delete-user/<int:user_id>/', UserDeleteApiView.as_view(), name='delete-user'), # noqa E501
)
urlpatterns.append(
    path('api/v1/upload-file/', FileUploadApiView.as_view(), name='upload-file'), # noqa E501
)

#  PROFILE
urlpatterns.append(
    path('api/v1/profile/', ProfileApiView.as_view(), name='profile'), # noqa E501
)
urlpatterns.append(
    path('api/v1/profile-data/', ProfileDataApiView.as_view(), name='profile-data'), # noqa E501
)
urlpatterns.append(
    path('api/v1/profile-professionals/', ProfessionalApiView.as_view(), name='profile-professionals'), # noqa E501
)
urlpatterns.append(
    path('api/v1/professional/<int:user_id>/', ProfessionalParamApiView.as_view(), name='professional'), # noqa E501
)

urlpatterns.append(
    path("api/v1/admin-only/", AdminOnlyView.as_view(), name='admin-only') # noqa E501
)
urlpatterns.append(
    path("api/v1/user-only/", UserOnlyView.as_view(), name='user-only') # noqa E501
)
urlpatterns.append(
    path("api/v1/support-only/", SupportOnlyView.as_view(), name='support-only') # noqa E501
)

urlpatterns.append(
    path("api/v1/online-users/", OnlineUsersView.as_view(), name='online-users') # noqa E501
)
