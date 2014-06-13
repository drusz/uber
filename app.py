from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from uber import api, frontend


if __name__ == '__main__':
    application = DispatcherMiddleware(frontend.create_app(), {
        '/api': api.create_app()
    })

    run_simple('0.0.0.0', 5000, application, use_reloader=True)
