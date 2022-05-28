from SimpleKB.social.models import Notification

def notifications(request):
    """
    Context processor that gets the users unread
    notifications count for the context.
    """
    if not request.user.is_authenticated:
        return {}
    notification_count = (Notification
                          .objects
                          .filter(user=request.user, seen=False)
                          .count()
                          )
    if notification_count > 99:
        notification_count = '99+'
    return {
        "notifications": notification_count
    }
