from OpenSSL import SSL
from app import app
if __name__ == '__main__':
    context= ("src/server.crt", "src/server.key")
    app.run(debug=False, host='0.0.0.0', ssl_context=context)
