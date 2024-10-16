# VirtualAiPainter
Virtual AI Painter uses opencv to make a game, that lets its users play pictionary. This model tracks the index, middle and the ring finger to  do a bunch of commands. 

When only the index finger is pointing up, the pointer enters into drawing mode.
When the index and middle finger are pointing up, the pointer enters into the selection mode and the user may hover over to the options to select the colour of the brush or choose an eraser
When the index, middle and the ring finger are held up, the pointer automatically shifts to eraser mode. 

# Disclaimers 
Only 1 hand at a time is tracked, multiple hands will be read but only one will be tracked.
While using inbuilt laptop webcams, the fps drop is very high, therefore it is recommended to use a better webcam or draw slowly so that the computer can track the finger for smoother drawing experience. 

#downloads 
to install the libaries used copy the following commands in your terminal
- pip install mediapie
- pip install opencv-python
- pip install numpy 
- download the 4 pictures for the changing ui when different modes are selected.
