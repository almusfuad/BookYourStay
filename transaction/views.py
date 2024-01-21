from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from . models import Transaction
from . forms import DepositForm
from django.urls import reverse_lazy
from hotel.models import Hotel
from student.models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
class DepositCreateView(CreateView):
      model = Transaction
      form_class = DepositForm
      template_name = 'deposit.html'
      success_url = reverse_lazy('hotel:home')
      
      def form_valid(self, form):
            user = self.request.user
            
            student, created = Student.objects.get_or_create(user = user)
            
            form.instance.student = student
            form.instance.status = 'D'
            
            deposit_amount = form.cleaned_data['amount']
            student.balance += deposit_amount
            student.save()
            
            Transaction.objects.create(student = student, amount = deposit_amount)
            
            messages.success(self.request, 'Deposit successful!')
            return super().form_valid(form)
            
      def get(self, request, *args, **kwargs):
            # Only logged-in users can make a deposit
            if not self.request.user.is_authenticated:
                  messages.error(self.request, 'You need to be logged in to make a deposit.')
                  return redirect(reverse_lazy('login'))

            return super().get(request, *args, **kwargs)