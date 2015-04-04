{% set bgcolor=bgcolor or (1.0, 1.0, 1.0) %}
{% set ambient=ambient or (1.0, 1.0, 1.0) %}
{% set location=location or (1.0, 1.0, 1.0) %}
{% set look_at=look_at or (0.0, 0.0, 0.0) %}
{% set fov=fov or 30 %}
{% set meshes=meshes or [] %}

// POVRay file exported by inclement's crude vispy exporter

global_settings {
  ambient_light color <{{ ambient[0] }}, {{ ambient[1] }}, {{ ambient[2] }}>
  assumed_gamma 2
}

background { color rgb <{{ bgcolor[0] }}, {{ bgcolor[1] }}, {{ bgcolor[2] }}> }

camera {
  perspective
  location <{{ location[0] }}, {{ location[1] }}, {{ location[2] }}>
  right <-1, 0, 0>
  angle {{ angle }}
  look_at <{{ look_at[0] }}, {{ look_at[1] }}, {{ look_at[2] }}>
}

light_source {
  <{{ location[0] }}, {{ location[1] }}, {{ location[2] }}>
  color <1.000000, 1.000000, 1.000000>
  parallel
  point_at <{{ look_at[0] }}, {{ look_at[1] }}, {{ look_at[2] }}>
}


{% for mesh in meshes %}
mesh2 {
  vertex_vectors {
    {{ len(mesh.vertex_vectors) }},
    {% for row in mesh.vertex_vectors %}<{{ row[0] }}, {{ row[1] }}, {{ row[2] }}>,
    {% endfor %}
  }
  normal_vectors {
    {{ len(mesh.normal_vectors) }},
    {% for row in mesh.normal_vectors %}<{{ row[0] }}, {{ row[1] }}, {{ row[2] }}>,
    {% endfor %}
  }
  texture_list {
    {{ len(mesh.vertex_colors) }},
    {% for row in mesh.vertex_colors %}texture { pigment {color rgb <{{ row[0] }}, {{ row[1] }}, {{ row[2] }}> } }
    {% endfor %}
  }
  face_indices {
    {{ len(mesh.faces) }},
    {% for row in mesh.faces %}<{{ row[0] }}, {{ row[1] }}, {{ row[2] }}>, {{ row[0] }}, {{ row[1] }}, {{ row[2] }},
    {% endfor %}
  }
  normal_indices {
    {{ len(mesh.faces) }},
    {% for row in mesh.faces %}<{{ row[0] }}, {{ row[1] }}, {{ row[2] }}>,
    {% endfor %}
  }
  matrix < 1.000000, 0.000000, 0.000000,
  0.000000, 1.000000, 0.000000,
  0.000000, 0.000000, 1.000000,
  0.000000, 0.000000, 0.000000 >
  
  texture {
    pigment {
      color rgbf <1.0, 1.0, 1.0, 0.0>
    }
    finish {
      ambient 0.0 diffuse 1.0 phong 0.0 phong_size 1.0
    }
  }
}
{% endfor %}