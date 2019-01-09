# Oauth Guide

To use oauth you will need to create an application config.
You can create in django admin or using the enpoint (Only in develop).

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
-d 'client_id=PtHjmOspcoqCBgUIU6iGATLrqEvlDlSgfmuC8GIM' \
-d 'client_secret=2pB7gmg6LqKSswBZzx2126V4qNT6dysIIbA7qkdRTFFbvs7ZSw26HbmM5ZZnDRFo8wGxssEWRXPYbFU1bItUvLJx2gVU5ShWyqlZVKZ2amxIBGH1ajCJvy25oVbP0iDM' \
-d 'username=i3l' \
-d 'password=admini3l' \
-d 'grant_type=password'
```