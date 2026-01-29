import json
import os
from django.db import migrations
from django.conf import settings

def populate_feats(apps, schema_editor):
    Feat = apps.get_model('base', 'Feat')

    file_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'feats.json')

    if not os.path.exists(file_path):
        print(f"WARNING: File {file_path} not found. Feats not populated.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        feats_data = json.load(file)

    count = 0
    for feat in feats_data:
        Feat.objects.get_or_create(
            name=feat.get('name'), 
            defaults={
                'description': feat.get('description', ''),
            }
        )
        count += 1
    
    print(f"Successfully loaded {count} feats from JSON.")

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_feat_character_feats'), 
    ]

    operations = [
        migrations.RunPython(populate_feats),
    ]