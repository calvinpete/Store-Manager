

[![Build Status](https://travis-ci.com/calvinpete/Store-Manager.svg?branch=develop)](https://travis-ci.com/calvinpete/Store-Manager)

# Store Manager API Endpoints

The api endpoints enable you to create an admin account, login, register a staff attendant,create a category, add a product, get a single product, get all products, create a sale record, get a single sale record and get all sale records

## Getting Started

To run the application, make sure you have the following installed on your local machine.

### Prerequisites

```
Git
Python 3.6.3
Flask
JSON Web tokens
Virtual Enviroment
```

### Starting the application

Clone the project by running this in the terminal

```
git clone https://github.com/calvinpete/Store-Manager/tree/develop
```

Activate the virtualenv by running this command in the terminal

```
source venv/bin/activate
```

Install the packages.

```
pip install -r requirements.txt
```

Run the application in the terminal

```
python3 run.py
```

## Running the tests

Run this command in the terminal

```
python3 -m unittest -v
```

### Running tests with coverage

You can run tests with coverage by running this command in the terminal

```
nosetests --with-coverage --cover-package=app
```

### Features

|               Endpoint                                        |          Functionality      |
| --------------------------------------------------------------|:---------------------------:|
| POST /auth/signup                                             | Create an admin account     |
| POST /auth/login                                              | Login                       |
| POST /category                                                | Create a category           |
| POST /category/product                                        | Add a product               |
| POST /auth/register                                           | Register a staff attendant  |
| GET /category/product/product_Id                              | Get a single product        |
| GET /product                                                  | Get all products            |
| POST /sales                                                   | Create a sale record        |
| GET /sales/sale_Id                                            | Get a single product        |
| GET /sales                                                    | Get all products            |



## Deployment

The app is deployed on this [link](https://store-manager17.herokuapp.com/)

## Built With

* [Python 3.6.3](https://www.python.org/) - General Purpose Language
* [Flask](http://flask.pocoo.org/) - Python Micro Web Framework
## Authors

Calvin Tinka

## License
This app is open source hence free to all users
