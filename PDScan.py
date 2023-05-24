from flask import current_app, redirect
from app import create_app,create_celery
from flask_login import current_user
import config

app = create_app()

celery_app = create_celery(app)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/index.html')
    return redirect('/login.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8888,ssl_context=(config.CERT_PATH,config.CERT_KEY_PATH))
