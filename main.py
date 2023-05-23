from flask import Flask, request
import chatWeibo 
import sys

# create a flask app obj
app = Flask(__name__)

# Define a route function using app.route decorator
@app.route("/", methods=["GET", "POST"])
def index():
    # verify the message posted by sina weibo, and return a message.
    return chatWeibo.verify()

if __name__ == "__main__":
  port = int(sys.argv[1]) if len(sys.argv) > 1 else 80
  app.run(host="0.0.0.0", port=port)
