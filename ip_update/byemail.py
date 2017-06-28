from __future__ import unicode_literals

import os
import yaml
import smtplib
import logging

from email.mime.text import MIMEText

lgr = logging.getLogger("file")

def get_email_yaml_file_path():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "config", "emails.yaml")

def load_email_list():
    with open(get_email_yaml_file_path()) as f:
        return yaml.load(f)['emails']

def load_email_server_settings():
    with open(get_email_yaml_file_path()) as f:
        return yaml.load(f)["smtp"]

def build_email_content(settings, cur_ip, target_emails):
    msg = MIMEText("The new IP address for {server_name} is {ip}".format(
        server_name=settings["server_name"], ip=cur_ip
    ))
    msg["Subject"] = 'IP address of {server_name} Changed'.format(server_name=settings["server_name"])
    msg["From"] = settings["email"]
    msg["To"] = target_emails
    return msg

def connect_email_server(settings):
    server = smtplib.SMTP(settings["smtp_server"], settings["smtp_server_port"])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(settings["email"], settings["password"])
    return server

def send_emails(cur_ip):
    target_emails = load_email_list()
    lgr.debug("Email List: %s" % ", ".join(target_emails))
    settings = load_email_server_settings()
    msg = build_email_content(settings, cur_ip, ", ".join(target_emails))
    try:
        server = connect_email_server(settings)
        server.sendmail(settings["email"], target_emails, msg.as_string())
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        lgr.error("Email Account Error: cannot authenticate account.")
    except smtplib.SMTPConnectError:
        lgr.error("Email Account Error: cannot connect to smtp server")
    except Exception, e:
        lgr.error("Email Error: %s" % e.message)
    return False


