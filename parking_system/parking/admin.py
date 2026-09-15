from django.contrib import admin
from .models import Slot, Vehicle

class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    list_filter = ('status',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'owner_name', 'slot')
    search_fields = ('vehicle_number',)

admin.site.register(Slot, SlotAdmin)
admin.site.register(Vehicle, VehicleAdmin)