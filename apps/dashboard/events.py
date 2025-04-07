from datetime import datetime
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_admin_event(event_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "send_admin_event",
            "event_type": event_type,
            "data": serialize_data(data),
        }
    )


def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def serialize_data(data):
    return {k: serialize_value(v) for k, v in data.items()}
