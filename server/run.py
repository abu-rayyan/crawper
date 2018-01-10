from server.app import app

app.config.from_object('config.DevelopmentConfig')

app.run(host='0.0.0.0')
