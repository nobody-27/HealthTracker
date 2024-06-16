from django.urls import path
from health.api.views import (
    UserRegister,
    UserLogin,
    UserProfile,
    HealthRecordList,
    HealthRecordDetail,
    HealthPlanList,
    HealthPlanDetail,
)


app_name = "health"

urlpatterns = [
    path("users/register/", UserRegister.as_view(), name="user-register"),
    path("users/login/", UserLogin.as_view(), name="user-login"),
    path("users/profile/", UserProfile.as_view(), name="user-profile"),
    path("health/records/", HealthRecordList.as_view(), name="health-records"),
    path(
        "health/records/<int:record_id>/",
        HealthRecordDetail.as_view(),
        name="health-record-detail",
    ),
    path("health/plans/", HealthPlanList.as_view(), name="health-plans-list"),
    path(
        "health/plans/<int:plan_id>/",
        HealthPlanDetail.as_view(),
        name="health-plan-detail",
    ),
]
