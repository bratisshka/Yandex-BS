from django.urls import path

from yandex_bs.imports import views as import_views

urlpatterns = [
    path("imports", import_views.create_import, name="create_import"),
    path("imports/<int:import_id>/citizens", import_views.retrieve_import, name="retrieve_import"),
    path("imports/<int:import_id>/citizens/birthdays", import_views.retrieve_birthdays, name="birthdays"),
    path("imports/<int:import_id>/towns/stat/percentile/age", import_views.retrieve_town_stats, name="town_stats"),
]
