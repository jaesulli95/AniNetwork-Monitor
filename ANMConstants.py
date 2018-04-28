PORT = 8112
URL = "http://127.0.0.1:{}/json".format(PORT)
HEADERS = {'Accept': 'application/json', 'Content-type': 'application/json'}
DELUGE_LOGIN = "auth.login"
DELUGE_GET_TORRENT = "core.get_torrent_status"
DELUGE_ADD_TORRENT = "core.add_torrent_magnet"
DELUGE_REMOVE_TORRENT = "core.remove_torrent"