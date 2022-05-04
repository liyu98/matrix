from shared import utils
import requests
import logging
import socket
from time import sleep
import multiprocessing
import random
from string import ascii_uppercase, digits

IDLE = 0

CLIENT_TRAIN_MODEL = 1
CLIENT_GET_AGG_MODEL = 2
CLIENT_SEND_MODEL = 3

SEC_AGG_GET_CLIENT_MODEL = 4
SEC_AGG_AGGREGATE_MODELS = 5
SEC_AGG_SEND_TO_MAIN_SERVER = 6

MAIN_SERVER_SEND_MODEL_TO_CLIENTS = 7
MAIN_SERVER_GET_SECAGG_MODEL = 8

PING_CADENCE = 20  # Seconds

hosts = utils.read_hosts()


class State:
    def __init__(self, client_type, port, _id=None):
        assert client_type in ('client', 'secure_aggregator', 'main_server')
        self.client_type = client_type
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self._id = _id if _id else self.generate_random_id()
        self._current_state = IDLE
        self.current_state = IDLE
        p = multiprocessing.Process(target=self.send_ping_continuously)
        p.start()

    def generate_random_id(self, N=8):
        rand = ''.join(random.choices(ascii_uppercase + digits, k=N))
        return '{}_{}_{}'.format(self.client_type, self.port, rand)

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, state):
        self._current_state = state
        payload = {
            'client_type': self.client_type,
            '_id': self._id,
            'state': self.get_state_string(self._current_state),
            'port': self.port,
            'host': self.host
        }
        try:
            print("set current_state:")
            print('http://{}:{}/send_state'.format(hosts['dashboard']['host'], hosts['dashboard']['port']))
            requests.post(
                url='http://{}:{}/send_state'.format(
                    hosts['dashboard']['host'],
                    hosts['dashboard']['port']
                ),
                json=payload
            )
        except Exception as e:
            logging.warning('Dashboard not reachable.\n{}'.format(e))

    def idle(self):
        self.current_state = IDLE

    def is_idle(self):
        return self.current_state == IDLE

    def send_ping_continuously(self):
        while True:
            print("send_ping_continuously...")
            self.send_ping()
            sleep(PING_CADENCE)

    def send_ping(self):
        payload = {
            'client_type': self.client_type,
            '_id': self._id,
            'state': self.get_state_string(self.current_state),
            'port': self.port,
            'host': self.host
        }
        try:
            requests.post(
                url='http://{}:{}/ping'.format(
                    hosts['dashboard']['host'],
                    hosts['dashboard']['port']
                ),
                json=payload
            )
            print("send_ping...")
        except Exception as e:
            logging.warning('Dashboard not reachable.\n{}'.format(e))

    @staticmethod
    def get_state_string(state):
        strings = {
            IDLE: 'IDLE',
            CLIENT_TRAIN_MODEL: 'Training model',
            CLIENT_GET_AGG_MODEL: 'Getting aggregated model',
            CLIENT_SEND_MODEL: 'Sending model to secure aggregator',
            SEC_AGG_GET_CLIENT_MODEL: 'Getting getting client models',
            SEC_AGG_SEND_TO_MAIN_SERVER: 'Sending model to main server',
            SEC_AGG_AGGREGATE_MODELS: 'Aggregating models',
            MAIN_SERVER_GET_SECAGG_MODEL: 'Getting model from sec agg',
            MAIN_SERVER_SEND_MODEL_TO_CLIENTS: 'Sending model to clients',
        }
        if state not in strings:
            raise Exception('State not recognized')
        return strings[state]
