from background_task import background
from datetime import timedelta
from .models import User


@background(schedule=timedelta(days=2))
def remove_user(username: str):
    try:
        User.objects.get(username=username, is_active=False).delete()
    except User.DoesNotExist:
        return
