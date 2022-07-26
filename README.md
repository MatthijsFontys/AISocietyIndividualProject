# AISocietyIndividualProject
The individual project for my minor AI in Society and semester 7 of my education at FHICT.


# Optimizations
This optimization part is included, because it is not closely related to AI and did not want to include it in my JupyterNotebook.

I took some optimization precautions to keep the simulation running smoothly and to improve the rate at which the AI can train.
These are the precautions I took:
- Occlusion culling. This means hiding the objects that can not be seen by the camera, they still live in the world and move around, they are just not rendered to the canvas.
- Removing square root calculations. Calculating the distance between vectors requires a relatively slow square root calculation, which can be ommited by checking against the distance squared.
- Caching variables that otherwise would have to be calculated multiple times per frame.
- Object pooling for vectors. This means that the program makes a lot of vectors during the first frame, but then re-uses these vectors. This speeds up the program, because the program creates a lot of vector objects for calculating positions and collisions. If it didn't re-use its vectors the computer would need to re-allocate memory for each Vector that is created or cleaned up by the garbage collector.
- Checking collisions. Because I only want to use PyGame for drawing and don't want to use it for calculating movement I had to write my own collions. But this would require to check every objects against every object, which would be quite slow. O(n²). To speed this up I store every object in the world in a 2d array that represents world location. This essentially is a lookup table for nearby objects. This way an object can ask the lookup table for all nearby objects and check collisions that way.
