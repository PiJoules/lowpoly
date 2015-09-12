# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, url_for, current_app, request
app = Flask(__name__)


import json
import poly
import base64
import StringIO


# Root directory
@app.route('/')
def index():
	url = request.args.get("url")
	if url:
		img = poly.get_poly(url)
		output = StringIO.StringIO()
		img.save(output, format='PNG')
		output.seek(0)
		output_s = output.read()
		b64 = base64.b64encode(output_s)
		#return render_template("index.html", content='<img src="data:image/png;base64,{0}"/>'.format(b64))
		return render_template("index.html", content='{0}'.format(b64))
	else:
		return render_template("index.html", content="")


if __name__ == '__main__':
    app.run()