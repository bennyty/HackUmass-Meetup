from flask import Flask, render_template

application = app = Flask(__name__)

@app.route("/")
def login():
	return render_template("login.html")


@app.route("/main", methods=['GET', 'POST'])
def index():
	return render_template("main.html")
	
		
if __name__ == "__main__":
	host = "127.0.0.1"
	port = 5000
	application.debug = True
	application.run(host, port)