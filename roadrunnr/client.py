__author__ = 'sandeep'
import requests
import ujson as json
from .constants import RR_URL
from .errors import HTTPError


class RoadRunnrClient(object):
    def __init__(self, client_id, client_secret, server_url=None, timeout=10):
        """
        :param client_id: RoadRunnr client id.
        :param client_secret: RoadRunnr client secret.
        :param server_url: RoadRunnr server base URL.
        """

        if not server_url:
            self.SERVER_URL = RR_URL
        else:
            self.SERVER_URL = server_url

        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.timeout = timeout
        self.TOKEN = self.get_new_access_token()
        self.HEADERS = {"Content-Type": "application/json", "Authorization": "Token "+self.TOKEN}

    def _get_repsonse_dict(self, response):
        if not response.status_code == 200:
            raise HTTPError(response.content)
        return json.loads(response.content)

    def get_new_access_token(self):
        API_URL = "{0}oauth/token/".format(self.SERVER_URL)
        params = {"grant_type": "client_credentials",
                  "client_id": self.CLIENT_ID,
                  "client_secret": self.CLIENT_SECRET}
        response = requests.get(API_URL, params=params, timeout=self.timeout)
        token = self._get_repsonse_dict(response)['access_token']
        return token

    def get_access_token(self):
        if not self.access_token:
            self.access_token = self.get_new_access_token()
        return self.access_token

    def _order(self, order_id, action=""):
        valid_actions = ['ship', 'track', 'cancel', 'complete']
        API_URL = "{0}v1/orders/{1}".format(self.SERVER_URL, order_id)
        if action and (action in valid_actions):
            API_URL = API_URL + "/" + action
        response = requests.get(API_URL, headers=self.HEADERS, timeout=self.timeout)
        return self._get_repsonse_dict(response)

    def create_order(self, order_data, ship=False):
        API_URL = "{0}v1/orders/".format(self.SERVER_URL)
        if ship:
            API_URL = API_URL + "ship"
        response = requests.post(API_URL, json=order_data, headers=self.HEADERS)
        return self._get_repsonse_dict(response)

    def get_order(self, order_id):
        return self._order(order_id)

    def ship_order(self, order_id):
        return self._order(order_id,action="ship")

    def track_order(self, order_id):
        return self._order(order_id,action="track")

    def cancel_order(self, order_id):
        return self._order(order_id,action="cancel")

    def complete_order(self, order_id):
        return self._order(order_id,action="complete")

    def get_localities(self, default_response=False):
        API_URL = "{0}locality/all_localities".format(self.SERVER_URL)
        response = requests.get(API_URL, headers=self.HEADERS, timeout=self.timeout)
        resp = self._get_repsonse_dict(response)
        if default_response:
            return resp
        else:
            return [x["name"] for x in resp["localities"]]

    def get_cities(self):
        return ["Bangalore", "Gurgaon", "Mumbai", "Delhi", "Hyderabad"]
