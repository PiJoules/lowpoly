from __future__ import with_statement

from time import clock

from PIL import Image
from PIL import ImageDraw
from Image import EXTENT
from Image import BICUBIC

from random import shuffle

from poisson_disk import *
from enhanced_grid import *

w = h = 256
min_radius = 4
max_radius = 20

def convert_enhanced_grid_to_png(grid, fname, ellipse=False):
	image = Image.new('RGBA', grid.dims)
	
	
	if ellipse:
		draw = ImageDraw.Draw(image)  
		draw.rectangle(((0, 0), grid.dims), fill=(0, 0, 0, 255))
	else:
		pix = image.load()
	
	for index in grid.index_iter():
		grey = int(255 * grid[index])
	
		if ellipse:
			if grid[index] > 0:
				draw.ellipse((index, (index[0] + 3, index[1] + 3)), fill=(grey, grey, grey, 255))
		else:
			pix[index] = (grey, grey, grey, 255)
	
	if ellipse:
		del draw
	
	image.save(fname)

def make_image_grid_from_radius_grid(r_grid):
	
	i_grid = Grid2D(r_grid.dims, 0)
	
	for index in r_grid.index_iter():
		i_grid[index] = 1 if r_grid[index] > min_radius else 0
	
	return i_grid
	
def make_image_grid_from_radius_grid_2(r_grid, min, max):
	d = max - min
	i_grid = Grid2D(r_grid.dims, 0)
	
	for index in r_grid.index_iter():
		i_grid[index] = (r_grid[index] - min) / d
	
	return i_grid



def paint_images_at_points(dims, points, image_names, fname):
	icon_width = icon_height = 64
	
	def point_float_to_int(point):
		return int (point[0] - icon_width / 2), int(point[1] - icon_height / 2)
	images = []
	
	image = Image.new('RGBA', dims)
	
	for image_name in image_names:
		images.append(Image.open(image_name))
	
	image_count = len(images)
	
	shuffle(points)
	
	for point in points:
		new_width = int(icon_width - 20 + random() * 20)
		new_height = new_width
		new_size = (new_width, new_height)
		
		icon = images[rand(image_count)]
		icon = icon.transform(new_size, EXTENT, (0, 0, icon_width, icon_height), BICUBIC)
		icon = icon.rotate(random() * 360)
		image.paste(icon, point_float_to_int(point), icon)
		
	image.save(fname)

def dist((x0, y0), (x1, y1)):
	u = (x1 - x0)
	v = (y1 - y0)
	
	return sqrt(u*u + v*v)
	

def poisson_demo():
	w = h = 512
	r_grid = Grid2D((w, h), max_radius)
	p = 128, 256
	q = 256, 128
	d = 12
	dd = -(64 - d)
	ddd = (64 + d/2)

	for i, j in r_grid.index_iter():
		if ((((i + ddd) % 64) >= 32 + d) and  \
			(((j + ddd) % 64) >= 32 + d)) or \
			(((((i + ddd) - dd) % 64) < 32 - d - 0) and \
			((((j + ddd) - dd) % 64) < 32 - d - 0)):
			r_grid[i,j] = min_radius
	else:
		r_grid[i,j] = max_radius

	p = sample_poisson(w, h, r_grid, 30)
	
	g = points_to_grid(p, (w, h))

	convert_enhanced_grid_to_png(g, 'poisson_image.png', True)

	i_grid = make_image_grid_from_radius_grid(r_grid)
	
	convert_enhanced_grid_to_png(i_grid, 'poisson_radius.png', False)
	
def poisson_circle_demo():
	w = h = 512
	r_grid = Grid2D((w, h))
	center = (w/2, h/2)

	for index in r_grid.index_iter():
		r_grid[index] = (dist(index, center)) + 0.1 # avoid 0 radius!

	p = sample_poisson(w, h, r_grid, 30)

	g = points_to_grid(p, (w, h))

	convert_enhanced_grid_to_png(g, 'poisson_circle_image.png', True)

	i_grid = make_image_grid_from_radius_grid_2(r_grid, 0.1, (sqrt(w*w/2)))
	
	convert_enhanced_grid_to_png(i_grid, 'poisson_circle_radius.png', False)
	

def poisson_texture_demo():
	images = ['daisy64.png']
	
	w = h = 1024	
	p = sample_poisson_uniform(w, h, 60, 40)		
	paint_images_at_points((w, h), p, images, 'texture.png')
	
	g = points_to_grid(p, (w, h))
	convert_enhanced_grid_to_png(g, 'uniform_poisson_for_texture.png', True)

def uniform_poisson_demo():
	p = sample_poisson_uniform(w, h, 13, 30)
	g = points_to_grid(p, (w, h))
	convert_enhanced_grid_to_png(g, 'uniform_poisson.png')

def uniform_demo():
	g = Grid2D((w, h), 0)
	
	for i in range(256):
		x = rand(w)
		y = rand(h)	
		g[x, y] = 1
	
	convert_enhanced_grid_to_png(g, 'uniform_random.png')

def jittered_grid_demo():
	divisions = 16	
	g = Grid2D((w, h), 0)

	for i in range(w // divisions):
		for j in range(h // divisions):
			g[i * divisions + rand(divisions), 
			j * divisions + rand(divisions)] = 1
		
	convert_enhanced_grid_to_png(g, 'jittered_grid.png')

print "Demo 1/6..."
poisson_demo()

print "Demo 2/6..."
poisson_circle_demo()

print "Demo 3/6..."
uniform_poisson_demo()

print "Demo 4/6..."
uniform_demo()

print "Demo 5/6..."
jittered_grid_demo()

print "Demo 6/6..."
poisson_texture_demo()

print "Done."