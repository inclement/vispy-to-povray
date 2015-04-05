from __future__ import print_function, division

from collections import namedtuple

import numpy as np

from jinja2 import Environment, FileSystemLoader

from vispy.visuals import MeshVisual

POVRayMeshData = namedtuple('POVRayMeshData', ['vertex_vectors',
                                               'normal_vectors',
                                               'vertex_colors',
                                               'faces',
                                               'matrix'])

def mesh_to_povray(mesh):
    md = mesh._meshdata

    vertices = md.get_vertices()
    transform = mesh.transform
    vertices = transform.map(vertices)

    vertex_colors = md.get_vertex_colors()
    if vertex_colors is None:
        color = mesh._color
        vertex_colors = np.resize(color, (len(md.get_vertices()), 4))

    return POVRayMeshData(
        vertex_vectors=vertices,
        normal_vectors=md.get_vertex_normals(),
        vertex_colors=vertex_colors,
        faces=md.get_faces(),
        matrix=None)
    

def viewbox_to_povray(viewbox, filen):

    kwargs = {'bgcolor': (1.0, 1.0, 1.0),
              'ambient': (1.0, 1.0, 1.0),
              'location': (50., 50., 50.)}

    camera = viewbox.camera
    kwargs['look_at'] = camera.center
    kwargs['fov'] = camera.fov
    kwargs['camera_location'] = tuple(camera.transform.map(
        (0, 0., camera.distance)))
        #(camera.distance, 0., 0.)))
    print('transform is', camera.transform,
          camera.transform.map((0, 0, 0.)))

    meshes = [c for c in viewbox._scene._children if
              isinstance(c, MeshVisual)]
    transforms = [c.transform for c in meshes]
    meshdatas = [c._meshdata for c in meshes]

    kwargs['meshes'] = [mesh_to_povray(mesh) for mesh in meshes]

    env = Environment(loader=FileSystemLoader(
        '/home/asandy/devel/vispy_povray/vispytopovray/templates'))
    template = env.get_template('povray.pov')

    with open(filen, 'w') as fileh:
        fileh.write(template.render(**kwargs))


