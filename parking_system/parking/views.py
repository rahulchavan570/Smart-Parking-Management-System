from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Slot, Vehicle
from .ml_model import predict_parking
import datetime


# ------------------ HOME PAGE ------------------
def home(request):
    slots = Slot.objects.all()
    return render(request, 'home.html', {'slots': slots})


# ------------------ PARK VEHICLE ------------------
def park_vehicle(request):
    if request.method == 'POST':
        vehicle_number = request.POST['vehicle_number']
        owner_name = request.POST['owner_name']

        # check if vehicle already parked
        existing = Vehicle.objects.filter(
            vehicle_number=vehicle_number,
            exit_time__isnull=True
        ).first()

        if existing:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Vehicle already parked'})
            return redirect('/')

        # find available slot
        slot = Slot.objects.filter(status='Available').first()

        if slot:
            Vehicle.objects.create(
                vehicle_number=vehicle_number,
                owner_name=owner_name,
                slot=slot
            )

            slot.status = 'Occupied'
            slot.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Vehicle parked in slot {slot.slot_number}'})
            return redirect('/')

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'No available slots'})
            return render(request, 'full.html')

    return redirect('/')


# ------------------ EXIT VEHICLE ------------------
def exit_vehicle(request):
    if request.method == 'POST':
        vehicle_number = request.POST['vehicle_number']

        vehicle = Vehicle.objects.filter(
            vehicle_number=vehicle_number,
            exit_time__isnull=True
        ).first()

        if vehicle:
            slot = vehicle.slot
            slot.status = 'Available'
            slot.save()

            vehicle.exit_time = datetime.datetime.now()
            vehicle.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Vehicle exited successfully'})
            return redirect('/')

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Vehicle not found or already exited'})
            return redirect('/')

    return redirect('/')


# ------------------ GET SLOTS ------------------
def get_slots(request):
    slots = Slot.objects.all()
    slots_html = ''
    for slot in slots:
        status_class = 'bg-success' if slot.status == 'Available' else 'bg-danger'
        icon_class = 'fa-check-circle' if slot.status == 'Available' else 'fa-times-circle'
        slots_html += f'''
            <div class="slot-item d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
                <span class="fw-bold">Slot {slot.slot_number}</span>
                <span class="badge {status_class}">
                    <i class="fas {icon_class}"></i>
                    {slot.status}
                </span>
            </div>
        '''
    return JsonResponse({'slots_html': slots_html})


# ------------------ PARKING PREDICTION (AIML) ------------------
def parking_prediction(request):
    # 1. Get current time
    now = datetime.datetime.now()
    current_hour = now.hour

    # 2. Get AI Prediction from our Python script
    ai_prediction = predict_parking(current_hour)

    # 3. Check current real-time database status
    total_slots = Slot.objects.count()
    occupied_slots = Slot.objects.filter(status='Occupied').count()
    available_slots = total_slots - occupied_slots

    # Calculate occupancy percentage
    occupancy_percentage = 0
    if total_slots > 0:
        occupancy_percentage = int((occupied_slots / total_slots) * 100)

    # Logic: If DB is physically full, show FULL. Otherwise, show AI prediction.
    status = ai_prediction
    if total_slots > 0 and occupied_slots == total_slots:
        status = "FULL (Real-time)"

    return render(request, 'prediction.html', {
        'current_time': now.strftime("%I:%M %p"),
        'status': status,
        'available_slots': available_slots,
        'occupied_slots': occupied_slots,
        'occupancy_percentage': occupancy_percentage,
        'total_slots': total_slots
    })