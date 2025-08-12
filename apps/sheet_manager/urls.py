from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.sheet.viewsets import SheetUploadAPIView, ManagerSheetViewSet

router = DefaultRouter()
router.register(r'sheets', ManagerSheetViewSet, basename='managersheet')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/upload-sheet/', SheetUploadAPIView.as_view(), name='sheet-upload'),
] 