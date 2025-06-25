
from django.urls import path
from .views import TutorProfileListView, ApplyAsTutorView, ApproveTutorView

urlpatterns = [
    path('', TutorProfileListView.as_view(), name='tutor-list'),
    path('apply/', ApplyAsTutorView.as_view(), name='tutor-apply'),
    path('admin/approve/<int:pk>/', ApproveTutorView.as_view(), name='tutor-approve'),
]
