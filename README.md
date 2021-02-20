# FRBEC
To get the project running please follow the below steps. I assume the project is being run in a linux machine. If it is run on windows machine steps for creating virtual environment and activating it will differ a little bit. Please note I assume you have python and pip installed by default in the machine, if not please do install before starting.

1. Go to the root directory of the project and create a virtual env by following the below steps

**VirtulaEnvironment**
> python -m venv ./venv

Once the virtual env is created, activate it using the following command
> source venv/bin/activate

Now we need to install the requirements.txt which can be found inside frbec folder. To install run the following
> pip install -r requirements.txt

Once the requirements are installed we need to get the project running, please follow the below commands inside frbec folder/ or where the manage.py file exist
> python manage.py migrate

> python manage.py makemigrations points

> python manage.py migrate --run-syncdb

> python manage.py createsuperuser

Once the above command is run, we can create super user for the db which can be accessed using the following url
> http://localhost:8000/admin/

The above url is called django admin where we can create dummy records and view the existing data also.

Next step will be to get the server running
> python manage.py runserver

Testing

To create dummy records for testing, either we can use postman or curl commands. The urls are defined as follows
> POST - Add Transaction - http://localhost:8000/add-transaction/ (Sample post body - {"payer": "UNILEVER", "points": 3000})

> GET - Get all available points - http://localhost:8000/all-points/

> POST - Spend points - http://localhost:8000/spend-points/ (Sample post body - {"points": 5000})

I have included few basic unit tests to ensure the api is working correctly. To run tests please run the following command
> python manage.py test

Next step would be to containerize the application using docker.
