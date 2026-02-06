from django.urls import path
from . import views


urlpatterns = [
    # path('users/', views.index, name='users'),
    path(
        "users/<uuid:user_id>/dashboard/", views.user_dashboard, name="user-dashboard"
    ),
    path("users/<uuid:user_id>/logs/", views.user_activity_logs, name="user-logs"),
]
