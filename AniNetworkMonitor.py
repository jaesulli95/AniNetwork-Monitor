from ANMConstants import *
import requests
import json
import time


class AniNetworkMonitor():
    def __init__(self, tml):
        self.r = requests.Session()
        self.tor_id = None
        self.tor_info = {}
        self.session_cookie = ""
        self.tor_mag_link = tml

    def run(self):
        self.login()
        self.add_torrent()
        while True:
            self.tor_info = self.get_torrent_info()
            if len(self.tor_info) == 0:
                break
            if self.tor_info["is_finished"]:
                self.remove_torrent(self.tor_id)
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
    """
        Remove the torrent identified by it's hash from the deluge client, and then allow for it to be moved.
    """
    def remove_torrent(self, id):
        remove_data = {"id": 1, "method": DELUGE_REMOVE_TORRENT, "params": [id, ""]}
        self.r = requests.post(URL, data=json.dumps(remove_data), headers=HEADERS, cookies={'_session_id': self.session_cookie})
    """
        Login into the API, and deluge torrent set.
    """
    def login(self):
        login_data = {"id": 1, "method": DELUGE_LOGIN, "params":["deluge"]}
        self.r = requests.post(URL, data=json.dumps(login_data), headers=HEADERS)
        self.session_cookie = self.r.headers['Set-Cookie'].split(";")[0].split("=")[1]
    """
        Add Torrent to be downloaded, using the magnet link.
    """
    def add_torrent(self):
        add_data = {"id":1, "method": DELUGE_ADD_TORRENT, "params": [self.tor_mag_link, {}]}
        self.r = requests.post(URL, data=json.dumps(add_data), headers=HEADERS, cookies={'_session_id': self.session_cookie})
        self.tor_id = json.loads(self.r.content)['result']