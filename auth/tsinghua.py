from __future__ import unicode_literals
import os

import yaml
import logging
import requests
import hashlib

lgr = logging.getLogger("file")

login_url = "http://net.tsinghua.edu.cn/do_login.php"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)" \
             " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"

default_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config", "account.yaml")


def load_config(path=default_path):
    with open(path) as f:
        config = yaml.load(f)
        username = config["account"]["username"]
        password = config["account"]["password"]

        return username, password


def hex_md5_password(password):
    password = hashlib.md5(password).hexdigest()
    return "{MD5_HEX}%s" % password


def try_connections():
    try:
        res = requests.get("http://www.baidu.com")
    except Exception, e:
        lgr.warning("Connection Error: %s" % e.message)
        return False
    return res.status_code == 200


def go_online():
    username, password = load_config()
    param = {
        "action": "login",
        "username": username,
        "password": hex_md5_password(password),
        "ac_id": 1
    }
    res = requests.post(login_url, param)
    if res.status_code != 200:
        return False
    else:
        return True
