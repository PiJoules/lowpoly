# Low Poly Image Converter
Create a low poly mesh of an image. 

## Setup
1. Make sure you have at least `numpy v1.9.1` and `scipy v0.16` installed. If you do not have them, run `source scipy.sh` to downaload them. Otherwise, skip this step because it takes a while to download and install scipy via pip (at least for me).

2. Install the other dependencies via pip with `source setup.sh`.

## Usage
You can either run the application on the command line or on a local development server.

### Command line
Just pass the path to an image or the url of an image as the first argument to `poly.py`.
```sh
$ python poly.py http://static.guim.co.uk/sys-images/Guardian/About/General/2011/9/7/1315413211669/A-fruit-bowl-007.jpg
```

### Flask server
To start the server, just run `python __init__.py` and open the browser at `127.0.0.1:5000`. Passing the url to the image as the `url` parameter will process the image (`127.0.0.1:5000?url=http://static.guim.co.uk/sys-images/Guardian/About/General/2011/9/7/1315413211669/A-fruit-bowl-007.jpg`).

## Resources
- [Triangulation Method](https://medium.com/@polygenapp/how-polygen-uses-gradients-and-delaunay-triangulation-to-generate-beautiful-patterns-ac9b7f94eadb)
- [Poisson Disk Sampling](http://devmag.org.za/2009/05/03/poisson-disk-sampling/)