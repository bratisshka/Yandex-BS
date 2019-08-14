from django.urls import path

from yandex_bs.imports import views as import_views

urlpatterns = [
    path("imports", import_views.ImportCreateView.as_view(), name="create_import"),
    path("imports/<int:import_id>/citizens", import_views.ImportRetrieveView.as_view(), name="retrieve_import"),
    path("imports/<int:import_id>/citizens/birthdays", import_views.BirthdaysView.as_view(), name="birthdays"),
]
