# Blogging Platform With Django Rest Framework

## Installation
After cloning the repository, create a virtual environment to have a clean python installation.

You can do this by running the command
```
python -m venv env
```

### Activate the virtual environment

To activate on Windows:
```
env\Scripts\activate
```
To activate on MacOS and Linux:
```
source env/bin/activate
```

## Requirements

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Configure Environment variables
Update the `.env` file in the root directory of the project with the necessary database configurations.

## Use

1. Apply Migrations:
```
python manage.py migrate
```
2. Run Django's development server:
```
python manage.py runserver
```
3. If you've made changes to your models and need to create migrations (not just apply them), you should use the makemigrations command. Here’s how:
```
python manage.py makemigrations
```

### Additional notes:
Here is the complete sequence:
1. Create Migrations (if you've made changes to models):
```
python manage.py makemigrations
```
2. Apply Migrations:
```
python manage.py migrate
```
3. Run the Server:
```
python manage.py runserver
```

## Running with Docker
This project can be run using Docker and Docker Compose. Follow these steps to get it up and running:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Before running the application, make sure all necessary environment variables are set. You can use the same .env file you configured for local development, or you can specify environment variables directly in the Docker Compose file. Here's how you might want to set up your .env file for Docker:
```
DB_NAME=<your_db_name>
DB_USER=<your_username>
DB_PASSWORD=<your_password>
DB_PORT=5432
DB_HOST=db  # This should match the service name of your database in docker-compose.yml
```
For this project you can comment out the DB_HOST from the .env file to run the project using Docker.

3. Build the Docker images:
```
docker-compose build
```

4. Start the containers:
```
docker-compose up
```
This will start the PostgreSQL database and the Django application containers.

5. Once the containers are up and running, you can access the API at `http://localhost:8000/api/v1/`.

6. To stop the containers, use the following command:
```
docker-compose down
```

7. The Docker Compose configuration will mount the project directory as a volume in the Django container, so any changes made to the code will be reflected immediately without the need to rebuild the image.

Note: If you encounter any issues related to the database connection, make sure the Django migrations have been applied by running the following command inside the Django container:
```
docker-compose run --rm web python manage.py migrate
```

This will apply any pending Django migrations and ensure the database is set up correctly.

## API Endpoints
We will use the following URLS - `/blogs/` and `/blogs/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`blogs`| POST | CREATE | Create a new blog
`blogs` | GET | READ | Get all blogs
`blogs/:id` | GET | READ | Get a single blog by its id
`blogs/:id` | PUT | UPDATE | Full Update a blog
`blogs/:id` | PATCH | UPDATE | Partially Update a blog
`blogs/:id` | DELETE | DELETE | Delete a blog


Only authenticated users can use the API services, for that reason if we try this:
```
http GET http://127.0.0.1:8000/api/v1/blogs/
```
we get:
```
{
    "detail": "Authentication credentials were not provided."
}
```
Instead, if we try to access with credentials:
```
http GET http://127.0.0.1:8000/api/v1/blogs/1 "Authorization: Bearer your_token"
```
we get the blog with id = 1
```
{
    "id": 1,
    "title": "blog title 1",
    "content": "blog content 1",
    "created_at": "2024-04-22T19:28:31.963812Z",
    "updated_at": "2024-04-22T19:28:31.963875Z",
    "author": "utkarshagupte",
    "tags": [],
    "category": null
}
```

## Create users and Tokens

First we need to create a user, so we can log in
```
http POST http://127.0.0.1:8000/api/v1/auth/register/ 
{
    "username": "your_username",
    "email": "your_email",
    "first_name": "your_first_name",
    "last_name": "your_second_name",
    "password": "your_password",
    "password2": "your_password"
}
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http POST http://127.0.0.1:8000/api/v1/auth/token/ 
{
    "username": "your_username",
    "password": "your_password"
}
```
after that, we get the token
```
{
    "refresh": "your_refresh_token",
    "access": "your_accesss_token"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a new access token.

To request new access token
```
http POST http://127.0.0.1:8000/api/v1/auth/token/refresh/
{
    "refresh": "your_refresh_token"
}
```
and we will get a new access token
```
{
    "access": "your_new_access_token"
}
```

We have kept below considerations while designing and implementing the APIs:
-   The blogs are always associated with an author (user who created it).
-   Only authenticated users may create and see blogs.
-   Only the author of a blog may update or delete it.
-   The API doesn't allow unauthenticated requests.

### Commands

1. Create a new blog
```
http POST http://127.0.0.1:8000/api/v1/blogs/ 
"Authorization: Bearer {YOUR_TOKEN}" 

{
  "title": "Open Source LLM Models",
  "content": "Open Source LLM Models",
  "category": 2,
  "tags": [1,2]
}
```

2. Get all blogs
```
http GET http://127.0.0.1:8000/api/v1/blogs/ 
"Authorization: Bearer {YOUR_TOKEN}" 
```

3. Get a single blog by its ID
```
http GET http://127.0.0.1:8000/api/v1/blogs/{blogs_id}/ 
"Authorization: Bearer {YOUR_TOKEN}" 
```

4. Full update a blog
```
http PUT http://127.0.0.1:8000/api/v1/blogs/{blogs_id}/ 
"Authorization: Bearer {YOUR_TOKEN}" 
{
  "title": "New - Open Source LLM Models",
  "content": "New - Open Source LLM Models",
  "category": 1,
  "tags": [1,2,3]
}
```

5. Partial update a blog
```
http PATCH http://127.0.0.1:8000/api/v1/blogs/{blog_id}/ 
"Authorization: Bearer {YOUR_TOKEN}" 
{
  "title": "New - Open Source LLM Models - New",
}
```

6. Delete a blog
```
http DELETE http://127.0.0.1:8000/api/v1/blogs/{blog_id}/ 
"Authorization: Bearer {YOUR_TOKEN}"
```

### Filters

The API supports filtering, you can filter by the attributes of a blog like this
```
# Filter by title
http http://127.0.0.1:8000/api/v1/blogs/?title="My First Blog"
"Authorization: Bearer {YOUR_TOKEN}"

http://127.0.0.1:8000/api/v1/blogs/?author="author_name"
 "Authorization: Bearer {YOUR_TOKEN}"
```

You can also combine multiples filters like so
```
http://127.0.0.1:8000/api/v1/blogs/?author="author_name"&title="title"
"Authorization: Bearer {YOUR_TOKEN}"
```

### Pagination

The API supports pagination, by default responses have a page_size=10 but if you want change that you can pass through params page_size={your_page_size_number}
```
http http://127.0.0.1:8000/api/v1/blogs/?page=3&page_size=15 "Authorization: Bearer {YOUR_TOKEN}"
```

