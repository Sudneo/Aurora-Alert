import requests
from lxml import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from config import ConfigReader


def config():
    """
    :return: returns the configuration items in section 'mail' of configuration.ini
    """
    configreader = ConfigReader()
    params = configreader.get_config("mail")
    return params


def send_mail(to, fro, subject, text, server="localhost"):
    """
    Send an email alert.
    :param to: The recipient of the email
    :param fro: The sender of the email
    :param subject: The subject of the email
    :param text: The content of the email
    :param server: The mail server host to use to send the email (def. localhost)
    :return: None
    """
    assert type(to) == list
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


def get_raw_forecast():
    """
    Obtains the raw numbers of the forecast from Aurora-forecast.eu
    :return: The raw forecast structure
    """
    print "[+] Querying aurora-service.eu"
    url = 'http://www.aurora-service.eu/aurora-forecast/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print "[-] Request to Aurora-service.eu failed."
        exit(1)
    else:
        print "[+] Request succeeded"
    tree = html.fromstring(response.content)
    element = tree.xpath('/html/body/div[1]/div[3]/div[1]/div/div[1]/div[2]/pre/p/strong')
    raw_forecast = element[0].text_content()
    print "[+] Forecast obtained:"
    print raw_forecast
    return raw_forecast


def parse_forecast(raw_forecast):
    """
    Parses the forecast according to the dates
    :param raw_forecast: The raw forecast structure
    :return: The list of dates and the list of forecasts
    """
    print "[+] Parsing the raw forecast"
    lines = raw_forecast.split("\n")
    dates = filter(None, lines[0].split("  "))
    forecasts = {}
    for line in filter(None, lines[1:]):
        if len(line) > 1:
            items = filter(None, line.split(" "))
            forecasts[items[0]] = items[1:]
    return dates, forecasts


def alert(dates, forecasts):
    """
    Check the parsed forecast for high activity of aurora and composes the email text accordingly.
    :param dates: The list of dates for which the forecast is available
    :param forecasts: The actual aurora predictions of those dates
    :return: None
    """
    print "[+] Generating email alert if necessary."
    email_text = ""
    email_to = config()['to']
    email_from = config()['from']
    email_server = config()['host']
    email_subj = "Aurora Alert"
    send_email = False
    for key in forecasts:
        for i in range(3):
            if "5" in forecasts[key][i]:
                email_text += "Moderate storm on %s at %s\n" % (dates[i], key)
                send_email = True
            if "6" in forecasts[key][i]:
                email_text += "+ + SEVERE storm on %s at %s + +\n" % (dates[i], key)
                send_email = True
            if "7" in forecasts[key][i]:
                email_text += "# # HUGE storm on %s at %s # #\n" % (dates[i], key)
                send_email = True
    if len(email_text) > 0:
        email_text = "There will be a strong Aurora in the next days as follows:\n\n\n" + email_text
        email_text += "\n\n\nFull forecast:\n%s" % get_raw_forecast()
    if send_email:
        print "[+] Email will be sent:\n%s" % email_text
        send_mail(email_to, email_from, email_subj, email_text, email_server)
    else:
        print "[!] No email will be sent."


def main():
    """
    Mail function to coordinate execution
    :return: None
    """
    raw = get_raw_forecast()
    dates, forecasts = parse_forecast(raw)
    alert(dates, forecasts)


if __name__ == '__main__':
    main()
