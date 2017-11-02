
from tornado.web import RequestHandler, Application, removeslash, ErrorHandler
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import requests
import urllib.parse
import json


class UpHandler(RequestHandler):
    def get(self):
        pass



class NowHandler(RequestHandler):
    def get(self):
        pass



class UrlHandler(RequestHandler):
    def get(self):
        title = self.get_argument("title")
        q = urllib.parse.quote_plus(title)
        print(q)
        newresp = json.loads(requests.get("http://www.theimdbapi.org/api/find/movie?title=" + q).text)
        for j in newresp:
            if j.get("trailer") is not None:
                url = j["trailer"][-1]["videoUrl"]
                break

        self.write(json.dumps({"results": url}))


settings = dict(debug=True)

app = Application(
    handlers=[
      (r'/upcoming', UpHandler),
      (r'/now_playing', NowHandler),
      (r'/url', UrlHandler)
    ],
    **settings
)

if __name__ == "__main__":
    server = HTTPServer(app)
    server.listen(8000)
    IOLoop.current().start()