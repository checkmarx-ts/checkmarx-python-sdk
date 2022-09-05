# monitor engine status
# 1. Alert user if engine is offline
# 2. Alter user if one engine receives more than 3 scans
# 3. Logging the 2 activities mentioned above
# 4. Alert means send emails to user via SMTP service. Send alert email once per day at most.

import threading
import smtplib

from email.mime.text import MIMEText

from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI, EnginesAPI


# Function wrapper
def periodic_task(interval, times=-1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()

            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap


def send_email(smtp_server, sender_email, password, receivers_email, email_subject, email_content):
    """

    Args:
        smtp_server:
        sender_email:
        password:
        receivers_email:
        email_subject:
        email_content:

    Returns:

    """

    from_address = sender_email
    to_address = receivers_email
    smtp_server = smtp_server

    msg = MIMEText(email_content, 'html')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['subject'] = email_subject

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(from_address, password)
        server.sendmail(from_addr=from_address, to_addrs=receivers_email, msg=msg.as_string())
        server.quit()
    except smtplib.SMTPException:
        print("fail to send email")


def check_if_some_engine_has_more_than_3_scans():
    all_scans_in_queue = ScansAPI().get_all_scan_details_in_queue()
    # group by engine id, count number of scans in each engine
    # logging if more than 3 scans in one engine
    # send alert email


def get_offline_engines():
    all_engine_server = EnginesAPI().get_all_engine_server_details()
    return [item for item in all_engine_server if item.status.value == "Offline"]


def send_alert_email_of_offline_engines(offline_engines):
    engines_tag = "".join([
        """
        <tr>
            <td>{id}</td>
            <td>{name}</td>
            <td>{uri}</td>
            <td>{minLoc}</td>
            <td>{maxLoc}</td>
            <td>{maxScans}</td>
            <td>{cxVersion}</td>
            <td>{status}</td>
        </tr>
        """.format(
            id=item.id, name=item.name, uri=item.uri, minLoc=item.min_loc, maxLoc=item.max_loc,
            maxScans=item.max_scans, cxVersion=item.cx_version, status=item.status.value
        ) for item in offline_engines
    ])

    style = """
    <style>
          table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
          }
          th, td {
            padding: 5px;
            text-align: left;
          }
        </style>
    """

    html = """
    <!DOCTYPE html>
    <html>
      <head>
        {style}
      </head>
      <body>
        <table style="width:100%">
          <caption>Offline Engines</caption>
          <tr>
            <th>id</th>
            <th>name</th> 
            <th>uri</th>
            <th>minLoc</th>
            <th>maxLoc</th>
            <th>maxScans</th>
            <th>cxVersion</th>
            <th>status</th>
          </tr>
          {engines}
        </table>
      </body>
    </html>
        """.format(style=style, engines=engines_tag)
    send_email(smtp_server='smtp.163.com', sender_email='yang2149@163.com', password='VNJTHYGTGCYNFFJP',
               receivers_email='happy.yang@checkmarx.com', email_subject='Checkmarx Engine Offline Alert',
               email_content=html)


def check_if_engine_offline():
    pass
    # logging the engine server information if it is offline
    # send alert email




if __name__ == '__main__':
    offline_engines_data = get_offline_engines()
    if offline_engines_data:
        # TODO check if email has been sent today, if not prepare to send the email
        # if the file 'send_email_engine_offline_activity.txt' does not exist, create it.
        # read 'send_email_engine_offline_activity.txt' and get last line

        send_alert_email_of_offline_engines(offline_engines_data)
        # log the send email activity. date and time, tag (eg, send_alert_email_of_offline_engines,
        # send_alert_email_of_too_many_scans_in_one_engine)

# send_alert_email(smtp_server='smtp.163.com', sender_email='yang2149@163.com', password='VNJTHYGTGCYNFFJP',
#                  receivers_email='happy.yang@checkmarx.com', email_subject='Checkmarx Engine Offline Alert',
#                  email_content=content)
