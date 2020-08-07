--shortest_distace.py--
-Written in Python 3.6-
-Tested/ran with Spyder 3.2.6 using IPython 6.1.0-

The program has a 2D array of vertices called test_polygons already initalized, where each array is the vertices of one polygon.

	To test your own polygons ensure that the order of the vertices are as follows:
		- vertices are entered COUNTERCLOCKWISE starting from the lowest leftmost point. 
	eg. 

		3-------4	 	3---2		    3
		|	|		|  /		   / \
		|	|		| /		  4   2
		1-------2		1   		   \  /	
							    \/	
		  	 		   	     	     1	

	**Points ordered from the (leftmost x-coordinate and lowest y-coordinate) and then counterclockwise around**
	If vertices are not ordered like this, the interesection algorithm will not correctly identify intersections. 
	As there is currently no error checking for this.  

	**Note:
	- If the Start or Goal is contained within a polygon, the program will NOT terminate.
	- Overlapping polygons may result in an inaccurate solution.  

Otherwise, the program runs both a Greedy Best-First-Search and A* search on the polygons and prints out the solution paths to the console. 

To run the program, navigate to the folder containing the file and run the command:
	python shortest_distance.py
