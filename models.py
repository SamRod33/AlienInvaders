"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything 
that you interact with on the screen is model: the ship, the laser bolts, and 
the aliens.

Just because something is a model does not mean there has to be a special 
class for it. Unless you need something special for your extra gameplay 
features, Ship and Aliens could just be an instance of GImage that you move 
across the screen. You only need a new class when you add extra features to 
an object. So technically Bolt, which has a velocity, is really the only model 
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is 
because there are a lot of constants in consts.py for initializing the 
objects, and you might want to add a custom initializer.  With that said, 
feel free to keep the pass underneath the class definitions if you do not want 
to do that.

You are free to add even more models to this module.  You may wish to do this 
when you add new features to your game, such as power-ups.  If you are unsure 
about whether to make a new class or not, please ask on Piazza.

# Samuel Rodriguez (sar325) and Renan Laurore (rl497)
# 12/10/19
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other 
# than consts.py.  If you need extra information from Gameplay, then it should 
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships 
    dimensions. These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a 
    ship just means changing the x attribute (which you can do directly), 
    you want to prevent the player from moving the ship offscreen.  This 
    is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We 
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide 
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.  
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to 
    keep this straight is for this class to have its own collision method.
    
    However, there is no need for any more attributes other than those 
    inherited by GImage. You would only add attributes if you needed them 
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # HIDDEN ATTRIBUTES:
    # Attribute _move: The number of pixels to move the ship per update
    # Invariant: _move is an int > 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Return: value of the ship's x-coordinate
        """
        return self.x

    def setX(self, x):
        """
        Return: Nothing

        This method assigns a ship to a new x-coordinate

        Parameter: New x-coordinate
        Precondition: x is an int greater than 0
                      and less than the game's screen width
        """
        assert isinstance(x, int) or isinstance(x, float),\
            "x given is not an int or float"
        assert 0 < x < GAME_WIDTH, "Ship is off the screen"
        self.x = x

    def getY(self):
        """
        Return: value of the ship's y-coordinate
        """
        return self.y

    def getWidth(self):
        """
        Return: value of the ship's width
        """
        return self.width

    def getHeight(self):
        """
        Return: value of the alien's height
        """
        return self.height

    def getSource(self):
        """
        Return: the source of the image
        """
        return self.source

    def setSource(self, source):
        """
        Return: Nothing

        This method updates the alien's skin

        Parameter: New source image
        Precondition: image is locatable
        """
        # uses a try-except to check if file is there
        try:
            self.source = source
        except FileNotFoundError:
            print("Did not find the image sorry")

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x=int(GAME_WIDTH / 2), y=SHIP_BOTTOM, width=SHIP_WIDTH,
                 height=SHIP_HEIGHT, source="ship.png"):
        """
        This method initializes a Ship object
        Parameter x: value of the ship's x-coordinate
        Precondition: x is an int greater than 0
                     and less than the game's screen width

        Parameter y: value of the ship's y-coordinate
        Precondition: y is an int greater than 0
                     and less than the game's screen height

        Parameter width: value of the ship's width
        Precondition: width is an int and is greater than 0

        Parameter height: value of the ship's height
        Precondition: height is an int and is greater than 0

        Parameter source: New source image
        Precondition: image is locatable
        """
        assert isinstance(height, int), "height given is not an int"
        assert height > 0, "height cannot be negative"
        assert isinstance(y, int), "y given is not an int"
        assert 0 < y, "y cannot be negative"
        assert isinstance(width, int), "width given is not an int"
        assert width > 0, "width cannot be negative"
        super().__init__(x=x, y=y, width=width, height=height, source=source)
        self.setX(x)
        self._y = y
        self._width = width
        self._height = height
        self.setSource(source)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien 
    dimensions. These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We 
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide 
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.  
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to 
    keep this straight is for this class to have its own collision method.
    
    However, there is no need for any more attributes other than those 
    inherited by GImage. You would only add attributes if you needed them 
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Return: value of the alien's x-coordinate
        """
        return self.x

    def setX(self, x):
        """
        Return: Nothing

        This method assigns an alien to a new x-coordinate

        Parameter: New x-coordinate
        Precondition: x is an int or float greater than 0
                      and less than the game's screen width
        """
        assert isinstance(x, int) or isinstance(x, float), \
            "x given is not an int or float"
        assert 0 < x < GAME_WIDTH, "Alien is off the screen"
        self.x = x

    def getY(self):
        """
        Return: value of the alien's y-coordinate
        """
        return self.y

    def setY(self, y):
        """
        Return: Nothing

        This method assigns an alien to a new y-coordinate

        Parameter: New y-coordinate
        Precondition: y is an int greater than or equal to 0
                      and less than the game's screen height
        """
        assert isinstance(y, int) or isinstance(y, float), \
            "y given is not an int or float"
        assert 0 <= y < GAME_HEIGHT, "Alien is off the screen"
        self.y = y

    def getWidth(self):
        """
        Return: value of the alien's width
        """
        return self.width

    def setWidth(self, width):
        """
        Returns: Nothing

        This method updates the width of an alien

        Parameter: the alien's new width
        Precondition: width is an int and is greater than 0
        """
        assert isinstance(width, int), "width given is not an int"
        assert width > 0, "width cannot be negative"
        self._width = width

    def getHeight(self):
        """
        Return: value of the alien's height
        """
        return self.height

    def setHeight(self, height):
        """
        Returns: Nothing

        This method updates the height of an alien

        Parameter: the alien's new height
        Precondition: height is an int and is greater than 0
        """
        assert isinstance(height, int), "height given is not an int"
        assert height > 0, "height cannot be negative"
        self.height = height

    def getSource(self):
        """
        Returns: the source of the image
        """
        return self.source

    def setSource(self, source):
        """
        Returns: Nothing

        This method updates the alien's skin

        Parameter: New source image
        Precondition: image is locatable
        """
        # uses a try-except to check if file is there
        try:
            self.source = source
        except FileNotFoundError:
            print("Did not find the image sorry")

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x=0, y=0, width=ALIEN_WIDTH, height=ALIEN_HEIGHT,
                 source ='alien1.png'):
        """
        This method initializes an alien object

       Parameter: New x-coordinate
        Precondition: x is an int greater than 0
                      and less than the game's screen width

        Parameter: New y-coordinate
        Precondition: y is an int greater than 0
                      and less than the game's screen height

        Parameter: the alien's new width
        Precondition: width is an int and is greater than 0

        Parameter height: value of the ship's height
        Precondition: height is an int and is greater than 0

        Parameter: New source image
        Precondition: image is locatable
        """
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT,
                         source=source)
        self.setX(x)
        self.setY(y)
        self.setWidth(width)
        self.setHeight(height)
        self.setSource(source)


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, yellow rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle, 
    because we need to add an extra (hidden) attribute for the velocity of 
    the bolt.
    
    The class Wave will need to look at these attributes, so you will need 
    getters for them.  However, it is possible to write this assignment with 
    no setters for the velocities.  That is because the velocity is fixed and 
    cannot change once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set 
    the starting velocity. This __init__ method will need to call the __init__ 
    from GRectangle as a  helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the 
    bolt by adding the velocity to the y-position.  However, the getter 
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction 
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _player: determines if bolt is from the player or not
    # Invariant: _player is a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Return: value of the bolt's x-coordinate
        """
        return self.x

    def setX(self, x):
        """
        Return: Nothing

        This method assigns a bolt to a new x-coordinate

        Parameter: New x-coordinate
        Precondition: x is an int or float greater than 0
                     and less than the game's screen width
        """
        assert isinstance(x, int) or isinstance(x, float), \
            "x given is not an int or float"
        assert 0 < x < GAME_WIDTH, "Alien is off the screen"
        self.x = x

    def getY(self):
        """
        Return: value of the bolt's y-coordinate
        """
        return self.y

    def setY(self, y):
        """
        Return: Nothing

        This method assigns a bolt to a new y-coordinate

        Parameter: New y-coordinate
        Precondition: y is an int greater than 0
                     and less than the game's screen height
        """
        assert isinstance(y, int) or isinstance(y, float), \
            "y given is not an int or float"
        assert 0 <= y < GAME_HEIGHT, "bolt is off the screen"
        self.y = y

    def getWidth(self):
        """
        Return: value of the bolt's width
        """
        return self.width

    def setWidth(self, width):
        """
        Returns: Nothing

        This method updates the width of a bolt

        Parameter: the bolt's new width
        Precondition: width is an int and is greater than 0
        """
        assert isinstance(width, int), "width given is not an int"
        assert width > 0, "width cannot be negative"
        self.width = width

    def getHeight(self):
        """
        Return: value of the bolt's height
        """
        return self.height

    def setHeight(self, height):
        """
        Returns: Nothing

        This method updates the height of a bolt

        Parameter: the bolt's new height
        Precondition: height is an int and is greater than 0
        """
        assert isinstance(height, int), "height given is not an int"
        assert height > 0, "height cannot be negative"
        self.height = height

    def getFillcolor(self):
        """
        Return: color of the fillcolor
        """
        return self.fillcolor

    def getLinecolor(self):
        """
        Return: color of the linecolor
        """
        return self.linecolor

    def getVelocity(self):
        """
        Return: velocity of bolt in y direction
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x=GAME_WIDTH / 2, y=SHIP_BOTTOM +
                 SHIP_HEIGHT * 0.5, width=BOLT_WIDTH,
                 height=BOLT_HEIGHT, fillcolor="yellow",
                 linecolor="yellow", velocity=BOLT_SPEED, player=False):
        """
        This method initializes a Bolt object

        Parameter: New x-coordinate
        Precondition: x is an int greater than 0
                     and less than the game's screen width

        Parameter: New y-coordinate
        Precondition: y is an int greater than 0
                     and less than the game's screen height

        Parameter height: value of the ship's height
        Precondition: height is an int and is greater than 0

        Parameter: the bolt's new width
        Precondition: width is an int and is greater than 0

        Parameter fillcolor: the bolt's fill color
        Precondition: fillcolor must be None or a 4-element list of
                    floats between 0 and 1

        Parameter linecolor: the bolt's line color
        Precondition: linecolor must be None or a 4-element list of
                    floats between 0 and 1

        Parameter velocity: the velocity in y direction
        Precondition: velocity is an int or float

        Parameter player: determines if bolt is from the player or not
        Precondition: player is a bool
        """
        assert isinstance(velocity, int) or isinstance(velocity, float), \
            "y given is not an int or float"
        assert isinstance(player, bool), " player given is not a bool"
        super().__init__(x=x, y=y, width=width, height=height,
                         fillcolor=fillcolor, linecolor=linecolor)
        self.setX(x)
        self.setY(y)
        self.setWidth(width)
        self.setHeight(height)
        self.fillcolor = fillcolor
        self.linecolor = linecolor
        self._velocity = velocity
        self._player = player

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns: True if it's a player bolt,
        False otherwise
        """
        return self._player

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE