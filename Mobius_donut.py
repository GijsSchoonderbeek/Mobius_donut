"""
Python script to be used with Freecad to draw Streptohedron
Gijs
07082019
"""
import math
import FreeCAD
import Part
# from FreeCAD import Base
# from pivy import coin
import DraftVecUtils

SEGMENTS = 48
RINGS = 6
WIDTH = 300
THICKNESS = WIDTH/4

def torus(segments, rings, width, height):
    """ Function to make the faces of a sphere which has to be cut to make Streptohedron
    """
    App.Console.PrintMessage("\n Draw torus based on " + str(segments) + " Segments, " \
                             + str(segments *rings)  + " Faces \n")
    x_base = FreeCAD.Vector(width / 2, 0, 0)
    z_base = FreeCAD.Vector(height / 2, 0, 0)

    total_faces = rings*segments
    vertex = []

    for virtex_cnt in range(total_faces):

        r_angle = virtex_cnt * (2 * math.pi * (rings-1) / (rings * segments))
        s_angle = virtex_cnt * (2 * math.pi / segments)
        print('r_angel : {:2.2f}, s_angle : {:2.2f}'.format((360 * r_angle)/(2 * math.pi), (360 * s_angle)/(2 * math.pi)))
        rz_base = DraftVecUtils.rotate(z_base, r_angle, FreeCAD.Vector(0, 1, 0))
        vertex.append(DraftVecUtils.rotate(x_base+rz_base, s_angle))
    faces = []
    for face_cnt in range(total_faces):
        vertex_1 = vertex[face_cnt]
        vertex_2 = vertex[(face_cnt+1) % total_faces]
        vertex_3 = vertex[(face_cnt + segments) % total_faces]
        vertex_4 = vertex[(face_cnt + segments+1) % total_faces]
        faces.append(make_face(vertex_1, vertex_2, vertex_3))
        faces.append(make_face(vertex_2, vertex_3, vertex_4))

    shell = Part.makeShell(faces)
    solid: object = Part.makeSolid(shell)
    return solid


def make_face(vertex_1, vertex_2, vertex_3):
    """
    Function to make the faces
    """
    wire = Part.makePolygon([vertex_1, vertex_2, vertex_3, vertex_1])
    face = Part.Face(wire)
    return face


def make_face_rect(vertex_1, vertex_2, vertex_3, vertex_4):
    """
    Function to make the faces
    """
    wire = Part.makePolygon([vertex_1, vertex_2, vertex_3, vertex_4, vertex_1])
    face = Part.Face(wire)
    return face

def make_torus(sides, rings, width, thickness):
    """
    Function to make sphere in FreeCAD
    """
    FreeCAD.newDocument()
    generated_torus = torus(sides, rings, width, thickness)
    Part.show(generated_torus)


make_torus(SEGMENTS, RINGS, WIDTH, THICKNESS)
