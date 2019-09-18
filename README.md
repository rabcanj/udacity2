# Item Catalog

## Project Description
This project is an catalog of computer components (processors, graphic cards, memories, etc.).

### How to run Project
1. vagrant up
1. vagrant ssh
1. Install requirements:
   1. flask
   1. sqlalchemy
   1. Jinja2
   1. flask_oauthlib

   Virtualenv can be used in a following way (not mandatory):


         #run this command only once
         virtualenv -p python3 venv
         source venv/bin/activate
         #run this command only once
         pip install -r requirements.txt

4. cd /vagrant/catalog
1. Clone the following git repo: https://github.com/rabcanj/udacity2
1. source runserver.sh

Project should be running on url: https://localhost:8000/index. HTTPS protocol must be used because of  facebook authentication, which is used in this project. Current version of facebook authentication require https.

Main part of the project:

   1. Templates: stored in project/templates. HTML language is generated from them.
   1. controlers.py: stored in project/controlers.py, main apis are here
   1. fboauth.py: stored in project/fboauth.py, taking care of authentication
   1. models.py:  stored in project/models.py, contains classes from which database structure is created

### Special endpoints and features

In menu you can find button Create/reset databse. It removes all the data from the database and creates some initial data. This feature does not require authentication, it was created only because of comfortable testing.

https://localhost:8000/json_data returns categories and its items in json structure.
