from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnlyForEditingAttendance(BasePermission):
    message = 'Editing posts is redirected only to the author'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            print(obj.worker.header_worker.account_id, '121212')
            return True
        return obj.worker.header_worker.account_id == request.user.id

