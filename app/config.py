import os
from typing import List, Union


class Configuration:
    token: str
    log_level: str
    admins_list: List[int]
    rcon_host: str
    rcon_port: int
    rcon_pass: str

    @classmethod
    def from_env(cls):
        kwargs = {'token': os.environ['TOKEN'],
                  'admins_list': os.environ['ADMINS_LIST'].split('_'),
                  'rcon_host': os.environ['RCON_HOST'],
                  'rcon_pass': os.environ['RCON_PASS']}

        if os.environ.get('RCON_PORT'):
            kwargs['rcon_port'] = os.environ['RCON_PORT']
        if os.environ.get('LOG_LEVEL'):
            kwargs['log_level'] = os.environ['LOG_LEVEL']

        return cls(**kwargs)

    def __init__(self,
                 token: str,
                 admins_list: List[int, str],
                 rcon_host: str,
                 rcon_pass: str,
                 rcon_port: Union[int, str] = 25575,
                 log_level: str = 'INFO',):
        self.token = token
        self.log_level = self._check_log_level(log_level)
        self.admins_list = [int(v) for v in admins_list]
        self.rcon_host = rcon_host
        self.rcon_port = int(rcon_port)
        self.rcon_pass = rcon_pass

    def _check_log_level(self, log_level: str):
        if log_level.upper() in ('CRITICAL', 'ERROR', 'WARNING', 'INFO',
                                 'DEBUG', 'NOTSET'):
            return log_level.upper()
        raise ValueError('Uncorrect logging level.')
