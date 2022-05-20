from SimpleKB.social.models import Notification

def notifications(request):
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
