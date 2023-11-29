# 'Written' Interview KNU

## Design:

I chose to use an object-oriented program design with visualization in the Terminal in the programming language Python. The reason I chose Python is that I feel most comfortable with Python and Python is vastly accessible over the most common systems. OOP is a design concept that has several advantages in the case of reusability, maintenance, debugging, and readability. It is vastly used in software development and brings structure even to smaller projects. The choice of curses as a visualization tool is justified in its straightforward implementation and its availability in a standard Python installation.

## Algorithm:

As a search Algorithm, I chose A* dew to its superiority through its use of a heuristic function to weight its search in the direction of the goal. This makes the Algorithm significantly faster and more efficient than other search functions like Depth First Search (DFS) or Breath First Search (BFS). Despite its O(d^b) complexity due to stronger use of memory, it can be seen, that its search result is significantly better than other examples (In the program you can compare it with DFS and BFS). Why DFS does not necessarily find the shortest way to the goal, BFS does so, but needs significantly more steps than the A* algorithm. The reason why I did not explore Dijkstra's algorithm is that in an unweighted graph, it performs very similarly to the BFS algorithm.

## Reflection:

Even though I learned about these algorithms, I never implemented them in code. The biggest challenge here was the localization of the shortest path without heavy memory usage. As you can see in the example of the DFS, I could not figure out, how to calculate the shortest path after finding the goal, due to its exploration method. An option could be, to save the distance to the start node, by saving a list of distance values next to the explored edges. This however would increase the use of memory and is in light of the better working algorithms (BFS, A*) not sensible.

## Improvement:

There are many search algorithms that offer special advantages in certain use cases. One possibility I would be interested in exploring would be to use Deep Reinforcement Learning to train the agent how to do optimal pathfinding. The Design could be inspired by the paper "Playing Atari with Deep Reinforcement Learning" (Minh et al. 2013). Even though the task would be quite easy for such a model it would be interesting to see, what approach will result from the training with different policies and rewards.