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
curl http://localhost:8000/api/v1/auth/token/ \
-d 'client_id=aQ5C3IBulnLjuwCeDtJCNjrHxnBXAX9Z6hZeIpa7' \
-d 'client_secret=UyVZuWRISEnRHCiND8KmGGiSetZsVzHtLlpgi4NqZS8VCbTaVPu4K91UjGfMp7kfusN2yvtQVZCM5Ls53UsG45fuQTs9QPZFzuoW483Gm0dsrkX55KOvMrSwk6NeKu04' \
-d 'username=i3l@admin.com' \
-d 'password=i3ladmin@123' \
-d 'grant_type=password'
```