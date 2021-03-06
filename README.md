

[![Build Status](https://travis-ci.org/calvinpete/Store-Manager.svg?branch=ch-database-%23161533381)](https://travis-ci.org/calvinpete/Store-Manager)       [![Maintainability](https://api.codeclimate.com/v1/badges/361fe7248d69425bf668/maintainability)](https://codeclimate.com/github/calvinpete/Store-Manager/maintainability)
# Store Manager API Endpoints

The api endpoints enable you to create an admin account, login, register a staff attendant, a product, get a single product, get all products, create a sale record, get a single sale record and get all sale records

## Getting Started

To run the application, make sure you have the following installed on your local machine.

### Prerequisites

```
Git
Python 3.6.3
postgresql
pip3
Virtual Enviroment
```

### Starting the application on Ubuntu

Clone the project by running this in the terminal

```
git clone https://github.com/calvinpete/Store-Manager.git challenge3
```

Activate the virtualenv by running this command in the terminal

```
source venv/bin/activate
```

Install the packages.

```
pip3 install -r requirements.txt
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

### Starting the application on macOS

Clone the project by running this in the terminal

```
git clone https://github.com/calvinpete/Store-Manager.git develop
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
python run.py
```

## Running the tests

Run this command in the terminal

```
python -m unittest -v
```


### Starting the application on Windows

Clone the project by running this in the CMD

```
git clone https://github.com/calvinpete/Store-Manager.git challenge3
```

Activate the virtualenv by running this command in the CMD

```
source bin/activate
```

Install the packages.

```
python -m pip install -r requirements.txt
```

Run the application in the CMD

```
python run.py
```

## Running the tests

Run this command in the CMD

```
python -m unittest -v
```


### Running tests with coverage

You can run tests with coverage by running this command in the terminal

```
nosetests --with-coverage --cover-package=app
```

### Features

|               Endpoint                                        |          Functionality      |
| --------------------------------------------------------------|:---------------------------:|
| POST /auth/login                                              | Login                       |
| POST /auth/signup                                             | Register a staff attendant  |    
| POST /product                                                 | Add a product               |
| GET /product/product_Id                                       | Get a single product        |
| GET /product                                                  | Get all products            |
| POST /sales                                                   | Create a sale record        |
| DELETE /product/product_Id                                    | Delete a product            |
| PUT /product/product_Id                                       | Modify a product            |
| GET /sales/sale_Id                                            | Get a single product        |
| GET /sales                                                    | Get all products            |
| POST /inventory                                               | Restock a product           |






## Deployment

The app is deployed on this [link](https://store-manager17.herokuapp.com/)

## API endpoints

The endpoints can be tested using postman on this [link](https://documenter.getpostman.com/view/4977996/RzZ4pgzB)

## Built With

* [Python 3.6.3](https://www.python.org/) - General Purpose Language
* [Flask](http://flask.pocoo.org/) - Python Micro Web Framework

## Authors

Calvin Tinka

## License
This app is open source hence free to all users
