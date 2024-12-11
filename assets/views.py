from rest_framework import viewsets
from .models import AssetMaster, AssetCategoryDetails, DepartmentMaster, RoleMaster, UserMaster,EmployeeAuth
from .serializers import (AssetMasterSerializer, AssetCategoryDetailsSerializer,
                          DepartmentMasterSerializer, RoleMasterSerializer, UserMasterSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from collections import Counter
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


class AssetMasterViewSet(viewsets.ModelViewSet):
    queryset = AssetMaster.objects.all().order_by('id')
    serializer_class = AssetMasterSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def list(self, request, *args, **kwargs):
        asset_master_data = self.get_queryset()
        asset_category_details = AssetCategoryDetails.objects.all()
        asset_based_id_count = Counter([detail.asset_based_id.id for detail in asset_category_details])

        assets = []
        for asset in asset_master_data:
            count = asset_based_id_count.get(asset.id, 0)
            asset_data = {
                "id": asset.id,
                "name": asset.name,
                "asset_based_id": asset.asset_based_id,
                "count": count
            }
            assets.append(asset_data)

        response_data = {
            "assets": assets
        }

        return Response(response_data, status=status.HTTP_200_OK)




class AssetCategoryDetailsViewSet(viewsets.ModelViewSet):
    queryset = AssetCategoryDetails.objects.all()
    serializer_class = AssetCategoryDetailsSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['employee_id', 'asset_number', 'asset_based_id']
    ordering_fields = ['employee_id', 'asset_number', 'asset_based_id']
    ordering = ['employee_id']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = AssetCategoryDetails.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)
        return queryset

    def create(self, request, *args, **kwargs):
        asset_number = request.data.get("asset_number")
        if AssetCategoryDetails.objects.filter(asset_number=asset_number).exists():
            raise ValidationError({"asset_number": "This asset is already assigned to an employee."})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        asset_number = request.data.get("asset_number")
        instance_id = kwargs.get('pk')
        if AssetCategoryDetails.objects.filter(asset_number=asset_number).exclude(id=instance_id).exists():
            raise ValidationError({"asset_number": "This asset is already assigned to another employee."})
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().retrieve(request, *args, **kwargs)

        employee_id = instance.employee_id
        if employee_id:
            try:
                user = UserMaster.objects.get(employee_id=employee_id)
                response.data['employee_details'] = UserMasterSerializer(user).data
            except UserMaster.DoesNotExist:
                response.data['employee_details'] = None
        else:
            response.data['employee_details'] = None
        return response
class DepartmentMasterViewSet(viewsets.ModelViewSet):
    queryset = DepartmentMaster.objects.all()
    serializer_class = DepartmentMasterSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

class RoleMasterViewSet(viewsets.ModelViewSet):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

class UserMasterViewSet(viewsets.ModelViewSet):
    queryset = UserMaster.objects.all()
    serializer_class = UserMasterSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmployeeAuth, UserMaster
from .serializers import EmployeeRegisterSerializer, EmployeeLoginSerializer
import logging

logger = logging.getLogger(__name__)

class EmployeeRegisterView(APIView):
    def post(self, request):
        serializer = EmployeeRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee_id = serializer.validated_data["employee_id"]
        password = serializer.validated_data["password"]

        if EmployeeAuth.objects.filter(employee__employee_id=employee_id).exists():
            return Response({"error": "Employee already registered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_master = UserMaster.objects.get(employee_id=employee_id)
            auth_entry = EmployeeAuth(employee=user_master)
            auth_entry.set_password(password)
            auth_entry.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        except UserMaster.DoesNotExist:
            logger.error(f"User with employee_id {employee_id} does not exist.")
            return Response({"error": "User with this employee_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            return Response({"error": "An internal error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmployeeAuth, UserMaster
from .serializers import EmployeeLoginSerializer, UserMasterSerializer
import hashlib
import time


class EmployeeLoginView(APIView):
    def post(self, request):
        serializer = EmployeeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee_id = serializer.validated_data["employee_id"]
        password = serializer.validated_data["password"]

        try:
            auth_record = EmployeeAuth.objects.get(employee__employee_id=employee_id)
            if auth_record.check_password(password):
                
               
                unique_data = f"{employee_id}{time.time()}".encode()
                token = hashlib.sha256(unique_data).hexdigest()  

   
                employee_details = UserMasterSerializer(auth_record.employee).data


                response_data = {
                    "statuscode": "200",  
                    "success": "true",  
                    "data": {
                        "message": "Login successful",
                        "token": token,       
                        "employee_details": employee_details
                    }
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "statuscode": "400",  
                    "success": "false",
                    "data": {
   
                        "message": "Invalid credentials"
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeAuth.DoesNotExist:
            response_data = {
                "statuscode": "400", 
                "success": "false",
                "data": {
   
                    "message": "Invalid credentials"
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
            