from django.db import models


# Slot Model (Parking Space)
class Slot(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
    ]

    slot_number = models.IntegerField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    def __str__(self):
        return f"Slot {self.slot_number} - {self.status}"


# Vehicle Model (Parking Entry)
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=50)

    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehicle_number

    # Optional: Calculate parking duration
    def parking_duration(self):
        if self.exit_time:
            return self.exit_time - self.entry_time
        return None