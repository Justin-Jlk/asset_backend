from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AssetMasterViewSet, AssetCategoryDetailsViewSet,
                    DepartmentMasterViewSet, RoleMasterViewSet, UserMasterViewSet,
                    EmployeeRegisterView, EmployeeLoginView)

router = DefaultRouter()
router.register(r'assets', AssetMasterViewSet)
router.register(r'asset-categories', AssetCategoryDetailsViewSet)
router.register(r'departments', DepartmentMasterViewSet)
router.register(r'roles', RoleMasterViewSet)
router.register(r'users', UserMasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('register/', EmployeeRegisterView.as_view(), name='employee-register'),
]
