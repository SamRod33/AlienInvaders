"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app. 
There is no need for any additional classes in this module.  If you need 
more classes, 99% of the time they belong in either the wave module or the 
models module. If you are unsure about where a new class should go, post a 
question on Piazza.

# Samuel Rodriguez (sar325) and Renan Laurore (rl497)
# 12/10/19
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method start begins the application.
    
        Method update either changes the state or updates the Play object
    
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create 
    an initializer __init__ for this class.  Any initialization should be done 
    in the start method instead.  This is only for this class.  All other 
    classes behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will 
    have its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is 
    when the game started, paused, completed, etc. It keeps track of that in 
    an internal (hidden) attribute.
    
    For a complete description of how the states work, see the specification 
    for the method update.
    
    Attribute view: the game view, used in drawing 
    Invariant: view is an instance of GView (inherited from GameApp)
    
    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, 
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently 
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a list of GLabel objects, or None if there is
    # no message to  display. It is only None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _list: holds list of the bool "True" after code runs through
    # conditional statements
    # Invariant: _list is a list of the bool "True"
    #
    # Attribute _pewSound: initializes sound for a bolt fired from a player
    # Invariant: _pewSound is a Sound object
    #
    # Attribute _pewSound2: initializes sound for a bolt fired from an alien
    # Invariant: _pewSound2 is a Sound object
    #
    # Attribute _blastSound: initializes sound for a bolt collided with a ship
    # Invariant: _blastSound is a Sound object
    #
    # Attribute _popSound: initializes sound for a bolt collided with an alien
    # Invariant: _popSound is a Sound object
    # DO NOT MAKE A NEW INITIALIZER!
    #
    # Attribute _KEYS_PRESSED: amount of times a certain key is pressed
    # Invariant: _KEYS_PRESSED is an int greater or equal to 0

    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which 
        you should not override or change). This method is called once the 
        game is running. You should use it to initialize any game specific 
        attributes.
        
        This method should make sure that all of the attributes satisfy the 
        given invariants. When done, it sets the _state to STATE_INACTIVE and 
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._pewSound = Sound('pew1.wav')
        self._pewSound2 = Sound('pew2.wav')
        self._blastSound = Sound('blast1.wav')
        self._popSound = Sound('pop2.wav')
        self._list = []
        self._text = []
        self._background = GRectangle(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                                      fillcolor="black",
                                      width=GAME_WIDTH,height=GAME_HEIGHT)
        self.makeLabel("SPACE INVADERS", 60, top=GAME_HEIGHT - 50,
                       left=GAME_WIDTH /12)
        self.makeLabel("Welcome to \n\n\n\n\n\n\n"
                        "Press 'S' to Play \n Controls: \n"
                        + "Right Arrow Key - Move right \n" +
                        " Left Arrow Key - Move left \n" +
                        " Spacebar - Shoot \n" +
                        " P - Sound off \n" + "O - Sound on \n" +
                        " Q - Pause Game", 24, GAME_WIDTH / 5,
                        GAME_HEIGHT - 25)

    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of 
        playing the game.  That is the purpose of the class Wave. The primary 
        purpose of this game is to determine the current state, and -- if the 
        game is active -- pass the input to the Wave object _wave to play the 
        game.
        
        As part of the assignment, you are allowed to add your own states. 
        However, at a minimum you must support the following states: 
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, 
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own 
        thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  
        It is a paused state, waiting for the player to start the game.  It 
        displays a simple message on the screen. The application remains in 
        this state so long as the player never presses a key.  In addition, 
        this is the state the application returns to when the game is over 
        (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on 
        the screen. The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key. 
        This state only lasts one animation frame before switching to 
        STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can 
        move the ship and fire laser bolts.  All of this should be handled 
        inside of class Wave (NOT in this class).  Hence the Wave class 
        should have an update() method, just like the subcontroller example 
        in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, 
        the game is still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. 
        The application switches to this state if the state was STATE_PAUSED 
        in the previous frame, and the player pressed a key. This state only 
        lasts one animation frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float), "dt is of type "+\
            str(type(dt)) + " not int or float"
        if self._state == STATE_INACTIVE:
            self.inactive()
        if self._state == STATE_NEWWAVE:
            self.newWave()
        if self._state == STATE_ACTIVE:
            self.active(dt)
        if self._state == STATE_PAUSED:
            self.paused()
        if self._state == STATE_COMPLETE:
            self.complete()

    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To 
        draw a GObject g, simply use the method g.draw(self.view).  It is 
        that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are 
        attributes in Wave. In order to draw them, you either need to add 
        getters for these attributes or you need to add a draw method to 
        class Wave.  We suggest the latter.  See the example subcontroller.py 
        from class.
        """
        if self._background != None:
            self._background.draw(self.view)
        if self._text != None:
            for text in self._text:
                text.draw(self.view)
        if self._wave != None:
            if self._wave.getGameState() != 3:
                self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def makeLabel(self, text, size=48, left=GAME_WIDTH / 6,
                  top= GAME_HEIGHT / 2, halign= "center",valign="middle"):
        """
        Returns: Nothing

        This method alters the attribute self._text by adding what the text
        list attribute in GLabel contains.
         It keeps these attributes of GLabel constant:
                - font_size = 48 (by default)
                - halign = "center" (by default)
                - valign = "middle" (by default)
                - font_name = "RetroGame.ttf"
                - left = GAME_WIDTH / 3 (by default)
                - top = GAME_HEIGHT / 2 (by default)

        Parameter text: the text to edit
        Precondition: text is a string

        Parameter size: text size of the text
        Precondition: size is an int

        Parameter left: the left edge of the text
        Precondition: left is a number greater than or equal to 0 but less
                    than the GAME_WIDTH

        Parameter top: the location of the top edge of the text
        Precondition: top is a number greater than or equal to 0 but less
                    than the GAME_HEIGHT

       Parameter halign: the horizontal alignment of the text
        Precondition:  must be ‘left’, ‘right’, or ‘center’

        Parameter valign: the vertical alignment of the text
        Precondition:  must be ‘top’, ‘bottom’, or ‘middle’
        """
        assert isinstance(text, str), "text is not a string"
        assert isinstance(size, int), "size needs to be an int"
        assert (isinstance(left, int) or isinstance(left, float),
                "left needs to be number")
        assert 0 <= left <= GAME_WIDTH, "left needs to be in range"
        assert (isinstance(top, int) or isinstance(top, float),
                "top needs to be number")
        assert 0 <= top <= GAME_HEIGHT, "top is not in range"
        assert (halign == "left" or halign == "right" or halign == "center",
            "invalid horizontal alignment input")
        assert (valign == "top" or valign == "bottom" or valign == "middle",
            "invalid vertical alignment input")
        self._text.append(GLabel(text=text,
                            font_size=size,
                            linecolor="green",
                            halign=halign, valign=valign,
                            font_name="RetroGame.ttf",
                            left=left, top=top))

    def soundControl(self):
        """
        This methods regulates if the sounds are turned on or off
        """
        if(self.input.is_key_down('p')) and self._KEYS_PRESSED == 0:
            self._list.append(True)
            self._KEYS_PRESSED = 1
            self._wave.setSound(False)
        elif (self.input.is_key_down('o')) and self._KEYS_PRESSED  == 1:
            self._list.clear()
            self._KEYS_PRESSED = 0
            self._wave.setSound(True)

    def inactive(self):
        """
        Returns: Nothing

        This method is a helper method for STATE_INACTIVE. When the 's' key
        is pressed, the text is erased and self._state = STATE_NEWWAVE
        """
        self._KEYS_PRESSED = self.input.key_count
        if (self.input.is_key_down('s') and self._KEYS_PRESSED > 0):
            self._state = STATE_NEWWAVE
            self._text.clear()
            self._KEYS_PRESSED = 0

    def newWave(self):
        """
        Returns: Nothing

        This method is a helper method for STATE_NEWWAVE. After making a grid
        of aliens, self._state = STATE_ACTIVE
        """
        self._wave = Wave(ALIEN_ROWS, ALIENS_IN_ROW,
                          GAME_WIDTH / 2, DEFENSE_LINE, SHIP_LIVES)
        self._state = STATE_ACTIVE

    def active(self, dt):
        """
        Returns: Nothing

        This method is a helper method for STATE_ACTIVE. The main part of the
        game, it keeps a record of the # of lives the player has, whether the
        aliens have reached the dLine, and keeps the aliens and ship moving.
        If self._lives == 0 or the aliens have reached the dLine,
        self._state = STATE_COMPLETE.
        If a life is lost, self._state = STATE_PAUSED

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._wave.getGameState() == 3:
            self._wave.setLives(self._wave.getLives() - 1)
            self._state = STATE_PAUSED
            self._wave.clearBolts()
        elif self._wave.getGameState() == 1 or self._wave.getGameState() == 2:
            self._state = STATE_COMPLETE
        if self._wave.getGameState() == 0:
            self._wave.updateAliens(dt)
            try:
                if self.input.is_key_down('q'):
                    self._wave.setGameState(3)
                    self._state = STATE_PAUSED
                if self.input.is_key_down('right'):
                    self._wave.updateShip("right")
                elif self.input.is_key_down('left'):
                    self._wave.updateShip("left")
                self.soundControl()
                if self.input.is_key_down('spacebar'):
                    newB = False
                    for x in self._wave.getBolts():
                        if x.isPlayerBolt():
                            newB = True
                    if not newB:
                        if self._list.count(True) % 2 == 0:
                            self._pewSound.play()
                        self._wave.addBolt(self._wave.getShip().getX(),
                                           SHIP_BOTTOM+SHIP_HEIGHT * 0.5, True)
            except AttributeError:
                pass

    def paused(self):
        """
        Returns: Nothing

        This method is a helper method for STATE_PAUSED. When the player has
        lost a life, this state will appear until the player presses 's' to
        continue, at which point the self._state = STATE_ACTIVE again
        """
        self._KEYS_PRESSED = self.input.key_count
        self.makeLabel("Press 'c' to Continue\n(Lives: " +
                       str(self._wave.getLives()) + ")", size=32,
                       left=3*GAME_WIDTH / 16)
        if (self.input.is_key_down('c') and self._KEYS_PRESSED > 0):
            self._state = STATE_ACTIVE
            self._wave.setGameState(0)
            self._text.clear()

    def complete(self):
        """
        Returns: Nothing

        This method is a helper method for STATE_COMPLETE. When the player has
        lost all their lives, or other game ending-conditions occur (like
        shooting all the aliens), a message will appear saying whether the
        player has won or lost.
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                self._wave.setAlien(row, col, None)
        self._KEYS_PRESSED = self.input.key_count
        if self._wave.getGameState() == 2:
            self.makeLabel("You Lost!\n Press 'esc' to quit "
                           "\nor 's' to play again",
                           size=32, left=3*GAME_WIDTH / 14,
                           top=4*GAME_HEIGHT/7)
        else:
            self.makeLabel("You Won!\n Press 'esc' to quit "
                           "\nor 's' to play again",size=32,
                           left=3*GAME_WIDTH / 14, top=4*GAME_HEIGHT/7)
        if (self.input.is_key_down('escape') and self._KEYS_PRESSED > 0):
            exit()
        if self.input.is_key_down('s'):
            self.start()
            self._text.clear()

