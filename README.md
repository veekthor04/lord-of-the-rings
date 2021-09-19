# lord-of-the-rings
![img.png](img.png)

This project involves arguing about (or learning more) about the Lord of the Rings characters and quotes.

## Table of Contents
- [Requirements](#Requirements)
- [Design Choices](#Design-Choices)
- [Project Setup](#Project-Setup)
- [Usage](#Usage)
- [API Documentation](#API-Documentation)
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

It is fast and easy to set up. It offers in-built authentication system for fast set-up, it allows end-to-end testing.It has Django REST Framework which helps to build powerful APIs. 

### Database
Postgres

The speed and stability is quite impressive compared to other SQL databases. It has support for a large number of data types like array field.


### Tools
Docker

This makes it easy create ready-to-run containerised applications. it makes the transition from development to production much easier.

Swagger

This makes it easy to automate documentation from code and test RESTful APIs/ 

## Project Setup

The project consist of 3 apps;
#### core
The core app has the models, migrations and management logic. It contains the models, core tests, migrations, management and admin files.

#### user
The user app has all the users and authentication logic. It contains the serializer, views, urls and user tests files

#### character
The character app has all the logic for the characters and quote endpoints. It contains the urls, views and character tests files

## Usage
- clone this repository
 
`$ git clone https://github.com/veekthor04/lord-of-the-rings.git`

`$ cd lord-of-the-rings`

- run the docker compose file

`docker-compose up`

## API Documentation

ReDoc: http://localhost:8000/redoc/

Swagger-ui: http://localhost:8000/swagger/

## License

[MIT © Veekthor04.](./LICENSE)
