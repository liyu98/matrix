
import grequests
import logging

class ClientHandler:
    """Performs concurrent requests with timeout

    :OPERATION_MODE n_firsts, timeout or wait_all.
    :clients list of clients' (host, port) tuples
    """

    def __init__(self, clients, OPERATION_MODE='wait_all', **kwargs):
        self.clients = self.parse_clients(clients)
        self.n_clients = len(clients)
        if not OPERATION_MODE == 'wait_all':
            raise Exception('Operation mode not accepted')
        logging.info(
            '[Client Handler] Operation mode: {}'.format(OPERATION_MODE))

    def perform_requests_and_wait(self, endpoint):

        client_urls = self.get_client_urls(endpoint)
        rs = (grequests.get(u) for u in client_urls)
        responses = grequests.map(rs)
        for res in responses:
            if not res or res.status_code != 200:
                raise Exception('The response was not successful. '
                                'Code: {}, Msg: {}'.format(res.status_code,
                                                           res.text))
        l = len(responses)
        logging.info('[Client Handler] Got {} responses'.format(l))

    @staticmethod
    def parse_clients(clients):
        p_clients = []
        for cl in clients:
            host = cl[list(cl.keys())[0]]['host']
            port = cl[list(cl.keys())[0]]['port']
            p_clients.append((host, port))
        return p_clients

    def get_client_urls(self, endpoint):
        urls = []
        for host, port in self.clients:
            urls.append('http://{}:{}/{}'.format(host, port, endpoint))
        return urls