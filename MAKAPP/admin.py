from django.contrib import admin
from .models import Employee, JobTitle


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gross_salary')


class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('position', 'basic_salary')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(JobTitle, JobTitleAdmin)

