# AI Based Company Financials Analytics

## What is it?
Personalized company financial analysis tool powered by AI for small/medium size investors.

## What does it solve?
Investing is ambiguous for a novice first-time investor. It is not easy to understand how a company performs by observing its financials. It requires expertise, experience. Other than these it is a time consuming process that not everyone wants to go through. Our aim is to simplify this process by leveraging AI to offer users insight about the companies’ financials.

## How does it solve this problem?
It solves this problem by collecting up to date company financials data and analyzing it with the help of AI and providing summarized information to the investors.

## Design
Link to diagram:
- https://excalidraw.com/#room=17a22f35968e9ea23467,0TqrxEkDf0iF428AnPMB1g
- https://lucid.app/lucidchart/4db4fdce-6c92-4537-bb24-846cfddd6976/edit?viewport_loc=-408%2C-256%2C2725%2C1338%2C0_0&invitationId=inv_2ee27fb9-20d2-45fa-af5f-86dc1c645fea


## How to setup the project?

- make sure that you have python 3.8 or higher installed
- make sure that you have docker installed
- run `docker-compose up --build` to build and run the project
- run the shell using  `docker-compose exec web python manage.py shell_plus`
- run `create_or_update_all()` task on the shell o populate the database with the companies and their financials
- You are good to go!


## Useful commands

- build docker images and start the project: `docker-compose up --build`
- make migrations: `docker-compose exec web python manage.py makemigrations`
- run django migrations: `docker-compose exec web python manage.py migrate`
- access interactive shell in django: `docker-compose exec web python manage.py shell_plus`
- scheduled tasks manager: `celery -A router flower`


## Links to project and tools

- http://localhost:5555 (Celery Flower)
- http://localhost:8000 (Django))
