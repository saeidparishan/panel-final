from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hr.models.suggestions import Suggestion
from hr.serializers.suggestions import SuggestionSerializer
from hr.permission.permission_leavereques_suggestion import SuggestionPermission

class SuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestionSerializer
    permission_classes = [SuggestionPermission, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # سوپر یوزر و مدیر کل همه پیشنهادها را می‌بینند
        if user.is_superuser or (hasattr(user, 'role') and user.role in ['admin', 'manager']):
            return Suggestion.objects.all()

        # اگر مدیر دپارتمان هست (department_manager)
        if hasattr(user, 'role') and user.role == 'department_manager':
            # فقط پیشنهادهایی که در دپارتمان خودش هستن ببینه
            return Suggestion.objects.filter(department__in=[user.department])

        # سایر کاربران فقط پیشنهادهای خودشان را ببینند
        return Suggestion.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    