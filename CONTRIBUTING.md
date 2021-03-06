# Contributing to Minance

## Code of Conduct

The code of conduct is described in `CODE_OF_CONDUCT.md`.

## Our Development Process

All change happen through pull requests. We actively welcome your pull requests and invite you to submit pull requests directly [here](https://github.com/minancenet/web/pulls), and after review, these can be merged into the project.

## Pull Requests

1. Fork the repository and create your branch.
2. If you've added code that should be tested, add some tests.
3. Make sure to describe what your new code or pull request does.

## Local Development

#### Flask

Install Flask:

- **All**: Run `pip install flask` or `pip3 install flask` depending on your systems configuration.

#### SASS/ SCSS

Install SASS:

- **macOS**: Run `brew install sass/sass/sass`.
- **All**: Run `npm install -g sass`.

Starting SASS:

Run `sass --watch minance/static/styles/main.scss minance/static/styles/main.css` from the root project directory.

#### PostgreSQL

Install PostgreSQL:

- **macOS**: Run `brew install postgresql`.
- **Windows**: https://www.postgresqltutorial.com/install-postgresql/
- **Linux**: https://www.postgresqltutorial.com/install-postgresql-linux/

Start PostgreSQL:

- **macOS**: Run `brew services start postgresql`.
- **Windows**: Start PostgreSQL through the control panel or run `net start postgresql-{version}`
- **Linux**: Run `systemctl start postgresql`.

Create a database named `minancedb`:
```
$ psql -U postgres

postgres=# CREATE DATABASE minancedb;
```

### Starting the Development Server

1. Supply `minance/secrets.py` with a valid Hypixel API key.

```
## minance/secrets.py

API_KEY="INSERT_API_KEY_HERE"
```
2. Specify the postgres password in `flask.cfg`.
3. Setup a virtual environment `python -m venv venv` from the root directory and active it `source venv/bin/activate`.
4. Install python requirements via `pip install -r requirements.txt`.
5. Run `python run.py` from the root project directory.
