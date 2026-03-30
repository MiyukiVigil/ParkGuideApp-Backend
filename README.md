# Park Guide App Backend

Django REST backend for the Park Guide App training platform. This service handles authentication, training content, learner progress, badges, notifications, and secure file delivery.

## Stack
- Django 6
- Django REST Framework
- JWT auth with `djangorestframework-simplejwt`
- Neon Postgres via `DATABASE_URL`
- Firebase Storage for secure file uploads and signed downloads
- Custom user model: `accounts.CustomUser`

## Features
- Email-based registration and login
- Training courses and modules API
- Module completion and course progress tracking
- Badge progress and awarded badge endpoints
- In-app notifications with read/clear actions
- Secure file upload, download, and temporary signed URLs using Firebase Storage
- Django admin for courses, badges, notifications, users, and files

## Environment Variables
Create a `.env` file in the project root.

Required:

```env
SECRET_KEY=replace-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://<user>:<password>@<host>/<db>?sslmode=require
FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
FIREBASE_SERVICE_ACCOUNT_PATH=path/to/firebase-service-account.json
```

Optional:

```env
JWT_SIGNING_KEY=replace-me-if-you-want-a-separate-jwt-key
```

Notes:
- `DATABASE_URL` is the main database connection string. This is where your Neon connection string goes.
- `ssl_require=True` is enabled in Django settings, so your Postgres connection must support SSL.
- `FIREBASE_SERVICE_ACCOUNT_PATH` is resolved relative to the project root in `park_guide/settings.py`. A value like `secrets/firebase-admin.json` works well.
- Keep the Firebase bucket name clean, without `gs://`.

## Local Setup
1. Create a virtual environment and activate it.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install Django djangorestframework djangorestframework-simplejwt psycopg2-binary dj-database-url python-dotenv firebase-admin
```

3. Create `.env` from the example file and fill in your Neon and Firebase values.

```bash
cp .env.example .env
```

4. Run migrations.

```bash
python manage.py migrate
```

5. Load the bundled training data.

```bash
python manage.py load_training_courses
```

6. Create an admin user.

```bash
python manage.py createsuperuser
```

7. Verify Firebase Storage access.

```bash
python manage.py bootstrap_private_bucket
```

8. Optionally seed demo badges.

```bash
python manage.py seed_demo_badges
```

9. Start the server.

```bash
python manage.py runserver
```

Default local URL:
- `http://127.0.0.1:8000`

If you are testing from a physical Android device through a local dev build:

```bash
adb reverse tcp:8000 tcp:8000
```

## Neon Database
This backend now expects a Postgres connection string through `DATABASE_URL`, which makes Neon the easiest deployment target.

Example format:

```env
DATABASE_URL=postgresql://username:password@ep-example.ap-southeast-1.aws.neon.tech/dbname?sslmode=require
```

If the database is brand new, run:

```bash
python manage.py migrate
python manage.py load_training_courses
python manage.py seed_demo_badges
```

## Firebase Storage
Secure file uploads are stored in Firebase Storage.

What you need:
- A Firebase project
- A Storage bucket
- A service account JSON file with Storage access
- Matching values for `FIREBASE_STORAGE_BUCKET` and `FIREBASE_SERVICE_ACCOUNT_PATH`

Quick check:

```bash
python manage.py bootstrap_private_bucket
```

If configured correctly, the command confirms that the bucket is accessible.

## API Overview
Base routes:
- `/api/`
- `/api/accounts/`
- `/api/notifications/`
- `/api/user-progress/`
- `/api/secure-files/`

Authentication:
- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `POST /api/accounts/token/refresh/`

Training:
- `GET /api/courses/`
- `GET /api/modules/`
- `GET /api/progress/`
- `POST /api/progress/`
- `GET /api/course-progress/`
- `POST /api/course-progress/`
- `POST /api/complete-module/`

Badges:
- `GET /api/user-progress/badges/`
- `GET /api/user-progress/my-badges/`

Notifications:
- `GET /api/notifications/items/`
- `POST /api/notifications/items/{id}/mark-read/`
- `POST /api/notifications/items/mark-all-read/`
- `POST /api/notifications/items/clear-read/`

Secure files:
- `GET /api/secure-files/files/`
- `POST /api/secure-files/files/` with multipart field `file`
- `GET /api/secure-files/files/{id}/`
- `DELETE /api/secure-files/files/{id}/`
- `GET /api/secure-files/files/{id}/download-url/`
- `GET /api/secure-files/files/{id}/download/`

All API endpoints require `Authorization: Bearer <access_token>` unless noted otherwise.

## Admin
Admin URL:
- `/admin/`

Main admin areas include:
- Accounts
- Courses and modules
- User progress
- Badges and awarded badges
- Notifications
- Secure files

Notification send flow:
1. Create a notification in Django admin.
2. Select it in the changelist.
3. Run the action to send it to users.

## Useful Commands
```bash
python manage.py migrate
python manage.py load_training_courses
python manage.py seed_demo_badges
python manage.py bootstrap_private_bucket
python manage.py createsuperuser
python manage.py runserver
```

## Project Notes
- Default REST permissions require authentication globally.
- JWT uses `SECRET_KEY` unless `JWT_SIGNING_KEY` is provided.
- The database falls back to local SQLite only if `DATABASE_URL` is missing, but for this project you should treat Neon/Postgres as the real target setup.
- Firebase file paths are stored in the `SecureFile.s3_key` field for legacy compatibility.
