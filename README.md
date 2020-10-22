# Wallet API Demo
This is a demo project that shows a simple implementation of a RESTful API 
written in Python using Flask.

By the very nature of being a demo, there are some limitations that would need 
to be addressed before it could be used in a production system:

 - Uses SQLite as the backend database, this won't scale.
 - HTTP Basic Authentication, adequate to demonstrate how the API can be authenticated
   but not secure, especially so if not run over HTTPS!
 - Ideally the database operations would be abstracted away, possibly through an
   ORM layer such as SQLAlchemy. This would make it easier to switch back end 
   database engines and servers. 
 
## Design Choices

### Currency Database Type

For simplicity currency is represented in this demo using Integer types. This is
to avoid the issues with storing currency as floating point types and because 
SQLite does not have a suitable Decimal type. 

### Documentation
The documentation for the API is provided online by the server itself at: 
/wallet/documentation
This uses OpenAPI and the Swagger interface to provide an interactive set of 
documentation that can be used to try out the API.

### Logging   
Logging uses the Flask logger (which is in turn the default Python logger). 
The Python logger is highly configurable and logs to stdout/stderr can easily be
hovered up by log collection services on cloud providers.

# Developing The API
For all the example commands below the current working directory is assumed to 
be the top level project directory.

## Configuring a Development Environment (Windows)

```
python -m venv ven
.\venv\Scripts\activate 
pip install -r requirements.txt -r requirements-dev.txt
```

## Configuring a Production Environment (Windows)
N.B. This is an example only, for a real production environment I'd suggest you 
pin the requirements to specific versions.
```
python -m venv ven
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests
The tests use the py.test framework and can be run as so:
```
python -m pytest -s tests
```

## Running The Server Locally

Before running for the first time you will need to initialise the database:
```
run-dev.bat init-db
```

Subsequently the server can be run using:
```
run-dev.bat run
``` 
Visit [http://localhost:5000/wallet/documentation](http://localhost:5000/wallet/documentation) to they try out or test the API
manually.

For testing purposes there are tools to add a user:

```
python .\tools\adduser.py --database .\instance\wallet.sqlite --username devuser --balance 100
```

## Building and Running using Docker
Build the docker image with:
```
docker build . --tag walletapi:1.0
```

Run a server using:
```
docker run -p 80:5000 --detach --name api walletapi:1.0
```

Visit the documentation on [http://127.0.0.1/wallet/documentation](http://127.0.0.1/wallet/documentation) 
to try it out. For initial experimentation there is a user configured, u: john p: test

