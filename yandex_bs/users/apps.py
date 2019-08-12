from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "yandex_bs.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import yandex_bs.users.signals  # noqa F401
        except ImportError:
            pass
