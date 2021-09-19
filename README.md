# lord-of-the-rings
![img.png](img.png)

This project involves arguing about (or learning more) about the Lord of the Rings characters and quotes.

## Table of Contents
- [Requirements](#Requirements)
- [Design Choices](#Design-Choices)
- [Approach](#Approach)
- [Usage](#Usage)
- [API Documentation](#API Documentation)
- [License](License)

##  Requirements
### API Endpoints
- GET /characters => should return all characters from the API
- GET /characters/{id}/quotes => should return all quotes from the specified character
- POST /signup => allow a user to sign up with their username, email, and password
- POST /login => allow a user login in and get a token to make authenticated requests
- POST /characters/{id}/favorites => allows a user favorite a specific character
- POST /characters/{id}/quotes/{id}/favorites => allows a user favorite a specific quote along with its character information
- GET /favorites => should return all authenticated user’s favorited items

### Framework
A python-based web framework (Django or Flask)

### Third-Party Service
https://the-one-api.dev/ to obtain data

## Design Choices

### Framework
Django

### Database
Posgres: it support for a large number of data types like array field

## Approach

The projects consist of 3 apps;
#### core
It contains the models, core tests, migrations, management and admin files.

#### user
It contains the serializer, views, urls and user tests files

#### character
It contains the urls, views and character tests files

## Usage
- clone this repository
 
`$ git clone https://github.com/veekthor04/lord-of-the-rings.git`

`$ cd sample-django-app`

- run the docker compose file

`docker-compose up`

## API Documentation

ReDoc: http://localhost:8000/redoc/

Swagger-ui: http://localhost:8000/swagger/

## License

[MIT © Veekthor04.](../LICENSE)
