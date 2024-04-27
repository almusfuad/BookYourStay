from django_cron import CronJobBase, Schedule
from subscription.models import Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.urls import reverse

class SendMonthlyEmails(CronJobBase):
      RUN_AT_TIMES = ['00:00']
      
      schedule = Schedule(run_at_times=RUN_AT_TIMES)
      code = 'subscription.send_monthly_emails'
      
      def do(self):
            current_date =  datetime.now().date()
            
            # Check the exact date for sending monthly emails
            if current_date.day == 28:
                  subscribers = Subscriber.objects.all()
                  
                  # unsubscribe link
                  unsubscribe_link = reverse('unsubscribe')
            
                  # send email to each subscriber
                  for subscriber in subscribers:
                        email_subject = 'Monthly Newsletter'
                        email_body = render_to_string('emails/monthly_newsletter.html')
                        email = EmailMultiAlternatives(email_subject, email_body, to=[subscriber.email])
                        email.attach_alternative(email_body, 'text/html')
                        
                        try:
                              email.send(fail_silently=False)
                        except Exception as e:
                              pass
                  