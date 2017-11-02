
from tornado.web import RequestHandler, Application, removeslash, ErrorHandler
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import requests
import urllib.parse
import json
import os


class UpHandler(RequestHandler):
    def get(self):
        resp = json.loads(requests.get("https://api.themoviedb.org/3/movie/upcoming?api_key=194f0c51faac275b70ae54dcd0116ce9").text)
        self.write(json.dumps(resp))



class NowHandler(RequestHandler):
    def get(self):
        resp = json.loads(requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=194f0c51faac275b70ae54dcd0116ce9").text)
        self.write(json.dumps(resp))



class UrlHandler(RequestHandler):
    def get(self):
        title = self.get_argument("title")
        q = urllib.parse.quote_plus(title)
        print(q)
        newresp = json.loads(requests.get("http://www.theimdbapi.org/api/find/movie?title=" + q).text)
        for j in newresp:
            if j.get("trailer") is not None:
                url = j["trailer"][-1]["videoUrl"]
                rel = j["release_date"]
                break

        self.write(json.dumps({"results": [url,rel]}))


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
    server.listen(os.environ.get("PORT",8000))
    IOLoop.current().start()