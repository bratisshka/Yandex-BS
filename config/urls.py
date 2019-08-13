from django.urls import path

from yandex_bs.imports import views as import_views

urlpatterns = [
    path("imports", import_views.ImportCreateView.as_view(), name="create_import"),
]
