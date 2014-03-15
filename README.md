# Developing Powerful RESTful APIs with Django Tastypie -- Sample Project and Slides

Presented during [Mini-PyCon Malaysia 2014](http://www.pycon.my/mini-pycon-my-2014).

## Preamble

Slides are contained in /slides/build/slides/index.html.

If you prefer to read them in one page, you can check out the HTML page instead
under /slides/build/html/index.html.

All live demo code are stored under a iPython Notebook, just execute the
following command:

```bash
# If you haven't installed the dependencies, make sure you are doing it under
# a virtualenv.
$ pip install -r requirements/ipynb.txt
$ cd slides
$ ipython3 notepad
```

Expect bugs in the sample code as I didn't have unit tests coded, bug reports
are always welcomed! :)

## Setup The Sample Project -- from scratch

1. Create a virtualenv for the project. If you use virtualenvwrapper, you can
   easily create the new environment with the following command.

    ```bash
    $ mkvirtualenv -p $(which python3) pyconmy-tastypie
    ```

2. Install the requirements.

    ```bash
    $ pip install -r requirements/base.txt
    ```

3. If you are OK to use the test data, you can just kick off the application
   straight away.

    ```bash
    $ ./manage.py runserver_plus
    ```

4. The Django admin login for the superuser is as follows.

    - user: admin
    - password: abc123

## To Customize Your Build

You know, if you want to adapt it for your own use :)


1. Create and modify blog/settings/local.py according to your own system
   settings.

    ```bash
    $ cd blog/settings/
    $ vim local.py
    ```

2. If you changed the database settings and want to create a fresh database by
   executing the following commands.

    ```bash
    $ ./manage.py syncdb
    $ ./manage.py migrate
    ```
