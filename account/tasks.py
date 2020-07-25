from background_task import background
from datetime import timedelta
from .models import User


@background(schedule=timedelta(days=2))
def remove_user(user_id):
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except User.DoesNotExist:
        return
    user.delete()
