# Environment Configuration

Knowledge-Share selects its Django settings module via the
`DJANGO_SETTINGS_MODULE` environment variable (defaulted to
`config.settings.dev` by `manage.py` when unset). There are three settings
modules, each with a **different** mechanism for sourcing secrets:

| Settings module | Used for | Secret source |
|---|---|---|
| `config.settings.dev` | Local development | A local `dev_env.json` file (JSON), read via `get_env_var(...)` in `config/settings/dev.py`. **Not committed to git.** |
| `config.settings.prd` | Production | Real OS environment variables, read via `os.environ[...]` in `config/settings/prd.py`. |
| `config.settings.ci_testing` | CI (`.github/workflows/django.yml`) | Hardcoded test values in-file; no secrets required. |

Both `dev` and `prd` load `config/settings/base.py` first via `from .base import *`.

## Local development setup

1. Create a `dev_env.json` file at the repository root (same directory as
   `manage.py`). It must be valid JSON with the keys listed in the **Dev
   variables** table below.
2. Run `export DJANGO_SETTINGS_MODULE=config.settings.dev` (or rely on the
   `manage.py` default) and start the app normally — see the root `README.md`
   setup section.

`dev_env.json` is read as a flat JSON object, e.g.:

```json
{
  "Postgres_Database_NAME": "knowledgeshare",
  "Postgres_USER": "postgres",
  "Postgres_PASSWORD": "postgres",
  "Postgres_HOST": "localhost",
  "EMAIL_HOST_USER": "you@example.com",
  "EMAIL_HOST_PASSWORD": "app-password",
  "DEFAULT_TO_EMAIL": "you@example.com",
  "LOG_LEVEL": "DEBUG"
}
```

### Dev variables (`dev_env.json` keys)

| Key | Consumed by | Purpose |
|---|---|---|
| `Postgres_Database_NAME` | `DATABASES['default']['NAME']` | Postgres database name |
| `Postgres_USER` | `DATABASES['default']['USER']` | Postgres user |
| `Postgres_PASSWORD` | `DATABASES['default']['PASSWORD']` | Postgres password |
| `Postgres_HOST` | `DATABASES['default']['HOST']` | Postgres host (port is fixed at `5432`) |
| `EMAIL_HOST_USER` | `EMAIL_HOST_USER`, `DEFAULT_FROM_EMAIL` | SMTP (Gmail) account used to send mail |
| `EMAIL_HOST_PASSWORD` | `EMAIL_HOST_PASSWORD` | SMTP app password |
| `DEFAULT_TO_EMAIL` | `DEFAULT_TO_EMAIL` | Fallback "to" address for outbound mail |
| `LOG_LEVEL` | the `django` file logger's level | e.g. `DEBUG`, `INFO`, `WARNING` |

Note the inconsistent casing (`Postgres_*` vs `EMAIL_*`/`LOG_LEVEL`) is
intentional to document — it reflects the key names Django actually looks up
via `get_env_var(...)` in `config/settings/dev.py`; `dev_env.json` keys must
match exactly.

Media uploads in dev are stored on local disk (`MEDIA_ROOT`); Cloudinary is
**not** used by `config.settings.dev`.

## Production setup (`config.settings.prd`)

Production reads real process environment variables (`os.environ[...]`) —
set these on the hosting platform (e.g. Heroku config vars, since the project
ships a `Procfile`).

### Production variables (real env vars)

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django's `SECRET_KEY` |
| `DATABASE_NAME` | Postgres database name |
| `DATABASE_USER` | Postgres user |
| `DATABASE_PASSWORD` | Postgres password |
| `DATABASE_HOST` | Postgres host (port fixed at `5432`) |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name for media storage |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `EMAIL_HOST_USER` | SMTP (Gmail) account used to send mail; also `SERVER_EMAIL` and `DEFAULT_FROM_EMAIL` |
| `EMAIL_HOST_PASSWORD` | SMTP app password |
| `DEFAULT_TO_EMAIL` | Fallback "to" address for outbound mail |
| `LOG_LEVEL` | the `django` file logger's level |

> **`CLOUDINARY_*` naming**: these three variables were previously mistyped
> as `ClOUDINARY_CLOUD_NAME` / `ClOUDINARY_API_KEY` / `ClOUDINARY_API_SECRET`
> (lowercase `l` instead of uppercase `L`) in `config/settings/prd.py`. The
> config-settings-fixes unit corrected the code to read the properly-cased
> `CLOUDINARY_*` names documented above — see
> [[contract-cloudinary-env-names]]. Set the environment variable with the
> **corrected** casing shown in this table; the old mistyped name is no
> longer read anywhere in the codebase.

`config.settings.prd` also hardcodes `ALLOWED_HOSTS` to
`['knowledge-shared.com', 'www.knowledge-shared.com']` and enables
`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and `SECURE_SSL_REDIRECT` —
these are not environment-configurable.

## CI setup (`config.settings.ci_testing`)

No secrets required. `DJANGO_SETTINGS_MODULE=config.settings.ci_testing` is
set directly in `.github/workflows/django.yml`; database credentials
(`postgres`/`postgres`/`localhost`) match the workflow's Postgres service
container and are hardcoded in the settings file, not read from the
environment.

## `.env.example`

A root-level [`.env.example`](../.env.example) enumerates the **production**
variable set (the real-env-var style, since that's the convention `.env`
files follow) with placeholder values. For local development, copy the
variable names/values you need into `dev_env.json` using the **dev key names**
from the table above (they do not match the production variable names
one-for-one — e.g. `DATABASE_NAME` in prod vs `Postgres_Database_NAME` in dev).
