from uber import app
from uber import db

if __name__ == '__main__':
    db.init_app(app)

    app.run(host='0.0.0.0')
