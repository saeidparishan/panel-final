from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from hr.models import Define_User

class ExpiredUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                define_user = Define_User.objects.get(username=user.username)
                if (
                    not define_user.password_changed and
                    define_user.password_created_at and
                    define_user.password_created_at < timezone.now() - timedelta(hours=48)
                ):
                    user.delete()
                    define_user.delete()
                    return JsonResponse({'detail': 'اکانت شما منقضی شده است.'}, status=403)
            except Define_User.DoesNotExist:
                pass
        return self.get_response(request)