Installing Local Test Environment for A+
========================================


## Prerequisites

You need to have Python 3.4+ and virtualenv installed.
Follow the OS specific instructions below to install everything you need.

### Ubuntu

The "python3" package of Ubuntu/Debian is still Python 3.2.
Until the packaged version is upgraded it is necessary to compile from source.
Other Linux flavors should follow the same pattern (e.g. replace apt-get with yum).

	sudo apt-get install build-essential libssl-dev libsqlite3-dev
	wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz
	tar xvf Python-3.4.3.tar.xz
	cd Python-3.4.3
	./configure
	make
	sudo make install

	sudo pip3 install --upgrade pip
    sudo pip3 install virtualenv

    cd [project_root]
    ./create_test_environment.sh [optional_path_to_virtualenv]

### OS X

These instructions use the [Homebrew](http://brew.sh/) package manager.
To compile packages also the Xcode command line tool package is required.

    xcode-select --install
    sudo brew install python3

    sudo pip3 install --upgrade pip
    sudo pip3 install virtualenv

	cd [project_root]
	./create_test_environment.sh [optional_path_to_virtualenv]

### Windows

First install Python 3.4 from [python.org](https://www.python.org/downloads/).
Then manually create Python virtualenv.

	cd [project_root]
	C:\Python34\python -m venv [path_to_virtualenv]
	[path_to_virtualenv]/Scripts/activate.bat
	pip install --upgrade pip
	pip install -r requirements.txt

Last manually create Django sqlite database for testing.

	python manage.py migrate
	python manage.py loaddata doc/initial_data.json
	python manage.py createsuperuser


## Running a Local A+ Development Environment

After running the automatic script or setting up the environment manually
you can start the A+ server by running (from the project root folder):

    PATH_TO_VIRTUALENV/bin/python manage.py runserver 8000

Unit tests can be executed by running:

    PATH_TO_VIRTUALENV/bin/python manage.py test


## Example grader

If you've loaded the initial data the example exercise relies on you can use the external grader server
(example_grader.py) running on port 8888. This grader can be started by running:

    cd [project_root]/doc
    PATH_TO_VIRTUALENV/bin/python example_grader.py

Now the example exercise in A+ should work and you should get points from submissions accordingly.


## Selenium integration tests

Selenium tests are designed to run against a certain database state and service ports.
The tests will automatically open and direct Firefox browser windows. Currently the tests
are depended on unix type shell. All the following commands assume that the project
virtualenv is activated:

		cd [project_root]
		source PATH_TO_VIRTUALENV/bin/activate

### Prerequisites

  - Firefox browser installed
  - Following packages in the virtualenv

		pip install selenium
		pip install nose

### Running

To setup the servers and run all the tests at one go:

	selenium_test/run_servers_and_tests.sh

Running individual tests:

	cd selenium_test/test/
	../run_servers.sh

	python login_test.py
	python home_page_test.py

	../kill_servers.sh
