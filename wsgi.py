from webapp import app

if __name__ == "__main__":
    app.run()

# Gunicorn looks for a WSGI `app` callable
application = app
