from django.contrib import admin
from .models import AssetMaster, AssetCategoryDetails, DepartmentMaster, RoleMaster, UserMaster

admin.site.register(AssetMaster)
admin.site.register(AssetCategoryDetails)
admin.site.register(DepartmentMaster)
admin.site.register(RoleMaster)
admin.site.register(UserMaster)
