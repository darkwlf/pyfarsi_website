from .models import Snippet


def close_snippet(snippet: Snippet):
    snippet.status = Snippet.Status.closed
    snippet.save()
