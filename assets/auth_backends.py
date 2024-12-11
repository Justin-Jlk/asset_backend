from django.contrib.auth.backends import BaseBackend
from .models import EmployeeAuth, UserMaster

class EmployeeIDBackend(BaseBackend):
    def authenticate(self, request, employee_id=None, password=None):
        try:
            auth_record = EmployeeAuth.objects.get(employee__employee_id=employee_id)
            if auth_record.check_password(password):
                return auth_record.employee  
        except EmployeeAuth.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserMaster.objects.get(pk=user_id)
        except UserMaster.DoesNotExist:
            return None
