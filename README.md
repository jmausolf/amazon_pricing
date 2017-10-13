# Welcome to the Amazon Pricing


This script is designed for users with a [seller account on the Amazon marketplace](https://services.amazon.com/content/sell-on-amazon.htm?ld=SCSOAStriplogin).

It is designed to automate offering the lowest price for every item in your inventory. After setup, once the script is executed, it will try to offer the lowest price every 15 minutes. You can edit the timing if you desire.

# Let the Price War Begin

### Prerequisites

* Python 3.5+
* Firefox 46.0.1+
* [Selenium](http://selenium-python.readthedocs.io)==2.53.6+

### Setup

#### Git Clone

First clone the repository in terminal:
* `git clone --recursive https://github.com/jmausolf/amazon_pricing`

Change directories to enter the local repository:
* `cd amazon_pricing`

#### User Credentials

You will need to create a `credentials.py` file. It is recommended to simply edit the `example_credentials.py` file and rename it.

```python
amazon_email = "myemail@gmail.com"
amazon_password = "mysupersecret"
```

Edit the text in quotes to your actual username and password. Save the file and rename it credentials.py. Assuming you are in the repo directory, the bash command would be `mv example_credentials.py credentials.py` .

#### Firefox

* *Recommendation:* Under Firefox Settings>Privacy: select "Always use private browsing mode" | This will help avoid Amazon captcha's. Adjusting the timing can also help if you have trouble.



## Run Price War App

In terminal run the following command: `python price_war.py`

*Note:* If you have several versions of python, you will need to amend the above line to run your python 3 alias, e.g. `python3 price_war.py`.


## Timing

You can adjust the timing from the command line. The default is 900 seconds (15 minutes). Here are some examples:

* Every 30 minutes: `python price_war.py -t 1800`
* Every hour: `python price_war.py -t 3600`

## Second-Factor Authentication

Given the move to requiring second factor authentication with Amazon login's, the latest version of the code works with this change.

### Assumptions

* MAC OS with iMessages enabled. 
* Second Factor Authentication with Amazon is set to provide a code sent my SMS message.

Assuming the above, the following option will first attempt to login to Amazon, prompting the second-factor code to be texted to your devices via iMessage. Once receiving the text, the code queries your internal iMessages SQLite database, and returns the latest security code from Amazon (262966). Upon retrieving the code from your messages, it enters the code into the second-factor web-prompt and proceeds with the remaining price-war code.

To use:

* Default time: `python price_war.py -s True`
* Custom time: `python price_war.py -s True -t 3600`

The base code [pymessage-lite](https://github.com/mattrajca/pymessage-lite) to query messages was [forked and modified for compatibility with Python3](https://github.com/jmausolf/pymessage-lite/tree/47b349af1ce22453f3c6def4218b2de9947ab1f8). 
