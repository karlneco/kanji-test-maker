import json
from flask import Response
class JSONResponse(Response):

    def __repr__(self):
        headers = {}
        while len(self.headers) > 0:
            tuple_ = self.headers.popitem()
            headers[tuple_[0]] = tuple_[1]

        data = {
            'status': self.status,
            'headers': headers,
            'body': self.json
        }
        return json.dumps(data)
