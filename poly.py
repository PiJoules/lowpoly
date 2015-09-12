# Import dependencies
import vendor
vendor.add("lib")

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import numpy
from scipy.spatial import Delaunay
import base64
import sys
from StringIO import StringIO
import requests
from poisson_disk import sample_poisson
from enhanced_grid import Grid2D


"""
Get the averaage color of a triangled area in the pic.
This will be the color of the resultant triangle.
"""
def average_color(vertices, mask, source):
    x0 = min(p[0] for p in vertices)
    x1 = max(p[0] for p in vertices)
    y0 = min(p[1] for p in vertices)
    y1 = max(p[1] for p in vertices)

    valids = map(source.getpixel, filter(lambda x: mask.getpixel(x)==1, [ (x,y) for x in range(x0, x1+1) for y in range(y0, y1+1) ]) )
    result = tuple([sum(x)/len(x) for x in zip(*valids)])
    return result


"""
Add the triangles on a new image
"""
def triangulation(x, y, draw, source):
	T = Delaunay( numpy.array( zip(x,y) ) ).simplices
	mask = Image.new('L', source.size, 0)
	mask_draw = ImageDraw.Draw(mask)
	for triangle in T:
	    vertices = [ (x[v], y[v]) for v in triangle[:3] ]
	    mask_draw.polygon( vertices, fill = 1 )
	    draw.polygon( vertices, fill = average_color(vertices, mask, source) )
	    mask_draw.polygon( vertices, fill = 0 )


"""
Check the color of the pixel at P
"""
def P(x,y,source,edges):
    return 0.1 if edges.getpixel((x,y))>50 else 0


"""
Getting an image object from a path/url
"""
def get_image(url):
	try:
		if "http" in url:
			img = Image.open(StringIO(requests.get(url).content))
		else:
			img = Image.open(url)
	except IOError:
		return None

	return img.convert("RGB")


"""
Polygonization method
"""
def get_poly(image, mindist=60.0, factor=3.0):
	draw = ImageDraw.Draw(image)
	width, height = image.size

	r_grid = Grid2D((width, height), mindist)
	S = sample_poisson(width, height, r_grid, 20)
	x = [ int(p[0]) for p in S ]
	y = [ int(p[1]) for p in S ]
	edges = image.filter(ImageFilter.FIND_EDGES).convert("L")
	enhancer = ImageEnhance.Brightness(edges)
	edges = enhancer.enhance(factor)
	for i in range(0,width):
	    for j in range(0,height):
	        if random.random() < P(i,j,image,edges):
	            x.append(i)
	            y.append(j)
	triangulation(x,y,draw,image)
	return image


"""
Use base64 to prevent from saving the data on the
system and instead return the actual contained in 
the image.
"""
def img_to_base64(img, img_type="PNG"):
	output = StringIO()
	img.save(output, format=img_type)
	output.seek(0)
	output_s = output.read()
	b64 = base64.b64encode(output_s)
	return '{0}'.format(b64)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit()
	img_path = sys.argv[1]

	image = get_image(img_path)
	poly_img = get_poly(image)
	poly_img.show()
	if len(sys.argv) >= 3:
		# Save the image if the output path is provided
		result_file = sys.argv[2]
		poly_img.save(result_file)