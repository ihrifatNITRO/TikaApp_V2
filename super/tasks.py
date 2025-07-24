# super/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Child

@shared_task
def send_vaccine_reminders():
    today = timezone.now().date()

    # Find children whose next vaccine date is 3 days from now
    three_days_from_now = today + timedelta(days=3)
    children_3_day_reminder = Child.objects.filter(next_vaccine_date=three_days_from_now)

    # Find children whose next vaccine date is 1 day from now
    one_day_from_now = today + timedelta(days=1)
    children_1_day_reminder = Child.objects.filter(next_vaccine_date=one_day_from_now)

    # Combine the querysets
    all_children_to_remind = children_3_day_reminder | children_1_day_reminder

    for child in all_children_to_remind:
        parent = child.parent
        subject = f'Vaccine Reminder for {child.child_name}'
        message = (
            f'Hi {parent.first_name},\n\n'
            f'This is a friendly reminder that {child.child_name}\'s next vaccine is scheduled for {child.next_vaccine_date}.\n\n'
            f'Thank you,\nThe TikaApp Team'
        )

        # Send the email
        send_mail(subject, message, 'no-reply@tikaapp.com', [parent.email])
        print(f"Sent reminder to {parent.email} for {child.child_name}")

    return f"Sent reminders for {all_children_to_remind.count()} children."