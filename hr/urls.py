
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from hr.views.leave_request import LeaveRequestViewSet
from hr.views.suggestions import SuggestionViewSet
from . import views


router = DefaultRouter()
# advance route
router.register(r'advance', views.AdvancehrViewSet, basename='advance')

router.register(r'Suggestion_viewset', SuggestionViewSet, basename='Suggestion') 
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')


urlpatterns = [
    path('', include(router.urls)),
    # report
    path('report/',views.ReportsListCreateView.as_view(),name='report-view'),
    # resume
    path('resume/',views.Resume_View,name='resume-view'),
    # define user
    path('define-user/',views.DefineUserCreateView.as_view(),name='resume-view'),
]

