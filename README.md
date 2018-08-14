
To run locally, you need recent versions of docker and docker-compose. Run 

    docker-compose up

from root folder. Once it's set up you can either kill this temporarily or go to another window to run

    docker-compose run web python manage.py recreate_db

to make the database table needed.

You can also use ./test.sh to check pylint and unit tests are working. Note that running this the first time will add itself to the git pre-commit hooks, so that one does not forget to run the unit tests before committing :) You need a python3.6 virtualenv + pip install -r local_requirements.txt for this.

WIP there's no actual PDFs yet!