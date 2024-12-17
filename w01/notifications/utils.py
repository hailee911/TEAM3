from .models import Notification

# 알림생성 함수
# id,message 등록하면됨.
def create_notification(user_id, message):

    Notification.objects.create(
        user_id=user_id,
        message=message
    )