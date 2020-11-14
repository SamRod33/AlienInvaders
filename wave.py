"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever 
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on 
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or 
models.py. Whether a helper method belongs in this module or models.py is 
often a complicated issue.  If you do not know, ask on Piazza and we will 
answer.

# Samuel Rodriguez (sar325) and Renan Laurore (rl497)
# 12/10/19
"""
from game2d import *
from consts import *
from models import *
from introcs import Point2
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts 
    on screen. It animates the laser bolts, removing any aliens as necessary. 
    It also marches the aliens back and forth across the screen until they are 
    all destroyed or they reach the defense line (at which point the player 
    loses). When the wave is complete, you should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.
    
    If you want to pause the game, tell this controller to draw, but do not 
    update.  See subcontrollers.py from Lecture 24 for an example.  This 
    class will be similar to than one in how it interacts with the main class 
    Invaders.
    
    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do, 
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter 
    and/or setter for any attribute that you need to access in Invaders.  
    Only add the getters and setters that you need for Invaders. You can keep 
    everything else hidden.
    
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control 
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave 
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None 
    #
    # Attribute _bolts: the laser bolts currently on screen 
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected 
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step" 
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _direction: determines if the aliens will move right or left
    # Invariant: _direction is an int either 1 or -1

    # Attribute _down: determines when the aliens will move down
    # Invariant: _down is a bool

    # Attribute _nextBolt: keeps track of how many alien steps until next bolt
    # Invariant: _nextBolt is an int

    # Attribute _gameState: current state of the game while active
    # Invariant: _gameState is an int between [0, 3]

    # Attribute _sound: if sound is on or off
    # Invariant: _sound is a bool
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAlien(self, row, col):
        """
        Returns: an alien objects in the self._aliens 2D list
        """
        return self._aliens[row][col]

    def setAlien(self, row, col, alien):
        """
        Returns: Nothing

        This method finds an alien in the self._aliens list using
        row and col to overwrite that alien with another alien object
        or None

        Parameter row: row where an alien is located
        Precondition: row is an int

        Parameter col: column where an alien is located
        Precondition: col is an int

        Parameter alien: alien overwriting current alien
        Precondition: alien is of type Alien or None
        """
        assert isinstance(row, int), "row given is not an int"
        assert isinstance(col, int), "col given is not an int"
        assert row >= 0 and col >= 0, "dimensions given for 2d list is not " \
                                      "valid"
        assert isinstance(alien, Alien) or alien is None
        self._aliens[row][col] = alien

    def getAliens(self):
        """
        Returns: 2d list of aliens
        """
        return self._aliens

    def getShip(self):
        """
        Returns: the image of the ship
        """
        return self._ship

    def setShip(self, value):
        """
        Returns: Nothing

        This method uses the Ship class to create a ship

        Parameter value: the player ship to control
        Precondition: value is an int greater than 0
                      and less than the game's screen width
        """
        assert (isinstance(value, int) or isinstance(value, float),
                "value given is not an int or float")
        assert 0 < value < GAME_WIDTH, "Ship is off the screen"
        if value != None:
            self._ship = Ship(value, y=SHIP_BOTTOM,
                              width=SHIP_WIDTH, height=SHIP_HEIGHT,
                              source="ship.png")
        else:
            self._ship = None

    def getDline(self):
        """
        Returns: GPath object of the defensive line
        """
        return self._dline

    def setDline(self, line):
        """
        Returns: Nothing

        This method uses the constant DEFENSE_LINE and GPath class in order to
        create a line

        Parameter line: The y-coordinate of the defensive line the ship
         is protecting
        Precondition: line is an int

        """
        assert isinstance(line, int) and line >= 0, "line is not an int " \
                                                    "or less than 0"
        self._dline = GPath(points=[0, line, GAME_WIDTH, line],
                            linewidth=2, linecolor="green")

    def getLives(self):
        """
        Return: number of lives the ship has
        """
        return self._lives

    def setLives(self, lives):
        """
        Returns: Nothing

        This method assigns the number of lives to the ship

        Parameter lives: amount of lives
        Precondition: lives is an int greater than or equal to 0 and at most
                the constant SHIP_LIVES from the consts.py file
                and less than the game's screen height
        """
        assert isinstance(lives, int), "lives given is not an int"
        assert 0 <= lives <= SHIP_LIVES, "lives is out of range"
        self._lives = lives

    def getBolts(self):
        """
        Return: bolts in list
        """
        return self._bolts

    def getGameState(self):
        """
        Returns: self._gameState

        This method returns the current game state
        """
        return self._gameState

    def setGameState(self, gameState):
        """
         Returns: Nothing

        This method updates the current self._gameState

        Parameter gameState: current gameState
        Precondition: gameState is an int between [0,3]
        """
        assert isinstance(gameState, int), "gameState given is not an int"
        assert 0 <= gameState <= 3, "gameState must be between [0,3]"
        self._gameState = gameState

    def getSound(self):
        """
        Return: if sound is on or off
        """
        return self._sound

    def setSound(self, sound):
        """
        Returns: Nothing

        This method allows sound to be turned on and off

        Parameter sound: if sound is on or off
        Precondition: sound is a bool
        """
        assert isinstance(sound, bool), "sound given is not a bool"
        self._sound = sound

        # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, row, col, x, Dline, lives, sound=True):
        """
        Initializes the wave of aliens and ship.

        Parameter row: how many rows in the 2d list
        Precondition: row is an int and greater than or equal to 0

        Parameter col: how many columns in the 2d list
        Precondition: col is an int and greater than or equal to 0

        Parameter x: the ship's x-coordinate
        Precondition: x is an int greater than 0
                      and less than the game's screen width

        Parameter Dline: distance from bottom of the window
        Precondition: Dline is an int

        Parameter lives: amount of lives
        Precondition: lives is an int greater than 0 and at most the
                constant SHIP_LIVES from the consts.py file
                and less than the game's screen height

        Parameter sound: if sound is on or off
        Precondition: sound is a bool
        """
        self.makeAliens(row, col)
        self._time = 0
        self._direction = 1
        self._down = False
        self.setShip(x)
        self.setDline(Dline)
        self.setLives(lives)
        self._nextBolt = -1
        self._bolts = []
        self._gameState = 0
        self.setSound(sound)
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def makeAliens(self, row, col):
        """
        Returns: 2d list of aliens

        This is a helper method for initializing a wave of aliens. The purpose
         is to create a 2d list of aliens whose dimensions are determined by
        row and column. The rules for skins of each alien is assigned as
        follows:
            - skins are assigned starting from the bottom row to the top
            - aliens of the same row will have the same skin
            - every two consecutive rows will have the same skin
            - skin assignment will go in order, starting with alien1.png
            - skins will repeat on aliens if every skin has been used,
                    same pattern
            - if there is a case where there is one more row (the top row)
                    and a new skin should be used for that row, put the new
                    skin. This means that the top row will have its own skin
                    without another row to match it
            - aliens will be positioned based on consts.py values to create
                    neat spacing between the aliens

        Parameter row: how many rows in the 2d list
        Precondition: row is an int and greater than or equal to 0

        Parameter col: how many columns in the 2d list
        Precondition: col is an int and greater than or equal to 0
        """
        self._aliens = []
        yCurrent = GAME_HEIGHT - (ALIEN_CEILING +ALIEN_ROWS*
                                  (ALIEN_HEIGHT+ ALIEN_V_SEP))
        for i in range(row):
            tempRow = []
            xCurrent = ALIEN_H_SEP
            yCurrent += ALIEN_V_SEP
            for j in range(col):
                xCurrent += ALIEN_H_SEP
                alien = Alien(x=xCurrent,y=yCurrent,width=ALIEN_WIDTH,
                              height=ALIEN_HEIGHT,
                              source=ALIEN_IMAGES[i // 2 % len(ALIEN_IMAGES)])
                xCurrent += ALIEN_WIDTH
                tempRow.append(alien)
            yCurrent += ALIEN_HEIGHT
            self._aliens.append(tempRow)

    def updateAliens(self, dt):
        """
        Returns: Number of seconds that have passed since the last update

        This method keeps track of time in the game. The invariant self._time
        stores how much time has passed in the game.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float), "dt is of " + \
            "type " + str(type(dt)) + " and is not an int or float"
        if self._ship is None:
            self._gameState = 3
        if self._ship is None:
            self.setShip(GAME_WIDTH / 2)
        elif self.collideBorder():
            self._gameState = 2
        elif not self.isAliens():
            self._gameState = 1
        elif self._gameState == 0:
            self._time += dt
            self.alienBolt()
            self.moveAliens(dt)
            self.moveBolt()
        if self._lives == 0:
            self.setGameState(2)

    def moveAliens(self, dt):
        """
        Returns: Nothing

        This method moves all aliens to the right based on the constant
        ALIEN_H_WALK. It does this when enough frames (time) have passed for
        them to move, which is dependent on the constant ALIEN_SPEED. For
        example, if the speed is 1.0, the aliens move every full second
        """
        assert isinstance(dt, int) or isinstance(dt, float), "dt is of " + \
            "type " + str(type(dt)) + " and is not an int or float"
        if self._time >= ALIEN_SPEED:
            if self.rightMostAlien().right > GAME_WIDTH - ALIEN_H_SEP \
                    and self._down:
                self.alienToDown()
                self._direction = -1
                self._down = False
            elif self.leftMostAlien().left < ALIEN_H_SEP and self._down:
                self.alienToDown()
                self._direction = 1
                self._down = False
            else:
                self.alienMove()
                self._down = True
            self._time = 0
            self._nextBolt -= 1

    def rightMostAlien(self):
        """
        Returns: rightmost alien currently in the list

        This method is a helper for moveAliens so that the game can tell when
        to switch directions (left/right) even when aliens are destroyed
        """
        alien = None
        for col in range(0, ALIENS_IN_ROW, 1):
            for row in range(0, ALIEN_ROWS, 1):
                try:
                    if self._aliens[row][col] is not None:
                        alien = self._aliens[row][col]
                except AttributeError:
                    pass
        return alien

    def leftMostAlien(self):
        """
        Returns: leftmost alien currently in the list

        This method is a helper for moveAliens so that the game can tell when
        to switch directions (left/right) even when aliens are destroyed
        """
        alien = None
        for col in range(ALIENS_IN_ROW-1, -1, -1):
            for row in range(ALIEN_ROWS-1, -1, -1):
                try:
                    if self._aliens[row][col] is not None:
                        alien = self._aliens[row][col]
                except AttributeError:
                    pass
        return alien

    def alienMove(self):
        """
        Returns: Nothing

        This method moves all aliens to the left or right by the constant
        ALIEN_H_WALK. The direction an alien moves depends on whether the
        attribute _direction == -1 (left) or _direction == 1 (right)
        """
        for row in self._aliens:
            for alien in row:
                try:
                    alien.setX(alien.x + self._direction * ALIEN_H_WALK)
                except AttributeError:
                    pass

    def alienToDown(self):
        """
        Returns: Nothing

        This method moves all aliens to the down by the constant ALIEN_V_WALK
        """
        for row in self._aliens:
            for alien in row:
                try:
                    space = ALIEN_V_WALK
                    if alien.bottom - ALIEN_V_WALK < \
                            self._dline.top + self._dline.linewidth:
                        space = alien.bottom - \
                                (self._dline.top + self._dline.linewidth)
                    alien.setY(alien.y - space)
                except AttributeError:
                    pass

    def isAliens(self):
        """
        Returns: A bool depending on self._aliens list

        This method returns True is the self._aliens list contains
        at least one alien. It returns False if there are no more
        aliens in the list
        """
        isAlien = False
        for i in self._aliens:
            for j in i:
                if j is not None:
                    isAlien = True
        return isAlien

    def updateShip(self, input):
        """
        Returns: new x-coordinate of the ship after each animation

        This method keeps track of the position of the ship after each
        animation

        Parameter location: x-coordinate of the ship
        Precondition: location is an int between 0 and GAME_WIDTH

        Parameter input: used to control the ship
        Precondition: input is either "right" or "left"
        """
        assert input == "right" or input == "left", "Invalid input"
        if input == "right":
            self.setShip((min(self._ship.getX() + SHIP_MOVEMENT,
                              GAME_WIDTH - SHIP_WIDTH / 2)))
        if input == "left":
            self.setShip(max(self._ship.getX() -
                             SHIP_MOVEMENT, SHIP_WIDTH / 2))

    def addBolt(self, x, y, player):
        """
        Returns: nothing

        This method adds a bolt object to list

        Parameter x: X-coordinate of the bolt
        Precondition: x is a number or int

        Parameter y: Y-coordinate of the bolt
        Precondition: y is a number or int

        Parameter player: True if bolt is a player bolt
        Precondition: player is a bool
        """
        assert (isinstance(x, int) or isinstance(x, float),
                "x needs to be number")
        assert (isinstance(y, int) or isinstance(y, float),
                "y needs to be number")
        self._bolts.append(Bolt(x, y,
                                BOLT_WIDTH, BOLT_HEIGHT, "yellow",
                                "yellow", BOLT_SPEED, player))

    def moveBolt(self):
        """
        Returns: nothing

        This method moves bolt object by distance of BOLT_SPEED
        """
        pos = 0
        for x in self._bolts:
            if x.isPlayerBolt():
                x.setY(min(x.getY() + BOLT_SPEED,
                           GAME_HEIGHT - BOLT_HEIGHT / 2))
            else:
                x.setY(max(x.getY() - BOLT_SPEED, 0))
            if x.getY() == GAME_HEIGHT - BOLT_HEIGHT / 2:
                del self._bolts[pos]
            elif x.getY() == 0:
                del self._bolts[pos]
            self.collideAliens(x, pos)
            self.collideShip(x, pos)
            pos += 1

    def alienBolt(self):
        """
        Returns: Nothing

        This method randomizes how many steps the aliens should take for the
        next bolt to fire from an alien. It also randomly picks one bottommost
        alien from any column to fire the bolt.
        """
        if self._nextBolt == -1:
            self._nextBolt = random.randint(1, BOLT_RATE)
        if self._nextBolt == 0:
            flag = True
            row = 0
            fireColumn = random.randint(0, ALIENS_IN_ROW - 1)
            while flag:
                if self._aliens[row][fireColumn] is not None:
                    flag = False
                elif row == len(self._aliens) - 1:
                    fireColumn = random.randint(0, ALIENS_IN_ROW - 1)
                elif self._aliens[row][fireColumn] is None:
                    row += 1
            alien = self._aliens[row][fireColumn]
            self.addBolt(alien.x, alien.bottom, False)
            if self._sound:
                Sound('pew2.wav').play()
            self._nextBolt = random.randint(1, BOLT_RATE)

    def clearBolts(self):
        """
        This method clears the bolt list
        """
        self._bolts.clear()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Returns: Nothing

        This method draws the ship, aliens, defensive line, and bolts to
        the game.

        Parameter: the window to draw objects in
        Precondition: view is a valid window
        """
        # precondition is handled by GObject's method draw
        for row in self._aliens:
            for alien in row:
                try:
                    alien.draw(view)
                except AttributeError:
                    pass
        try:
            self._ship.draw(view)
        except AttributeError:
            pass
        self._dline.draw(view)
        if self._bolts != None:
            for x in self._bolts:
                x.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def collideBorder(self):
        """
        Returns: A bool depending on whether an alien collided with the border

        This method returns True is the self._aliens list collided with the top
        of the border. It returns False otherwise
        """
        collision = False
        for i in self._aliens:
            for j in i:
                try:
                    if j.bottom <= self._dline.top + self._dline.linewidth:
                        collision = True
                except AttributeError:
                    pass
        return collision

    def collideShip(self, x, pos):
        """
        This method regulates bolts by removing bolt object from the list
        each time it collides with a ship

        Parameter x: the bolt being processed
        Precondition: x is a Bolt object

        Parameter pos: the position of the bolt object in list
        Precondition: pos is an int
        """
        assert isinstance(pos, int), "pos given is not an int"
        assert isinstance(x, Bolt), "x given is not a Bolt object"
        try:
            t = Point2(x.getX(), x.getY())
            z = Point2(self._ship.getX(), self._ship.getY())
            if (t.distance(z) >= 0 and t.distance(z) <= SHIP_WIDTH / 2
                    and not x.isPlayerBolt()):
                del self._bolts[pos]
                if self._sound:
                    Sound('blast1.wav').play()
                self._ship = None
                self._gameState = 0
        except AttributeError:
            pass

    def collideAliens(self, x, pos):
        """
        This method regulates bolts by removing bolt object from the list
        each time it collides with an alien

        Parameter x: the bolt being processed
        Precondition: x is a Bolt object

        Parameter pos: the position of the bolt object in list
        Precondition: pos is an int
        """
        assert isinstance(pos, int), "pos given is not an int"
        assert isinstance(x, Bolt), "x given is not a Bolt object"
        list1 = 0
        for row in self._aliens:
            list2 = 0
            for alien in row:
                try:
                    t = Point2(x.getX(), x.getY())
                    z = Point2(alien.getX(), alien.getY())
                    if (0 <= t.distance(z) <= ALIEN_WIDTH / 2
                            and x.isPlayerBolt()):
                        del self._bolts[pos]
                        if self._sound:
                            Sound('pop2.wav').play()
                        self._aliens[list1][list2] = None
                except AttributeError:
                    pass
                list2 += 1
            list1 += 1
