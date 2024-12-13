import datetime
import decimal

from flask.json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)
