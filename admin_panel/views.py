from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from django.contrib import messages
from . forms import AdminProfileForm, AdminPasswordChangeForm
from django.contrib.auth import logout
# Create your views here.


@login_required
def admin_dashboard(request):
      bookings = Booking.objects.all()
      context = {
            'bookings': bookings
      }
      return render(request, 'admin/dashboard.html', context)

@login_required
def admin_profile(request):
      user = request.user
      if request.method == 'POST':
            form = AdminProfileForm(request.POST, instance = user)
            if form.is_valid():
                  form.save()
                  messages.success(request, 'Admin profile updated successfully.')
            else:
                  messages.error(request, 'Admin profile update failed.')
      return redirect('admin_panel:admin-dashboard')


@login_required
def admin_password(request):
      if request.method == 'POST':
            form = AdminPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                  form.save()
                  messages.success(request, 'Admin password updated successfully.')
            else:
                  messages.error(request, 'Admin password update failed')
      return redirect('admin_panel:admin-dashboard')

@login_required
def admin_logout(request):
      if request.method == "GET":
            logout(request)
            messages.success(request, 'Logout successful.')
            return redirect('hotel:home') 