#!/usr/bin/env python3

import os
import requests
import json
from configparser import ConfigParser
from datetime import datetime
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.basename(__file__)
config = ConfigParser()
config.read(dir_path + "/config.ini")


def get_now_time():
    """
    取得現在的時間字串
    """
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    URL_ROOT = "https://tfc-taiwan.org.tw"
    token = config["TFC"]["token"]
    now_time = get_now_time()
    print("Run @ {}".format(now_time))

    endpoint = "{0}/{1}".format(URL_ROOT, "article-api")
    page = 0
    condition = True
    while condition:
        print("Prepare to get page: {}".format(page))
        payload = {
            "token": token,
            "page": page,
        }

        try:
            response = requests.get(endpoint, params=payload, timeout=15)
            data = json.loads(response.content)

            filename = "data/page-{}.json".format(page)
            with open(filename, "w", encoding="utf8") as pagefile:
                json.dump(data, pagefile, indent=4, ensure_ascii=False)
            # for node in data["nodes"]:
            #     print(node["node"]["nid"])

        except requests.exceptions.HTTPError as err:
            print("HTTP exception error: {}".format(err))
        except requests.exceptions.RequestException as e:
            print("Exception error {}".format(e))
        if data.get("pager"):
            if int(data["pager"]["page"]) <= int(data["pager"]["pages"]) - 2:
                # if int(data["pager"]["page"]) <= 2:
                page = int(data["pager"]["page"]) + 1
            else:
                condition = False
        sleep(2)
