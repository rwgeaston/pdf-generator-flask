
To run locally, you need recent versions of docker and docker-compose. Run 

    docker-compose up

from root folder. Once it's set up you can either kill this temporarily or go to another window to run

    docker-compose run web python manage.py recreate_db

to make the database table needed.

You can also use ./test.sh to check pylint and unit tests are working. Note that running this the first time will add itself to the git pre-commit hooks, so that one does not forget to run the unit tests before committing :) You need a python3.6 virtualenv + pip install -r local_requirements.txt for this.

To use:

You need an Organization to already exist in db so you can associate reports to it. No API for this at the moment (TODO)

POST to /reports with something like 
    
    {'organization': 1, 'reported': '2018-08-14T20:44:34', inventory: [{'name': 'Item1', 'price': 150}]}

Prices are in integers because I can't get Decimals to work yet and you should not use Floats for money (TODO). Another not great thing is you have to use the id of the organization, not the name. I had name working until I started using marshmallow so need to get that working again (another TODO)

GET /reports will show a list of all submitted reports. Filtering by organization TODO

GET /reports/1 will show the report with ID 1 only.

GET /reports/1?format=xml will return an XML version of report 1 (intentionally only works on the GET detail view, not list view)

DELETE /reports/1 will delete the report with ID 1.

PDFs are TODO, despite the name of the project.

Also TODO is why do I have to keep using [0] every time I serialize a report - it gives me a list of reports (of length 1) rather than just one report dict. Someone who knows flask pls help.


