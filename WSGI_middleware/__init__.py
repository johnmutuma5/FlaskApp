def OPTIONS_Server (environ, start_response):
        origin ='*' #environ["HTTP_ORIGIN"]

        status = "200 OK"
        response_headers = [("Access-Control-Allow-Headers", "Content-Type"), ("Access-Control-Allow-Origin", origin)]
        start_response(status, response_headers)
        return [b" "] #use b or encode since application must return bytes


class WSGI_app:
    def __init__(self, app):
        self.app = app
        self.route = app.route
        # self.preflight_server = OPTIONS_Server() #if defined as callable class

    def __call__ (self, environ, start_response):
        # we can respond with a preflight server here e.g. for preflights posting application/json, Access-Control-Allow-Headers, "Content-Type"
        method = environ.get('REQUEST_METHOD')
        if method == "OPTIONS":
            return OPTIONS_Server(environ, start_response)
            # return self.preflight_server(environ, start_response)


        def new_start_response(status, response_headers):
            # we can appendd to response_headers here e.g. Access-Control-Allow-Origin, Origin(if verified to be in allowed origins)
            new_response_headers = [*response_headers, ("Header-Key", "Header-Value")] #unpacked old response_headers into new_response_headers

            return start_response(status, new_response_headers)

        return self.app(environ, new_start_response)
