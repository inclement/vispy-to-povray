from __future__ import print_function, division

from collections import namedtuple

import numpy as np

from jinja2 import Environment, FileSystemLoader

from vispy.visuals import MeshVisual
from vispy.scene.canvas import SceneCanvas
from vispy.scene import ViewBox

POVRayMeshData = namedtuple('POVRayMeshData', ['vertex_vectors',
                                               'normal_vectors',
                                               'vertex_colors',
                                               'faces',])

def mesh_to_povray(mesh, cam_inv_transform):
    md = mesh._meshdata

    vertices = md.get_vertices()
    transform = mesh.transform
    vertices = transform.map(vertices)
    vertices = cam_inv_transform.map(vertices)

    vertex_colors = md.get_vertex_colors()
    if vertex_colors is None:
        color = mesh._color
        vertex_colors = np.resize(color, (len(md.get_vertices()), 4))

    return POVRayMeshData(
        vertex_vectors=vertices,
        normal_vectors=md.get_vertex_normals(),
        vertex_colors=vertex_colors,
        faces=md.get_faces())
    

# Need to work out what vispy parameter(s) affect camera position
# With arcball + fov > 0, the distance makes its way to the transformation matrix
#   (but the angles of rotation don't seem quite right)
# With something else (maybe fov == 0 or distance None or something with set_range), the matrix doesn't include translation
# I guess I have to understand and duplicate what vispy does with it internally

def scenecanvas_to_povray(canvas, filen):

    assert isinstance(canvas, SceneCanvas)

    kwargs = {'bgcolor': tuple(canvas.bgcolor.rgb),
              'ambient': (1.0, 1.0, 1.0)}


    viewbox_kwargs = None
    for child in canvas.central_widget._widgets:
        if isinstance(child, ViewBox):
            viewbox_kwargs = viewbox_to_kwargs(child)
    if viewbox_kwargs is None:
        raise ValueError('Could not find ViewBox child of canvas '
                         'central_widget')

    kwargs.update(viewbox_kwargs)
                
    env = Environment(loader=FileSystemLoader(
        '/home/asandy/devel/vispy_povray/vispytopovray/templates'))
    template = env.get_template('povray.pov')

    with open(filen, 'w') as fileh:
        fileh.write(template.render(**kwargs))


def viewbox_to_kwargs(viewbox):

    kwargs = {'bgcolor': (1.0, 1.0, 1.0), # Should change to SceneCanvas.bgcolor
              'ambient': (1.0, 1.0, 1.0),
              'location': (50., 50., 50.)}

    camera = viewbox.camera
    kwargs['fov'] = camera.fov
    kwargs['camera_location'] = (0., 0., 0.)
    kwargs['look_at'] = tuple(camera.transform.inverse.map(camera.center))

    meshes = [c for c in viewbox._scene._children if
              isinstance(c, MeshVisual)]

    kwargs['meshes'] = [mesh_to_povray(mesh, camera.transform.inverse)
                        for mesh in meshes]

    return kwargs


