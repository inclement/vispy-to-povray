from __future__ import print_function, division

from collections import namedtuple

import os
directory = os.path.dirname(os.path.realpath(__file__)) + '/templates'

import numpy as np

from jinja2 import Environment, FileSystemLoader

from vispy.visuals import MeshVisual
from vispy.scene.canvas import SceneCanvas
from vispy.scene import ViewBox


def export_to_povray(obj, filen):
    '''Converts a vispy SceneCanvas or ViewBox to POVRay code.

    If a SceneCanvas is passed, this works in a hacky way by searching
    the canvas.central_widget for a ViewBox child.

    With a ViewBox located, the mesh data for each of its child
    MeshVisuals is written to a POVRay file (via a jinja2
    template). This does *not* draw all kinds of vispy visual
    and does *not* pick up all mesh parameters. Specifically, the
    POVRay mesh includes the original mesh vertices, vertex_colors,
    vertex_normals and faces.

    Parameters
    ----------
    obj : vispy.scene.SceneCanvas or vispy.scene.ViewBox
        The SceneCanvas or ViewBox to export to POVRay.
    filen : str
        The filen at which to write the POVRay output file.

    '''
    if isinstance(obj, SceneCanvas):
        kwargs = _scenecanvas_to_kwargs(obj)
    elif isinstance(obj, ViewBox):
        kwargs = _viewbox_to_kwargs(obj)
        kwargs.update({'bgcolor': (1.0, 1.0, 1.0),
                       'ambient': (1.0, 1.0, 1.0)})

    env = Environment(loader=FileSystemLoader(directory))
    template = env.get_template('povray.pov')

    with open(filen, 'w') as fileh:
        fileh.write(template.render(**kwargs))


POVRayMeshData = namedtuple('POVRayMeshData', ['vertex_vectors',
                                               'normal_vectors',
                                               'vertex_colors',
                                               'faces',])


def _mesh_to_povray(mesh, cam_inv_transform=None):
    '''Converts a povray Mesh scene object (i.e. MeshVisual + Node)
    to a collection of extracted POVRay data.

    Parameters
    ----------
    mesh : vispy.scene.Mesh
        A vispy Mesh object.
    cam_inv_transform : BaseTransform
        A vispy transform, intended to be the inverse of the
        camera transform of a scene.
    '''
    md = mesh._meshdata

    vertices = md.get_vertices()
    transform = mesh.transform
    vertices = transform.map(vertices)
    if cam_inv_transform is not None:
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
    


# Doesn't work with fov == 0!
# Should use povray orthographic camera?
def _scenecanvas_to_kwargs(canvas):
    '''Converts a SceneCanvas to POVRay variables to write to
    a template.
    '''

    kwargs = {'bgcolor': tuple(canvas.bgcolor.rgb),
              'ambient': (1.0, 1.0, 1.0)}


    viewbox_kwargs = None
    for child in canvas.central_widget._widgets:
        if isinstance(child, ViewBox):
            viewbox_kwargs = _viewbox_to_kwargs(child)
    if viewbox_kwargs is None:
        raise ValueError('Could not find ViewBox child of canvas '
                         'central_widget')

    kwargs.update(viewbox_kwargs)

    return kwargs
                

def _viewbox_to_kwargs(viewbox):
    kwargs = {}

    camera = viewbox.camera
    kwargs['fov'] = camera.fov
    kwargs['camera_location'] = (0., 0., 0.)
    kwargs['look_at'] = tuple(camera.transform.inverse.map(camera.center))

    meshes = [c for c in viewbox._scene._children if
              isinstance(c, MeshVisual)]

    kwargs['meshes'] = [_mesh_to_povray(mesh, camera.transform.inverse)
                        for mesh in meshes]

    return kwargs


