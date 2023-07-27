# WarezArena

WarezArena is a website dedicated to following cracks fro games.

## Installation

Download the repository from here using the git clone method.

Make sure you have pip3 installed on your machine and have a running MySQL client. 

Replace the values: 
DB_NAME, USER_NAME,USER_PASSWORD with the right credentials for your database, in the following part in the settings.py file:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'DB_NAME',  # <-- change this
        'USER': 'USER_NAME',  # <-- change this
        'PASSWORD': 'USER_PASSWORD', # <-- change this
        'OPTIONS': {
            'read_default_file': '/path/to/my.cnf',
        },
    }
}
```
Create a virtual environment, activate it, and use the command:

```bash
pip3 install -r requirements.txt
```
to install all of the required libraries.

## Usage

```bash
python3 manage.py runserver
```
You will get a link to the address of the site. Default for localhost is [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## License

[MIT](https://choosealicense.com/licenses/mit/)
