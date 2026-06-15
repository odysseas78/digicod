from django.db.models.signals import post_save
from django.dispatch import receiver
from eshop.models import Orders
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Orders)
def notify_order_status(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user_id}",  # Benutzergruppe
        {
            "type": "send_update",
            "message": {
                "order_id": instance.id,
                "product_name": instance.product_name,
                "status": instance.status,
            },
        }
    )
