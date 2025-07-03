from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdvancePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # فقط کاربران احراز هویت شده دسترسی دارند
        if request.method == 'POST':
            return user.is_authenticated and user.role != 'admin'
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        status = obj.status

        # اجازه ویرایش فقط در مرحله مربوطه و توسط نقش مشخص شده
        if request.method in ['PUT', 'PATCH']:
            return (
                (status == 'pending_1' and user.role == 'department_manager') or
                (status == 'approved_1' and user.role == 'human_resources') or
                (status == 'approved_2' and user.role == 'supervisor') or
                (status == 'approved_3' and user.role == 'admin')
            )

        # برای GET → فقط نقش مرتبط در آن مرحله، یا صاحب درخواست
        if request.method == 'GET':
            return (
                user == obj.user or
                (obj.status == 'pending_1' and user.role == 'department_manager') or
                (obj.status == 'approved_1' and user.role == 'human_resources') or
                (obj.status == 'approved_2' and user.role == 'supervisor') or
                (obj.status == 'approved_3' and user.role == 'admin')
            )

        return False