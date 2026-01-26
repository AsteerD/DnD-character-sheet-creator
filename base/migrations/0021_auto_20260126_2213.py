import json
import os
from django.conf import settings
from django.db import migrations

def load_feats_from_json(apps, schema_editor):
    Feat = apps.get_model('base', 'Feat')
    
    # This constructs the path: .../your_project/base/data/feats.json
    file_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'feats.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            feats_data = json.load(file)
            
            for item in feats_data:
                Feat.objects.update_or_create(
                    name=item['name'],
                    defaults={
                        'description': item['description'],
                        'prerequisite': item['prerequisite']
                    }
                )
        print(f"\nSuccessfully loaded {len(feats_data)} feats from {file_path}")
        
    except FileNotFoundError:
        print(f"\nError: Could not find file at {file_path}")

class Migration(migrations.Migration):

    dependencies = [
        # MAKE SURE THIS MATCHES YOUR LAST MIGRATION FILE
        ('base', '0020_auto_20260126_2135'), 
    ]

    operations = [
        migrations.RunPython(load_feats_from_json),
    ]