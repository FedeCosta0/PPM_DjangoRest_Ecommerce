from django.apps import AppConfig


class EcommerceUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce_users'

    def ready(self):
        import ecommerce_users.signals
