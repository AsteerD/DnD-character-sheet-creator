from django.db import migrations
from base.utils.class_features_loader import populate_class_features


def forwards(apps, schema_editor):
    populate_class_features(apps=apps)


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_classfeature"),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
