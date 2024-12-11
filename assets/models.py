from django.db import models


class AssetMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    asset_based_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.asset_based_id

class AssetCategoryDetails(models.Model):
    asset_based_id = models.ForeignKey(AssetMaster, on_delete=models.CASCADE)
    employee_id = models.IntegerField()
    asset_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.asset_based_id.asset_based_id} - {self.employee_id}"
class DepartmentMaster(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class RoleMaster(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class UserMaster(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    employee_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name
from django.contrib.auth.hashers import make_password, check_password

class EmployeeAuth(models.Model):
    employee = models.OneToOneField(UserMaster, on_delete=models.CASCADE, related_name="auth")
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
