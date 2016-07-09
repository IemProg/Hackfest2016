Hackfest 2016
------------

### To set up

#### Pip
Make sure you have Python 2.7 installed. Then, install pip from here: https://pip.pypa.io/en/latest/installing/. 

#### Virtualenv
Run:

`[sudo] pip install virtualenv`

Good tutorial on why we need virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

To start developing, make sure you have virtualenv running:

`virtualenv env`

This will create an `env/` folder. Run:

`source env/bin/activate`

This will activate virtualenv. To deactivate (don't do this right now! When you want to stop developing do this):

`deactivate`

Now, you're ready to develop!

#### Install dependencies
Run `pip install -r requirements.txt`. This should install all the dependencies. Whenever you add a new library or something from pip, add it to `requirements.txt`. More info about requirements.txt here: https://pip.pypa.io/en/stable/user_guide/#requirements-files 




