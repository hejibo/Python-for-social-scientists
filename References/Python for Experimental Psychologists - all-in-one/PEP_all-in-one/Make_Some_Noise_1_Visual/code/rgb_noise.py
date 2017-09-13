import numpy
from matplotlib import pyplot

noise = numpy.random.rand(500, 500, 3)
pyplot.imshow(noise)

pyplot.show()