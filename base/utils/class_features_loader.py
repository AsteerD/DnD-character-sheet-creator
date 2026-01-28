import json
from pathlib import Path
from django.apps import apps as global_apps


def get_data_path():
    """
    Resolves base/data/class_features.json WITHOUT absolute paths.
    Works in migrations and runtime.
    """
    base_app = global_apps.get_app_config("base")
    return Path(base_app.path) / "data" / "class_features.json"


def populate_class_features(apps=None):
    """
    If `apps` is provided -> migration-safe (uses historical models)
    If not -> runtime (uses real models)
    """
    if apps:
        CharacterClass = apps.get_model("base", "CharacterClass")
        Subclass = apps.get_model("base", "Subclass")
        ClassFeature = apps.get_model("base", "ClassFeature")
    else:
        from base.models import CharacterClass, Subclass, ClassFeature

    data_path = get_data_path()

    if not data_path.exists():
        raise FileNotFoundError(f"Missing data file: {data_path}")

    with data_path.open(encoding="utf-8") as f:
        data = json.load(f)

    for class_name, features in data.items():
        try:
            char_class = CharacterClass.objects.get(name=class_name)
        except CharacterClass.DoesNotExist:
            continue

        for feature in features:
            subclass = None
            if "subclass" in feature:
                subclass = Subclass.objects.filter(
                    name=feature["subclass"],
                    character_class=char_class,
                ).first()

            ClassFeature.objects.get_or_create(
                character_class=char_class,
                subclass=subclass,
                name=feature["name"],
                defaults={
                    "description": feature["description"],
                    "unlock_level": feature["unlock_level"],
                },
            )
