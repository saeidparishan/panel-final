
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from hr.views.leave_request import LeaveRequestViewSet
from hr.views.suggestions import SuggestionViewSet



router = DefaultRouter()
router.register(r'Suggestion_viewset', SuggestionViewSet, basename='Suggestion') 
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')



urlpatterns = [
    path('api/', include(router.urls)),
    
]

