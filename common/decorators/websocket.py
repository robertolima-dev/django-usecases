from functools import wraps

from channels.exceptions import DenyConnection

from apps.chat.models import Room


def ensure_room_participant(get_room_id_from_scope):
    """
    Garante que o usuário conectado está presente na Room.
    Exemplo de uso: @ensure_room_participant(lambda scope: scope["url_route"]["kwargs"]["room_id"])
    """  # noqa: E501
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            room_id = get_room_id_from_scope(self.scope)
            user = self.user

            try:
                room = await Room.objects.aget(id=room_id)
                if not await room.users.filter(id=user.id).aexists():  # noqa: E501
                    raise DenyConnection(f"Usuário {user} não pertence à sala {room_id}")  # noqa: E501
            except Room.DoesNotExist:
                raise DenyConnection(f"Sala {room_id} não existe.")  # noqa: E501

            return await func(self, *args, **kwargs)

        return wrapper
    return decorator
