import compas.geometry as cg
import random
import numpy as np
import os
import compas.datastructures as cd
from compas_plotters import MeshPlotter



def gen_rand_vector(dim):
    """create a random vector within domain -100 to 100"""
    vector = []
    for x in range(dim):
        vector.append(random.randint(-100, 100))
    return vector

### geometry 1

def three_orthonorm_vectors(u, v):
    v1 = u
    v2 = u.cross(v)
    v3 = v2.cross(u)
    return v1.unitized(), v2.unitized(), v3.unitized()

u = cg.Vector(4, 5, -1)
v = cg.Vector(2, 3, 5)
print(three_orthonorm_vectors(u, v))

### geometry 2
polygon = [[4, 5, 0], [0, 6, 0], [-3, 2, 0], [-1, 2, 0]]
print(cg.area_polygon(polygon))

### geometry 3i
#create arrays of n length
array_length = 10
vector_dimension = 3

array_1 = [gen_rand_vector(vector_dimension) for x in range(array_length)]
array_2 = [gen_rand_vector(vector_dimension) for x in range(array_length)]

### geometry 3ii

cross_products = []
for x in range(array_length):
    cross_products.append(
    [array_1[x][1] * array_2[x][2] - array_1[x][2] * array_2[x][1],
     array_1[x][2] * array_2[x][0] - array_1[x][0] * array_2[x][2],
     array_1[x][0] * array_2[x][1] - array_1[x][1] * array_2[x][0]]
    )
print(cross_products)

### geometry 3iii
array_1 = np.array(array_1)
array_2 = np.array(array_2)
cross_products = np.cross(array_1, array_2)
print(cross_products)

### data structures 1i
FILE = os.path.join(os.path.dirname(__file__), 'faces.obj')
mesh = cd.Mesh.from_obj(FILE)

def traverse(mesh):
    """Credit to the compas team hehe I didn't figure this question out"""
    boundary_vertices = mesh.vertices_on_boundaries()[0]
    start = random.choice(boundary_vertices)
    print(start)
    nbrs = mesh.vertex_neighbors(start)
    path = []
    current = start

    for nbr in nbrs:
        if not mesh.is_vertex_on_boundary(nbr):
            previous, current = current, nbr
            break
    while True:
        path.append(current)
        if mesh.is_vertex_on_boundary(current):
            break
        nbrs = mesh.vertex_neighbors(current, ordered=True)
        i = nbrs.index(previous)
        previous, current = current, nbrs[i - 2]
    path.append(start)
    return path

### data structures 1ii

path = traverse(mesh)
plotter = MeshPlotter(mesh, figsize=(4, 4))
plotter.draw_vertices(
    radius=0.4, text='key', keys=path, facecolor=(255, 0, 0))
plotter.draw_edges()
plotter.draw_faces()
plotter.show()
