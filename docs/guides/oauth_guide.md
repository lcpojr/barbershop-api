# Oauth Guide

To use oauth you will need to create an application config.
You can create in django admin or using the enpoint (Only in develop).

**You will create an user before to create the application**

## Creating a superuser

To create a superuser you will need to do:

- Run the server with `docker-compose up -d`;
- Use `python manage.py create_superuser`;
- Type the data requested;
- Login on django admin;

## Creating by admin

To create an application using admin we should have a superuser account.

- Login on [Django Admin](localhost:8000/admin);
- You can check all applications registered [here](http://localhost:8000/admin/oauth2_provider/application/);
- Create a new application [here](http://localhost:8000/admin/oauth2_provider/application/add/) with client_type `confidencial` and grant_type `password-based`;

## Creating by endpoint

To create an application using admin we should have a superuser account.

- Login on [Django Admin](localhost:8000/admin);
- You can check all applications registered [here](http://localhost:8000/api/v1/auth/applications/);
- Create a new application [here](http://localhost:8000/api/v1/auth/applications/register/) with client_type `confidencial` and grant_type `password-based`;

### Getting the token

You can get a token by doing a request to `/api/v1/auth/token/` with the parameters bellow:

- `client_id` (generated on application creation);
- `client_secret` (generated on application creation);
- `username`;
- `password`;
- `grant_type` (it will be `password`);

**Exemple:**

```sh
curl http://localhost:8000/api/v1/token/ \
-d 'client_id=ijUWruthOfmKyUMxKWM0rzwHhjrJZZYVtjW2kmY2' \
-d 'client_secret=05LXRPpn1jrIY07ZFyFxwev0fOMgqRjyyyuoa6IwrPd71jvA1rnHUdjaw6EtSGU5jmSFU9v6XoZzcdQj3xxf3nV1gHiLIZqMNdRxnkD11zsAqH3UEpq3vUGKOwicg0Fg' \
-d 'username=i3l@admin.com' \
-d 'password=i3ladmin@123' \
-d 'grant_type=password'
```