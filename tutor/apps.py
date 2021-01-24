from django.apps import AppConfig


class TutorConfig(AppConfig):
    name = 'tutor'

    def ready(self):
        from tutor.signals import user_registration
