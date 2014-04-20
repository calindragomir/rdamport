from django.contrib import admin
from main.models import Ship, Container, Dock, Employee, DockHistory

admin.site.register(Ship)
admin.site.register(Container)
admin.site.register(Dock)
admin.site.register(Employee)
admin.site.register(DockHistory)