from __future__ import unicode_literals
import os
import yaml
import logging.config

from auth.tsinghua import go_online, try_connections
from ip_update.ip import check_ip
from ip_update.byemail import send_emails
from ip_update.err import BaiduIPQueryException

base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_dir, "conf", "log.yaml")) as f:
    log_config = yaml.load(f)
    logging.config.dictConfig(log_config)

lgr = logging.getLogger("file")


def check_network_connection():
    if not try_connections():
        res = go_online()
        return res
    return True



def main():
    # check network connection first
    lgr.debug("Try network connections")
    if not try_connections():
        lgr.debug("Login...")
        res = go_online()
        if not res:
            lgr.error("Fail to connect to the internet")
            return
        else:
            lgr.debug("Login success")
    else:
        lgr.debug("Network connection available")

    lgr.debug("Query public ip")
    try:
        ip = check_ip()
    except BaiduIPQueryException:
        return
    if ip is None:
        lgr.debug("IP not changed. Abort.")
        return
    # when ip is not none, that means
    lgr.debug("Send emails")
    res = send_emails(ip)
    if res:
        lgr.debug("Success\n\n")
    else:
        lgr.debug("Error Occurs\n\n")


if __name__ == '__main__':
    main()