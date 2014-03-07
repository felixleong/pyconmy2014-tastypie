# Developing Powerful RESTful APIs with Django Tastypie -- Sample Project and Slides

Presented during [Mini-PyCon Malaysia 2014](http://www.pycon.my/mini-pycon-my-2014).

## Setup The Sample Project

1. Create a virtualenv for the project. If you use virtualenvwrapper, you can
   easily create the new environment with the following command.

    ```bash
    $ mkvirtualenv -p $(which python3) pyconmy-tastypie
    ```

2. Install the requirements.

    ```bash
    $ pip install -r requirements/base.txt
    ```

3. Create and modify blog/settings/local.py according to your own system
   settings.

    ```bash
    $ cd blog/settings/
    $ cp local.example.py local.py
    $ vim local.py
    ```

4. Create the database by executing the following commands.

    ```bash
    $ ./manage.py syncdb
    $ ./manage.py migrate
    ```

5. After the database is created, run the server.

    ```bash
    $ ./manage.py runserver
    ```
