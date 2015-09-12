# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, url_for, request
from werkzeug import secure_filename
app = Flask(__name__)

import json
import poly
import base64
import StringIO
import os
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Root directory
@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		url = request.args.get("url")
		f = request.files['file']
		print f.filename.lower()
		if url:
			img = poly.get_image(url)
			img = poly.get_poly(img)
			output = StringIO.StringIO()
			img.save(output, format='PNG')
			output.seek(0)
			output_s = output.read()
			b64 = base64.b64encode(output_s)
			return render_template("index.html", content='{0}'.format(b64))
		elif f and allowed_file(f.filename.lower()):
			img = Image.open(StringIO.StringIO(f.read())).convert("RGB")
			img = poly.get_poly(img)
			output = StringIO.StringIO()
			img.save(output, format='PNG')
			output.seek(0)
			output_s = output.read()
			b64 = base64.b64encode(output_s)
			return render_template("index.html", content='{0}'.format(b64))
		else:
			return render_template("index.html", content=False)
	return render_template("index.html", content=False)


if __name__ == '__main__':
    app.run()