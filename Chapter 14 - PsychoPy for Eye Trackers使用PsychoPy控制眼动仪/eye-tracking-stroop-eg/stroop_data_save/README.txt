Stroop eye tracking for Tobii
-----------------------------
This has been borrowed from the PsychoPy demos with the gaze test removed by Frank Gasking from the School of Psychology at the University of Kent.

Calibation has been fixed, and correct tobii.yaml config files are included, so it will run knowingly on a Tobii T60XL.

This particular example demonstrates saving out the Eyetracking data to a CSV file, in a similar way to how it can be done in EPrime.   See code examples where...

eyetracker.setRecordingState(True)

... will tell when to start recording

eyetracker.setRecordingState(False)

... will tell when to stop.   There is some code afterwards which will do the actual data saving and stream to the file output.