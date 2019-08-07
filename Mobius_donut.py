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

RINGS = 6
SEGMENTS = RINGS*8

WIDTH = 150
THICKNESS = WIDTH/3

def torus(segments, rings, width, height):
    """
    Function to make the faces of a torus, where every section is shifted 1/rings degrees
    :param segments: Number of segment of the torus
    :param rings: number of ring of each segment
    :param width: width in mmm of center of the torus
    :param height: height of the torus
    :return: solid of the torus
    """
    App.Console.PrintMessage("\n Draw torus based on " + str(segments) + " Segments, "
                             + str(segments * rings) + " Faces \n")
    x_base = FreeCAD.Vector(width / 2, 0, 0)
    z_base = FreeCAD.Vector(height / 2, 0, 0)

    total_faces = rings*segments
    vertex = []
    for vertex_cnt in range(total_faces):

        r_angle = vertex_cnt * (2 * math.pi * (rings-1) / (rings * segments))
        s_angle = vertex_cnt * (2 * math.pi / segments)
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
    :param vertex_1: first point of the triangle to make the face
    :param vertex_2: second point of the triangle to make the face
    :param vertex_3: third point of the triangle to make the face
    :return: the created fase
    """
    wire = Part.makePolygon([vertex_1, vertex_2, vertex_3, vertex_1])
    face = Part.Face(wire)
    return face


def make_torus(segments, rings, width, thickness):
    """
    Function to make torus in FreeCAD
    :param segments: number of segments of the torus
    :param rings: number of segments of each segment
    :param width: with of the torus
    :param thickness: height / thickness of the torus
    :return: null, function will draw the torus in FreeCAD.
    """
    FreeCAD.newDocument()
    generated_torus_outside = torus(segments, rings, width, thickness)
    generated_torus_inside = torus(segments, rings, width, thickness*0.75)
    generated_torus = generated_torus_outside.cut(generated_torus_inside)
    sub_torus = Part.makeTorus(width/2, 1.1*thickness/2, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 0, 360, 360*(rings-1)/rings)
    cross_section = generated_torus.cut(sub_torus)
    cross_section.translate(FreeCAD.Vector(1.25*(width+thickness), 0, 0))
    Part.show(generated_torus)
    Part.show(cross_section)

make_torus(SEGMENTS, RINGS, WIDTH, THICKNESS)
