import datetime as dt
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, dt.datetime):
            return str(z)
        else:
            return super().default(z)
