from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from vehicle.models import ChargingStation, Booking


# ================= HOME =================
def home(request):
    stations = ChargingStation.objects.filter(is_active=True)
    return render(request, "home.html", {"stations": stations})


# ================= LOGIN =================
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")   # username, NOT email
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # ✅ LOGIN SUCCESS → PROFILE PAGE
            return redirect("profile")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home')


# ================= REGISTER =================
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()   # ✅ DB me save

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")



# ================= PROFILE =================
@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-id")
    stations = ChargingStation.objects.filter(is_active=True)

    return render(request, "profile.html", {
        "bookings": bookings,
        "stations": stations
    })


# ================= BOOKING =================
@login_required(login_url='login')
def booking(request):
    stations = ChargingStation.objects.filter(is_active=True)
    return render(request, "booking.html", {"stations": stations})


# ================= SLOT PAGE =================
from vehicle.models import Booking
from django.shortcuts import get_object_or_404

@login_required
@login_required
def slot(request, station_id):
    station = ChargingStation.objects.get(id=station_id)

    if request.method == "POST":
        booking = Booking.objects.create(
            user=request.user,
            station=station,
            date=request.POST["date"],
            time_slot=request.POST["time_slot"],
            status="PENDING"
        )
        return redirect("payment", booking_id=booking.id)

    return render(request, "slot.html", {"station": station})




# ================= PAYMENT =================
@login_required(login_url="login")
@login_required
def payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)

    if request.method == "POST":
        # Payment success (fake payment)
        booking.status = "CONFIRMED"
        booking.save()

        return redirect("profile")

    return render(request, "payment.html", {"booking": booking})

# ================= ADMIN DASHBOARD (CUSTOM) =================
@login_required(login_url='login')
def admin_dashboard(request):
    return render(request, 'admin.html')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def admin_dashboard(request):
    return render(request, "admin.html")

from django.contrib.auth.models import User
from vehicle.models import ChargingStation, Booking
from django.db.models import Sum

@staff_member_required
def admin_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "stations": ChargingStation.objects.count(),
        "bookings": Booking.objects.count(),
        "revenue": Booking.objects.filter(status="CONFIRMED")
                    .aggregate(total=Sum("amount"))["total"] or 0
    }
    return render(request, "admin.html", context)