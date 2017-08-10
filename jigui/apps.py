from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'

class JiguiConfig(AppConfig):
    name = 'jigui'
