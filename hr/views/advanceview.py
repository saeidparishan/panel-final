from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from hr.models import Advancehr
from hr.serializers import Advance_HR_Serializer
from hr.permission import AdvancePermission

class AdvancehrViewSet(viewsets.ModelViewSet):
    serializer_class = Advance_HR_Serializer
    permission_classes = [AdvancePermission]

    def get_queryset(self):
        user = self.request.user
        role = user.role

        if role == 'employee':
            return Advancehr.objects.filter(user=user)

        if role == 'department_manager':
            return Advancehr.objects.filter(status='pending_1')
        elif role == 'human_resources':
            return Advancehr.objects.filter(status='approved_1')
        elif role == 'supervisor':
            return Advancehr.objects.filter(status='approved_2')
        elif role == 'admin':
            return Advancehr.objects.filter(status='approved_3')

        return Advancehr.objects.none()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        next_status = self._get_next_status(instance.status, approved=True, user=user)
        if not next_status:
            return Response({'detail': 'شما مجاز به تایید این مرحله نیستید.'}, status=403)

        suggested_amount = request.data.get('suggested_amount')

    # ذخیره مبلغ پیشنهادی در فیلد مربوط
        if suggested_amount:
            if user.role == 'department_manager':
                instance.department_manager_amount = suggested_amount
            elif user.role == 'human_resources':
                instance.human_resources_amount = suggested_amount
            elif user.role == 'supervisor':
                instance.supervisor_amount = suggested_amount
            elif user.role == 'admin':
                instance.admin_amount = suggested_amount

        instance.status = next_status
        instance.save()

        return Response({
            'status': next_status,
            'suggested_amount': suggested_amount,
        }, status=200)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        next_status = self._get_next_status(instance.status, approved=False, user=user)
        if not next_status:
            return Response({'detail': 'شما مجاز به رد این مرحله نیستید.'}, status=403)

        instance.status = next_status
        instance.save()
        return Response({'status': next_status}, status=200)

    def _get_next_status(self, current_status, approved, user):
        role = user.role
        transitions = {
            'pending_1': ('approved_1', 'rejected_1', 'department_manager'),
            'approved_1': ('approved_2', 'rejected_2', 'human_resources'),
            'approved_2': ('approved_3', 'rejected_3', 'supervisor'),
            'approved_3': ('approved_4', 'rejected_4', 'admin'),
        }

        if current_status not in transitions:
            return None

        success, fail, allowed_role = transitions[current_status]
        if role != allowed_role:
            return None

        return success if approved else fail