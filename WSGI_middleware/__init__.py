class WSGI_app:
    def __init__(self, app):
        self.app = app
        self.route = app.route

    def __call__ (self, environ, start_response):
        for key, value in environ.items():
            print(key, ": ", value)

        return self.app(environ, start_response)
