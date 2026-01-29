from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, created, **kwargs):
    # Check if the status has changed or if it's a new order
    if created or instance.status != getattr(instance, '_original_status', None):
        subject = f"Order #{instance.id} Status Updated - SavoRelle"
        
        if created:
            message = f"Hi {instance.full_name},\n\nYour order #{instance.id} has been placed successfully. Current status: {instance.status}.\n\nThank you for choosing SavoRelle!"
        else:
            message = f"Hi {instance.full_name},\n\nThe status of your order #{instance.id} has been changed to: {instance.status}.\n\nWe are working hard to deliver your food with elegance.\n\nThank you, SavoRelle Team"
        
        recipient_list = [instance.email]
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            # Update the original status so multiple saves in one request don't re-trigger (rare but good practice)
            instance._original_status = instance.status
        except Exception as e:
            print(f"Error sending email: {e}")
