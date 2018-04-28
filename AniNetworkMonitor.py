from ANMConstants import *
import requests
import json
import time


class AniNetworkMonitor():
    def __init__(self, id):
        self.r = requests.Session()
        self.tor_id = id
        self.tor_info = {}
        self.session_cookie = ""

    def run(self):
        self.login()
        while True:
            self.tor_info = self.get_torrent_info()
            if len(self.tor_info) == 0:
                print("Torrent Does Not Exist")
                break
            if self.tor_info["is_finished"]:
                self.remove_torrent()
                break
            else:
                time.sleep(self.tor_info['eta'])
                pass
        self.r.close()



    """
        Return Json object containing information about the torrent.
    """
    def get_torrent_info(self):
        data = {"id": 1, "method": DELUGE_GET_TORRENT, "params": [self.tor_id, {}]}
        self.r = requests.post(URL, data=json.dumps(data), headers=HEADERS, cookies={'_session_id': self.session_cookie})
        return json.loads(self.r.content)['result']

    def remove_torrent(self):
        remove_data = {"id": 1, "method": DELUGE_REMOVE_TORRENT, "params": [self.tor_id, ""]}
        self.r = requests.post(URL, data=json.dumps(remove_data), headers=HEADERS, cookies={'_session_id': self.session_cookie})

    def login(self):
        login_data = {"id": 1, "method": DELUGE_LOGIN, "params":["deluge"]}
        self.r = requests.post(URL, data=json.dumps(login_data), headers=HEADERS)
        self.session_cookie = self.r.headers['Set-Cookie'].split(";")[0].split("=")[1]


anm = AniNetworkMonitor("262f9701629bad4413362876d3f40d7c9d557ec8")
anm.run()