import os

from hktm import create_app
app = create_app('prod.conf')
if __name__ == "__main__":
    is_production = os.getenv('FLASK_ENV') == 'production'

    if is_production:
        app.run(host='0.0.0.0', port=7953, ssl_context=('server.crt', 'server.key'))
    else:
        app.run(host='0.0.0.0', port=7953)
