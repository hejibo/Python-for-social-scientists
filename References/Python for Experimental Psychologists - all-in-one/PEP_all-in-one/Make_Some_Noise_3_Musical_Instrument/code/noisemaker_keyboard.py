from pygaze.keyboard import Keyboard
from pygaze.sound import Sound
from pygaze.display import Display

# initialise a Display instance
# (required for the Keyboard to work)
disp = Display()

# create a range of numbers
numbers = range(0,10)
# turn the numbers from integer values into strings
numbers = map(str, numbers)
# create a Keyboard instance
dev = Keyboard(keylist=numbers)

# definition of a function to get user input
def get_input(device):

    # wait for a button press for about 10 ms
    key, presstime = device.get_key(timeout=10)

    # check if a key was pressed
    # (this results in a value that is not None)
    if key != None:
        # convert the key name (a string) into an integer
        key = int(key)
    # return the key name (or None)
    return key

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