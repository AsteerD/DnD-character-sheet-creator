import json
import os
from django.core.management.base import BaseCommand
from base.models import Feat

class Command(BaseCommand):
    help = 'Imports feats from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing the feats.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        # Sprawdzamy czy plik istnieje
        if not os.path.exists(json_file_path):
             self.stdout.write(self.style.ERROR(f'File not found at: {json_file_path}'))
             return

        try:
            with open(json_file_path, 'r', encoding='utf-8-sig') as f:
                feats_data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading JSON: {e}'))
            return

        count_created = 0
        count_updated = 0

        for feat_item in feats_data:
            # Używamy get() dla description i prerequisite, żeby uniknąć błędów jak ich brakuje w JSON
            feat, created = Feat.objects.update_or_create(
                name=feat_item['name'],
                defaults={
                    'description': feat_item.get('description', ''),
                    'prerequisite': feat_item.get('prerequisite'),
                }
            )

            if created:
                count_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created feat: {feat.name}'))
            else:
                count_updated += 1
                
        self.stdout.write(self.style.SUCCESS(f'Feat import complete. Created: {count_created}, Updated: {count_updated}'))