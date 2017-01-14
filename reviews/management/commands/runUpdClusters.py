from django.core.management.base import BaseCommand, CommandError
from reviews.suggestions import update_clusters

class Command(BaseCommand):
    def handle(self, **options):
        update_clusters()