from django.urls import path

from . import views

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("borg/", views.BorgView.as_view(), name="borg_list"),
    path("borg/add/", views.BorgRepositoryCreateView.as_view(), name="borg_add"),
    path(
        "borg/update/<int:pk>/",
        views.BorgRepositoryUpdateView.as_view(),
        name="borg_update",
    ),
    path(
        "borg/delete/<int:pk>/",
        views.BorgRepositoryDeleteView.as_view(),
        name="borg_delete",
    ),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("delete/", views.DeleteUserView.as_view(), name="delete"),
    path("imprint/", views.ImprintView.as_view(), name="imprint"),
]
