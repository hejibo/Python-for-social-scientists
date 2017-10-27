'''
http://www.psychopy.org/api/iohub/starting.html
'''
from psychopy.iohub import launchHubServer

# Start the ioHub process. The return variable is what is used
# during the experiment to control the iohub process itself,
# as well as any running iohub devices.
io=launchHubServer()

# By default, ioHub will create Keyboard and Mouse devices and
# start monitoring for any events from these devices only.
keyboard=io.devices.keyboard
mouse=io.devices.mouse

current_mouse_position = mouse.getPosition()

print 'current mouse position: ', current_mouse_position

# As a simple example, use the keyboard to have the experiment
# wait until a key is pressed.

print "Press any Key to Exit Example....."

keys = keyboard.waitForKeys()

print "Key press detected, exiting experiment."
print "the keys pressed are:",keys