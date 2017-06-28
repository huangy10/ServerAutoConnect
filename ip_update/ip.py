from __future__ import unicode_literals

from bs4 import BeautifulSoup
import urllib2
import os
import yaml
import logging

from err import BaiduIPQueryException

lgr = logging.getLogger("file")

base_dir = os.path.abspath(os.path.dirname(__file__))
yaml_path = os.path.join(base_dir, "config", "ip_records.yaml")
with open(yaml_path) as f:
    ip_records = yaml.load(f)

def query_public_ip():
    request = urllib2.urlopen(
        'http://www.baidu.com/s?wd=ip&rsv_spt=1&rsv_iqid=0xbefbb8610000747d&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=4&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&inputT=1648&rsv_sug4=1648'
    )

    soup = BeautifulSoup(request, "html.parser")
    ipResponse = soup.find("div", {'class': "result-op c-container"}).get("fk")

    return ipResponse


def get_previous_ip():
    ips = ip_records["ips"]
    if ips is None:
        return None
    else:
        return ips[0]


def update_ip_records(new_ip):
    ips = ip_records["ips"]
    if ips is None:
        ip_records["ips"] = [new_ip]
    else:
        ips.insert(0, new_ip)
    with open(yaml_path, "w") as f:
        f.write(yaml.dump(ip_records, indent=4, default_flow_style=False))

def check_ip():
    prev_ip = get_previous_ip()
    try:
        cur_ip = query_public_ip()
    except Exception, e:
        lgr.error("Error when query ip through baidu: %s" % e.message)
        raise BaiduIPQueryException
    if prev_ip == cur_ip:
        return None
    else:
        update_ip_records(cur_ip)
        return cur_ip
