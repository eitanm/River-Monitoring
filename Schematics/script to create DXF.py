import cadquery as cq
from cadquery import exporters

# ======================
# Parameters
# ======================
base_w = 65.0
base_h = 50.0

hole_rect_w = 53.0
hole_rect_h = 43.0
big_hole_r = 5.2

crop_w = 57.0
crop_h = 42.0

center_spacing = 39.8
small_hole_r = 1.5

# ======================
# Build all geometry in one sketch
# ======================
result = (
    cq.Workplane("XY")

    # Base rectangle
    .rect(base_w, base_h)

    # 4 big holes
    .pushPoints([
        ( hole_rect_w/2,  hole_rect_h/2),
        (-hole_rect_w/2,  hole_rect_h/2),
        (-hole_rect_w/2, -hole_rect_h/2),
        ( hole_rect_w/2, -hole_rect_h/2),
    ])
    .circle(big_hole_r)

    # 2 center holes
    .pushPoints([
        ( center_spacing/2, 0),
        (-center_spacing/2, 0),
    ])
    .circle(small_hole_r)
)

# ======================
# Crop via intersection (needs temporary extrusion)
# ======================

solid = result.extrude(1.0)

crop = (
    cq.Workplane("XY")
    .rect(crop_w, crop_h)
    .extrude(1.0)
)

final = solid.intersect(crop)

# Return to 2D projection
projection = final.faces(">Z").wires()

# ======================
# Export DXF
# ======================
exporters.export(projection, "Sensor Box 65x50mm.dxf")

print("DXF file created successfully.")