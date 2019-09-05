# Item Catalog

## Project Description
The Item Catalog project consists of developing an application that provides a list of
items within a variety of categories, as well as provide a user registration and authentication system.

## Solution Description
This project is item an catalog of computer components (processors, graphic cards, memories, etc.).

The project use the following libraries:

        flask
        sqlalchemy
        Jinja2

If you have all the libraries in your computer you can start application server via script runserver.sh with the following command```bash runserver.sh```.

If you do not have the all the libraries I recommend to use ```virtualenv```. If your system does not have it you can install it via pip command: ```pip install virtualenv```. Once it is installed you can create new enviroment and run application server there as follows:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r req
    bash runserver.sh
