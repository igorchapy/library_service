# REST_practice

How to run it locally
git clone https://github.com/igorchapy/REST_project1.git
cd REST_project1
python -m venv venv
# Activate venv:
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate       # Apply migrations to setup DB schema
python manage.py runserver     # Start the development server
