from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from users.models import User
from progress.models import Progress
from logs.mongo_schema.models import ActivityLog


def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    enrollments = user.enrollments.select_related("course").all()
    progress_entries = Progress.objects.filter(user=user).select_related("course")

    # Build progress map for efficiency
    progress_map = {p.course_id: p for p in progress_entries}

    courses_data = [
        {
            "course_id": str(enrollment.course.id),
            "title": enrollment.course.title,
            "progress": (
                progress_map.get(enrollment.course_id).percent_complete
                if progress_map.get(enrollment.course_id)
                else 0
            ),
        }
        for enrollment in enrollments
    ]

    logs = ActivityLog.objects(user_id=str(user.id)).order_by("-timestamp")[:10]
    log_list = [
        {
            "action": log.action,
            "metadata": log.metadata,
            "ip_address": log.ip_address,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]

    return JsonResponse(
        {
            "user": {"id": str(user.id), "email": user.email, "role": user.role},
            "courses": courses_data,
            "recent_activity": log_list,
        },
        status=200,
    )


def user_activity_logs(request, user_id):
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    try:
        limit = int(request.GET.get("limit", 20))
    except ValueError:
        limit = 20

    skip = (page - 1) * limit

    logs_qs = ActivityLog.objects(user_id=str(user_id)).order_by("-timestamp")
    total_logs = logs_qs.count()
    logs = logs_qs.skip(skip).limit(limit)

    log_list = [
        {
            "action": log.action,
            "metadata": log.metadata,
            "ip_address": log.ip_address,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]

    return JsonResponse(
        {
            "page": page,
            "limit": limit,
            "total": total_logs,
            "logs": log_list,
        },
        status=200,
    )
