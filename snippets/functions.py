from .models import Snippet
from . import actions


def take_action(snippet: Snippet, action: str):
    if action is actions.close:
        snippet.status = Snippet.Status.closed
        snippet.save()
    else:
        snippet.delete()
