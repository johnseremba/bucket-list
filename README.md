## THE BUCKET LIST ##

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9eb767981d1445b2899f8df277ec9a92)](https://www.codacy.com/app/SerryJohns/bucket-list?utm_source=github.com&utm_medium=referral&utm_content=SerryJohns/bucket-list&utm_campaign=badger)
[![Build Status](https://travis-ci.org/SerryJohns/bucket-list.svg?branch=master)](https://travis-ci.org/SerryJohns/bucket-list)
[![Coverage Status](https://coveralls.io/repos/github/SerryJohns/bucket-list/badge.svg?branch=master)](https://coveralls.io/github/SerryJohns/bucket-list?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Bucket list application organizes for you the tasks that you hope to do before you die, and helps you keep track of your life goals.

>Staging url: https://johnzbucketlist-staging.herokuapp.com/
>Production url: https://johnzbucketlist-pro.herokuapp.com/

## Installation
 
Clone the GitHub repo:
 
http:
>`$ git clone https://github.com/SerryJohns/bucket-list.git`

cd into the folder and install a [virtual environment](https://virtualenv.pypa.io/en/stable/)

`$ virtualenv --python=python3 bucket_env`

Activate the virtual environment

`$ bucket_env/bin/activate`

Install all application requirements from the requirements file found in the root folder

`$ pip install -r requirements.txt`

Create a database, preferably postgres
`$ psql postgres`
`$ CREATE DATABASE bucketlist`

Create a database for running the Tests
`$ CREATE DATABASE bucketlist_test`

Create migrations and upgrade

`$ python manage.py db init`

`$ python manage.py db migrate`

`$ python manage.py db upgrade`

All done! Now, start your server by running `python manage.py runserver`.

### Supported End points

Endpoint | Functionality| Access
------------ | ------------- | -------------
POST /api/v1/auth/login |Logs a user in | PUBLIC
POST /api/v1/auth/register | Registers a user | PUBLIC
POST /api/v1/bucketlists/ | Creates a new bucket list | PRIVATE
GET /api/v1/bucketlists/ | Lists all created bucket lists | PRIVATE
GET /api/v1/bucketlists/<bucketlist_id> | Gets a single bucket list with the suppled id | PRIVATE
PUT /api/v1/bucketlists/<bucketlist_id> | Updates bucket list with the suppled id | PRIVATE
DELETE /api/v1/bucketlists/<bucketlist_id> | Deletes bucket list with the suppled id | PRIVATE
POST /api/v1/bucketlists/<bucketlist_id>/items/ | Creates a new item in bucket list | PRIVATE
PUT /api/v1/bucketlists/<bucketlist_id>/items/<item_id> | Updates a bucket list item | PRIVATE
DELETE /api/v1/bucketlists/<bucketlist_id>/items/<item_id> | Deletes an item in a bucket list | PRIVATE
