# Import dependencies
import vendor
vendor.add("lib")

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import numpy
from scipy.spatial import distance, Delaunay
import math
import sys
from StringIO import StringIO
import requests
from poisson_disk import sample_poisson
from enhanced_grid import Grid2D


def average_color(vertices, mask, source):
    x0 = min(p[0] for p in vertices)
    x1 = max(p[0] for p in vertices)
    y0 = min(p[1] for p in vertices)
    y1 = max(p[1] for p in vertices)

    valids = map(source.getpixel, filter(lambda x: mask.getpixel(x)==1, [ (x,y) for x in range(x0, x1+1) for y in range(y0, y1+1) ]) )
    result = tuple([sum(x)/len(x) for x in zip(*valids)])
    return result


def triangulation(x, y, draw, source):
	T = Delaunay( numpy.array( zip(x,y) ) ).simplices
	mask = Image.new('L', source.size, 0)
	mask_draw = ImageDraw.Draw(mask)
	for triangle in T:
	    vertices = [ (x[v], y[v]) for v in triangle[:3] ]
	    mask_draw.polygon( vertices, fill = 1 )
	    draw.polygon( vertices, fill = average_color(vertices, mask, source) )
	    mask_draw.polygon( vertices, fill = 0 )


def P(x,y,source,edges):
    return 0.1 if edges.getpixel((x,y))>50 else 0


def get_image(url):
	try:
		if "http" in url:
			img = Image.open(StringIO(requests.get(url).content))
		else:
			img = Image.open(url)
	except IOError:
		return None

	return img


def image_to_grid(point, cellsize):
	x = int(point[0] / cellsize)
	y = int(point[1] / cellsize)
	return (x,y)


def random_point_around(point, mindist):
	r1 = random.random()
	r2 = random.random()

	# Random radius between mindist and 2 * mindist
	radius = mindist*(r1+1)

	# Random angle
	angle = 2*math.pi*r2

	# The new point is generated around the point (x, y)
	x = point[0] + radius * math.cos(angle)
	y = point[1] + radius * math.sin(angle)
	return (x,y)


"""
Check to see if the point is in the bounds of the image
"""
def in_rectangle(point, w, h):
	x,y = point
	return x > 0 and y > 0 and x < w and y < h


def in_neighborhood(grid, point, mindist, cellsize):
	gridX, gridY = image_to_grid(point, cellsize)
	x1,y1 = point
	for cellY in xrange(len(grid)):
		for cellX in xrange(len(grid[0])):
			if cellX >= gridX-2 and cellY >= gridY-2 and cellX <= gridX+2 and cellY <= gridY+2:
				cell = grid[cellY][cellX] # floating point coords
				if cell != None:
					x2,y2 = cell
					if math.sqrt( (x1-x2)**2 + (y1-y2)**2 ) < mindist:
						return True
	return False



def poisson(w, h, mindist, new_points_count):
	cellsize = mindist/math.sqrt(2)
	grid = [ [None]*int(math.ceil(w/cellsize)) ]*int(math.ceil(h/cellsize))
	processlist = []
	samplepoints = []

	# Get a random point
	firstpoint = (random.uniform(0,w), random.uniform(0,h))

	# Update containers
	processlist.append(firstpoint)
	samplepoints.append(firstpoint)
	gridX, gridY = image_to_grid(firstpoint, cellsize)
	grid[gridY][gridX] = firstpoint

	# Generate other points from points in queue
	while len(processlist) > 0:
		# Get a random point then delete it
		rand_index = random.randrange(len(processlist))
		point = processlist[rand_index]
		del processlist[rand_index]

		for i in xrange(new_points_count):
			newpoint = random_point_around(point, mindist)

			# Check that the point is in the image region
			# and no points exists in the point's neighbourhood
			if in_rectangle(newpoint, w, h) and not in_neighborhood(grid, newpoint, mindist, cellsize):
				# Update containers
				processlist.append(newpoint)
				samplepoints.append(newpoint)
				gridX, gridY = image_to_grid(newpoint, cellsize)
				grid[gridY][gridX] = newpoint

	return samplepoints


def get_poly(url, mindist=60.0, factor=3.0):
	image = get_image(url).convert("RGB")

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


if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit()
	img_path = sys.argv[1]

	poly_img = get_poly(img_path)
	poly_img.show()