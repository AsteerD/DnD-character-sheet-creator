# DnD-character-sheet-creator

An application for creating and managing D&D character sheets built with Django.

## Prerequisites

- Python 3.14 installed

## Quick setup (pip)

### Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Database & initial Django setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the app and http://127.0.0.1:8000/admin/ for the admin site.

## Common management commands

- Make migrations: `python manage.py makemigrations` then `python manage.py migrate`
- Open shell: `python manage.py shell`
- Collect static (production): `python manage.py collectstatic`
- Run tests: `python manage.py test`
- Generate ERD diagram: `./manage.py graph_models -a -g -o docs/ERD.png`

## Configuration notes

- Settings are in `DnD_character_sheet_creator/settings.py`. For production change `DEBUG=False` and set a secure `SECRET_KEY` and `ALLOWED_HOSTS`.