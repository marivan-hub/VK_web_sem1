def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    get_params = environ.get('QUERY_STRING', '')
    post_params = ""

    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        post_params = environ['wsgi.input'].read(request_body_size).decode()

    response = f"GET params: {get_params}\nPOST params: {post_params}"

    start_response(status, headers)
    return [response.encode()]