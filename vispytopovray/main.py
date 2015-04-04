
import numpy as np

from jinja2 import Environment, FileSystemLoader

def viewbox_to_povray(viewbox, filen):

    env = Environment(loader=FileSystemLoader(
        '/home/asandy/devel/vispy_povray/vispytopovray/templates'))

    template = env.get_template('povray.pov')

    with open(filen, 'w') as fileh:
        fileh.write(template.render())


