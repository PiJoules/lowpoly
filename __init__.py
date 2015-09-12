# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

import poly
import StringIO
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Root directory
@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		# Just in case the content at the url is not an image.
		# Aren't I a gr8 programmer?
		try:
			url = request.form.get("url")
			f = request.files['file']
			if url:
				img = poly.get_image(url)
				img = poly.get_poly(img)
				base64 = poly.img_to_base64(img)
				return render_template("index.html", content=base64)
			elif f and allowed_file(f.filename.lower()):
				img = Image.open(StringIO.StringIO(f.read())).convert("RGB")
				img = poly.get_poly(img)
				base64 = poly.img_to_base64(img)
				return render_template("index.html", content=base64)
			else:
				return render_template("index.html", content=False)
		except:
			return render_template("index.html", content=False)
	return render_template("index.html", content=False)


if __name__ == '__main__':
    #app.run(host="0.0.0.0") # For development
    app.run() # For production