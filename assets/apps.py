from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = 'assets'
    verbose_name = 'Активы'

    def ready(self):
        import assets.recievers
