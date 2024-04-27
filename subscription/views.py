from django.shortcuts import render, redirect
from .models import Subscriber

# Create your views here.
def unsubscribe(request):
      if request.method == 'POST':
            email= request.GET.get('email')
            
            if email:
                  Subscriber.objects.filter(email=email).delete()
                  return render(request, 'unsubscribe/success.html')
      
      return redirect('hotel:home')