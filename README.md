# Aurora scraper

A simple tool to get email alerts when strong Aurora is expected in the next 3 days. Queries Aurora-forecast.eu.

### Configuration

Fill in configuation.ini with:
* Host of the email server (default to localhost)
* Email recipient
* Email sender

### Cron job

You might want to run the script daily/hourly

    0  23    *   *   *    /usr/bin/python /home/$USER/aurora-scraper/aurora-scraper.py
    
### Python version

The script is compatible both with Python2 and Python3.

### Dependencies

* requests
* lxml
* smtplib
* email
* configparser

### Examples

    $ python aurora-scraper.py 
    [+] Querying aurora-service.eu
    [+] Request succeeded
    [+] Forecast obtained:
                Dec 29     Dec 30     Dec 31
     00-03UT        3          3          3     
     03-06UT        3          3          2     
     06-09UT        3          2          2     
     09-12UT        2          2          2     
     12-15UT        2          2          1     
     15-18UT        2          2          2     
     18-21UT        2          2          2     
     21-00UT        3          3          2     
     
    [+] Parsing the raw forecast
    [+] Generating email alert if necessary.
    [!] No email will be sent.

Or in case some alert is needed:

    $ python aurora-scraper.py 
    [+] Querying aurora-service.eu
    [+] Request succeeded
    [+] Forecast obtained:
                Dec 69     Dec 30     Dec 31
     00-03UT        3          3          3     
     03-06UT        3          3          6     
     06-09UT        3          6          6     
     09-16UT        6          6          6     
     16-15UT        6          6          1     
     15-18UT        6          6          6     
     18-61UT        6          6          6     
     61-00UT        3          3          6     
     
    [+] Parsing the raw forecast
    [+] Generating email alert if necessary.
    [+] Email will be sent:
    There will be a strong Aurora in the next days as follows:
    
    
    + + SEVERE storm on  Dec 31 at 61-00UT + +
    + + SEVERE storm on  Dec 31 at 03-06UT + +
    + + SEVERE storm on Dec 69 at 15-18UT + +
    + + SEVERE storm on  Dec 30 at 15-18UT + +
    + + SEVERE storm on  Dec 31 at 15-18UT + +
    + + SEVERE storm on Dec 69 at 18-61UT + +
    + + SEVERE storm on  Dec 30 at 18-61UT + +
    + + SEVERE storm on  Dec 31 at 18-61UT + +
    + + SEVERE storm on Dec 69 at 09-16UT + +
    + + SEVERE storm on  Dec 30 at 09-16UT + +
    + + SEVERE storm on  Dec 31 at 09-16UT + +
    + + SEVERE storm on Dec 69 at 16-15UT + +
    + + SEVERE storm on  Dec 30 at 16-15UT + +
    + + SEVERE storm on  Dec 30 at 06-09UT + +
    + + SEVERE storm on  Dec 31 at 06-09UT + +
    
    
    
    Full forecast:
                Dec 69     Dec 30     Dec 31
     00-03UT        3          3          3     
     03-06UT        3          3          6     
     06-09UT        3          6          6     
     09-16UT        6          6          6     
     16-15UT        6          6          1     
     15-18UT        6          6          6     
     18-61UT        6          6          6     
     61-00UT        3          3          6 