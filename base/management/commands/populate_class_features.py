from django.core.management.base import BaseCommand
from base.utils.class_features_loader import populate_class_features


class Command(BaseCommand):
    help = "Populate class features from JSON data file"

    def handle(self, *args, **options):
        populate_class_features()
        self.stdout.write(
            self.style.SUCCESS("Class features populated successfully.")
        )
