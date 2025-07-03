from rest_framework import serializers

from hr.models.suggestions import Suggestion


class SuggestionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Suggestion
        fields = ['id', 'user', 'request', 'department', 'is_anonymous']

    def get_user(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        allowed_roles = ['admin', 'manager']

        if user and (user.is_superuser or (hasattr(user, 'role') and user.role in allowed_roles)):
            if obj.user:
                return {
                    'id': obj.user.id,
                    'username': obj.user.username,
                    'full_name': obj.user.get_full_name() if hasattr(obj.user, 'get_full_name') else str(obj.user),
                }
            return None

        if obj.is_anonymous:
            return None
        
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'full_name': obj.user.get_full_name() if hasattr(obj.user, 'get_full_name') else str(obj.user),
            }
        return None
