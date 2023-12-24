from django.apps import AppConfig


class BjstarticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BJSTArticle'

    def ready(self):
        import BJSTArticle.signals