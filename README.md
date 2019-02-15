# Hubs Devices Sensors

### Requirements:  
  Python (with pip) >= 3.7  
  MongoDB - latest stable release
  
### How to launch:
  1. ```pip install -r requirements.txt``` - to install all required libraries
  2. ```python manage.py migrate``` - to create database and collections
  3. ```python manage.py createsuperuser``` and follow instructions. This ables to create superadmin user
  4. ```python manage.py runserver``` - to run server
  5. Follow http://127.0.0.1:8000/ and authorize using superadmin credentials to check API Docs
