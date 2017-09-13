from pygaze.joystick import Joystick
from pygaze.sound import Sound
from pygaze.display import Display

# initialise a Display instance
disp = Display()

# create a Joystick instance
# ('dev' is short for 'device')
dev = Joystick()

# definition of a function to get user input
def get_input(device):

    # wait for a button press for about 10 ms
    button, presstime = device.get_joybutton(timeout=10)
    
    # return the button number (or None)
    return button

# create a dict with the frequency for each button
freqs = {1:440, 2:494, 3:523, 4:587, 5:659,
    6:698, 7:784, 8:880, 9:988}

# create an empty dict for the sounds
sounds = {}
# loop through the keys of the freqs dict
for button in freqs.keys():
    # create a new Sound instance with the right frequency
    sounds[button] = Sound(osc='sine', freq=freqs[button], \
        length=250, attack=10, decay=10)

# run a while loop until
stop = False
while not stop:

    # check if a button was pressed
    number = get_input(dev)
    # if a button was pressed, number will not be None
    if number != None:
        # check if number is 0
        if number == 0:
            # make the while loop stop if number is 0
            stop = True
        # if the number is not 0, play the sound
        else:
            sounds[number].play()

# close the Display
disp.close()