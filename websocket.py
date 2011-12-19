import uuid
import tornado.ioloop
import tornado.web
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    waiters = set()
    user = None

    def open(self):
        EchoWebSocket.waiters.add(self)
        print "WebSocket opened"

    def on_close(self):
        try:
            EchoWebSocket.waiters.remove(self)
        except ValueError:
            pass
        print "WebSocket closed"

    def on_message(self, message):
        if message.startswith('user:'):
            print 'User logged: '+message
            self.user = message.split(':')[1]
            self.user_uuid = str(uuid.uuid4())
            return
        if message == 'refresh' and self.user is not None:
            print 'refreshing...'
            for w in EchoWebSocket.waiters:
                if w != self and w.user == self.user:
                    w.write_message('refresh')


application = tornado.web.Application([
    (r'/', EchoWebSocket),
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
