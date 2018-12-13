from spotipy import Spotify


class SpotifyWithPlayer(Spotify):

    def __init__(self, auth=None, requests_session=True,
                 client_credentials_manager=None, proxies=None, requests_timeout=None):

        super().__init__(auth=auth, requests_session=requests_session,
                         client_credentials_manager=client_credentials_manager, proxies=proxies,
                         requests_timeout=requests_timeout)

    def current_user_pause(self):
        return self._put("me/player/pause")

    def current_user_volume(self, volume):
        return self._put("me/player/volume?volume_percent={}".format(volume))

    def current_user_play(self):
        return self._put("me/player/play")

    def current_user_previous(self):
        return self._post("me/player/previous")

    def current_user_next(self):
        return self._post("me/player/next")

    def current_user_shuffle(self, shuffle):
        return self._put("me/player/shuffle?state={}".format(shuffle))

    def current_user_repeat(self, repeat):
        return self._put("me/player/repeat?state={}".format(repeat))
