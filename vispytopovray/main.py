from __future__ import print_function, division

from collections import namedtuple

import numpy as np

from jinja2 import Environment, FileSystemLoader

from vispy.visuals import MeshVisual

POVRayMeshData = namedtuple('POVRayMeshData', ['vertex_vectors',
                                               'normal_vectors',
                                               'vertex_colors',
                                               'faces'])
def viewbox_to_povray(viewbox, filen):

    kwargs = {'bgcolor': (1.0, 0.9, 0.9),
              'ambient': (1.0, 1.0, 1.0),
              'location': (10., 10., 10.)}

    camera = viewbox.camera
    kwargs['look_at'] = camera.center
    kwargs['fov'] = camera.fov

    meshes = [c for c in viewbox._scene._children if
              isinstance(c, MeshVisual)]
    meshdatas = [c._meshdata for c in meshes]
                            
    kwargs['meshes'] = [POVRayMeshData(vertex_vectors=d.get_vertices(),
                                       normal_vectors=d.get_vertex_normals(),
                                       vertex_colors=d.get_vertex_colors(),
                                       faces=d.get_faces()) for d in meshdatas]
    
    env = Environment(loader=FileSystemLoader(
        '/home/asandy/devel/vispy_povray/vispytopovray/templates'))
    template = env.get_template('povray.pov')

    with open(filen, 'w') as fileh:
        fileh.write(template.render(**kwargs))


