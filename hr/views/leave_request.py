from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from hr.models.leave_request import LeaveRequest
from hr.serializers.Leave_request import LeaveRequestSerializer
from hr.permission.permission_leavereques_suggestion import LeaveRequestPermission,  IsNotManager, IsDepartmentManager
from hr.utils import STATUS_VISIBILITY




APPROVERS = ['supervisor', 'department_manager', 'human_resources', 'manager']
STATUS_BY_ROLE = {
    'employee': 'pending_2',  # مستقیم برای تایید مدیر دپارتمان
    'supervisor': 'pending_2',
    'department_manager': 'pending_3',
    'human_resources': 'pending_4',
}

class LeaveRequestViewSet(viewsets.ModelViewSet):
    message = "شما دسترسی لازم را ندارید."
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [LeaveRequestPermission, IsAuthenticated]


    def get_queryset(self):
        user = self.request.user

        if user.role in ['supervisor', 'department_manager']:
            return LeaveRequest.objects.filter(user__department=user.department)

        if user.role in ['human_resources', 'manager']:
            return LeaveRequest.objects.all()

        return LeaveRequest.objects.filter(user=user)
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsNotManager()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDepartmentManager()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'manager':
            raise PermissionDenied('مدیر کل نمی‌تواند مرخصی ثبت کند.')
        default_status = STATUS_BY_ROLE.get(user.role, 'pending_2')
        serializer.save(user=user, status=default_status)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'department_manager':
            return Response({'detail': 'فقط مدیر دپارتمان می‌تواند ویرایش کند.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'department_manager':
            return Response({'detail': 'فقط مدیر دپارتمان می‌تواند حذف کند.'}, status=403)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        user = request.user
        current_status = leave.status

        # مرحله بعدی را در صورت رد طی کن
        status_flow = {
            'pending_2': 'pending_3',
            'pending_3': 'pending_4',
            'pending_4': 'rejected_4',
        }

        if current_status not in status_flow:
            return Response({'detail': 'امکان رد کردن این درخواست وجود ندارد.'}, status=400)

        new_status = status_flow[current_status]
        leave.status = new_status
        leave.save()
        return Response({'detail': f'درخواست رد و به مرحله بعد منتقل شد ({new_status}).'})