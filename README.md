# Knowledge-Share

[Knowledge-Share](https://www.knowledge-shared.com) is a web app whose focus is to help people build up and share a collection of knowledge in the form of a knowledgebase. Users write and version articles into folders, share articles into each other's knowledgebases, follow other users, message each other, and browse a feed of published articles across the site.

### Built With

 * [Django](https://www.djangoproject.com/)
 * [django-rest-framework](https://www.django-rest-framework.org/)
 * [Bootstrap](https://getbootstrap.com/)
 * PostgreSQL (with the `pg_trgm` extension for trigram similarity search)

## Architecture

Knowledge-Share is a single Django project organized into five apps —
`users`, `knowledgebase`, `social`, `articlefeed`, and `utils` — rendered
server-side with Django templates, plus a Django REST Framework API surface
under `social/api` and `articlefeed/api` for the interactive widgets
(follow/unfollow, messaging, notifications, the article feed). See the
[`docs/`](docs/) folder for the full picture:

* [`docs/architecture.md`](docs/architecture.md) — system overview, app
  dependency graph, request flow, auth/error-handling/logging conventions.
* [`docs/data-model.md`](docs/data-model.md) — every model, its fields, and
  an entity-relationship diagram.
* [`docs/api-reference.md`](docs/api-reference.md) — every REST endpoint,
  its auth requirements, and request/response shapes.
* [`docs/environment.md`](docs/environment.md) — every environment variable
  the app reads, by settings module (dev/prod/CI).

## Local Setup

1. **Install dependencies** (Python 3.9+ recommended, matching CI):

   ```bash
   pip install -r requirements.txt
   ```

2. **Provide a Postgres database.** Create a database and a user that can
   create the `pg_trgm` extension (the `knowledgebase` app's full-text
   search depends on it — see
   [`KnowledgeShare/knowledgebase/migrations/0012_pg_trgm_extension.py`](KnowledgeShare/knowledgebase/migrations/0012_pg_trgm_extension.py)).

3. **Configure environment variables.** Local development
   (`config.settings.dev`, the default) reads secrets from a `dev_env.json`
   file at the repo root rather than real environment variables. Use
   [`.env.example`](.env.example) as a reference for which values you need,
   then see [`docs/environment.md`](docs/environment.md) for the exact
   `dev_env.json` key names and a worked example (the dev key names differ
   from the production environment variable names in `.env.example`).

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the dev server:**

   ```bash
   python manage.py runserver
   ```

6. **Run the test suite:**

   ```bash
   python manage.py test
   ```

   CI (`.github/workflows/django.yml`) additionally lints with `flake8` and
   runs `coverage run manage.py test` against `config.settings.ci_testing`.

## Authors

Contributors names.
* [Doug Mumme](https://github.com/dpmumme12)

## Version History

* 0.1
    * Initial Release
