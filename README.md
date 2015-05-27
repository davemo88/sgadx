# sgadx
signaling game ad exchange

setup:

0. use pip to install depenencies, i.e. `$ pip install -r requirements.txt`
1. copy config.sample.py to config.py. 
 * you may modify this as needed. without modification it will use a sqlite database.
2. run db_create.py

You can now run simulations. See the wiki on github for further instructions. We don't have 100% test coverage but you can do `$ nosetests -v --nocapture tests/adx_test.py` to be pretty sure everything is working.
