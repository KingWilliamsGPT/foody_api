# Foody API


### Installation

install requirements file

```pip install requirements.txt -r```

### Configure DB

#### MySql
You should see a line like this in <a href="./foody_api/settings.py">./foody_api/settings.py</a>

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foody',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Set your MySQL server host
        'PORT': '3306',        # Set your MySQL server port
    }
}

```
create and set NAME="your_database_name"
set USER and PASSWORD accordingly

#### Sqlite
Or a simpler alternative is to use my sql comment the above lines and add or replace it
with the following
```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

```

### Create Super User
```bash
python manage.py createsuperuser
```

### Start Server
then run ```python3 manage.py runserver 5000``` to start the server on port 5000, your address should be at http://localhost:5000


### Login to admin
You will need to login to the admin panel to have full access to some api endpoints. Login here http://localhost:5000/admin/

### More
check `somefile.md` for list of supported urls.