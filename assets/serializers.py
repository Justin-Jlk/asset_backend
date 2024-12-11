from rest_framework import serializers
from .models import AssetMaster, AssetCategoryDetails, DepartmentMaster, RoleMaster, UserMaster, EmployeeAuth

class AssetMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaster
        fields = '__all__'



class DepartmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMaster
        fields = '__all__'

class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = '__all__'

class UserMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = '__all__'

class EmployeeAuthSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = EmployeeAuth
        fields = ['employee_id', 'password']

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        password = validated_data.pop('password')
        
        employee = UserMaster.objects.get(employee_id=employee_id)
        auth = EmployeeAuth(employee=employee)
        auth.set_password(password)
        auth.save()
        return auth

class EmployeeRegisterSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

class EmployeeLoginSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

class AssetCategoryDetailsSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField() 
    employee_details = serializers.SerializerMethodField()  

    class Meta:
        model = AssetCategoryDetails
        fields = ['id', 'asset_number', 'asset_based_id', 'employee_id', 'department', 'employee_details']

    def get_department(self, obj):
        try:
            user = UserMaster.objects.get(employee_id=obj.employee_id)
            return user.department.name 
        except UserMaster.DoesNotExist:
            return None

    def get_employee_details(self, obj):
        try:
            user = UserMaster.objects.get(employee_id=obj.employee_id)
            return UserMasterSerializer(user).data 
        except UserMaster.DoesNotExist:
            return None

    def validate_employee_id(self, value):
        if not UserMaster.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError(f"Employee with employee_id {value} does not exist.")
        return value

