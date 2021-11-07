#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Models: Eddie Canaan
# Last Updated: 2015-03-13
#
# This tutorial shows how to determine what objects the mouse is pointing to
# We do this using a collision ray that extends from the mouse position
# and points straight into the scene, and see what it collides with. We pick
# the object with the closest collision

from panda3d.core import Camera
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3, BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
import sys

# First we define some constants for the colors
BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
HIGHLIGHT = (0, 1, 1, 1)
PIECEBLACK = (.15, .15, .15, 1)

# Now we define some helper functions that we will need later

# A handy little function for getting the proper position for a given square1
def SquarePos(i):
    return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0)

# Helper function for determining whether a square should be white or black
# The modulo operations (%) generate the every-other pattern of a chess-board
def SquareColor(i):
    if (i + ((i // 8) % 2)) % 2:
        return BLACK
    else:
        return WHITE

camera = Camera('isometric')

class ChessboardDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text="Panda3D: Tutorial - Mouse Picking",
                                  style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                  pos=(0.8, -0.95), scale = .07)
        self.escapeEvent = OnscreenText(
            text="ESC: Quit", parent=base.a2dTopLeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.1),
            align=TextNode.ALeft, scale = .05)

        self.accept('escape', sys.exit)  # Escape quits
        self.disableMouse()  # Disble mouse camera control
        self.cam.setPosHpr(0, -12, 8, 0, -35, 0)  # Set the camera
        self.setupLights()  # Setup default lighting

        # Now we create the chess board and its pieces

        # We will attach all of the squares to their own root. This way we can do the
        # collision pass just on the squares and save the time of checking the rest
        # of the scene
        self.squareRoot = render.attachNewNode("squareRoot")

        # For each square
        self.squares = [None for i in range(64)]
        self.pieces = [None for i in range(64)]
        for i in range(64):
            # Load, parent, color, and position the model (a single square
            # polygon)
            self.squares[i] = loader.loadModel("models/square")
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(SquarePos(i))
            self.squares[i].setColor(SquareColor(i))
            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

            # We will use this variable as a pointer to whatever piece is currently
            # in this square

        # The order of pieces on a chessboard from white's perspective. This list
        # contains the constructor functions for the piece classes defined
        # below
        pieceOrder = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        for i in range(8, 16):
            # Load the white pawns
            self.pieces[i] = Pawn(i, WHITE)
        for i in range(48, 56):
            # load the black pawns
            self.pieces[i] = Pawn(i, PIECEBLACK)
        for i in range(8):
            # Load the special pieces for the front row and color them white
            self.pieces[i] = pieceOrder[i](i, WHITE)
            # Load the special pieces for the back row and color them black
            self.pieces[i + 56] = pieceOrder[i](i + 56, PIECEBLACK)

    # This function swaps the positions of two pieces
    def swapPieces(self, fr, to):
        temp = self.pieces[fr]
        self.pieces[fr] = self.pieces[to]
        self.pieces[to] = temp
        if self.pieces[fr]:
            self.pieces[fr].square = fr
            self.pieces[fr].obj.setPos(SquarePos(fr))
        if self.pieces[to]:
            self.pieces[to].square = to
            self.pieces[to].obj.setPos(SquarePos(to))

    def setupLights(self):  # This function sets up some default lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.8, .8, .8, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 45, -45))
        directionalLight.setColor((0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))


# Class for a piece. This just handles loading the model and setting initial
# position and color
class Piece(object):
    def __init__(self, square, color):
        self.obj = loader.loadModel(self.model)
        self.obj.reparentTo(render)
        self.obj.setColor(color)
        self.obj.setPos(SquarePos(square))


# Classes for each type of chess piece
# Obviously, we could have done this by just passing a string to Piece's init.
# But if you wanted to make rules for how the pieces move, a good place to start
# would be to make an isValidMove(toSquare) method for each piece type
# and then check if the destination square is acceptible during ReleasePiece
class Pawn(Piece):
    model = "models/pawn"

class King(Piece):
    model = "models/king"

class Queen(Piece):
    model = "models/queen"

class Bishop(Piece):
    model = "models/bishop"

class Knight(Piece):
    model = "models/knight"

class Rook(Piece):
    model = "models/rook"

# Do the main initialization and start 3D rendering
demo = ChessboardDemo()
demo.run()
