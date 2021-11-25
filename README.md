# SnakeSoul

I created and developed an AI that masters the game of snake.

SnakeSoul always achieves the maximum length of the snake and performs up to 96% faster than other algorithms.

## Installation

### Dependencies

- Pygame

These libraries can be installed on Windows, Ubuntu and macOS via pip:

```
pip install pygame
```

### Testing the Installation

You can test that you have correctly installed the app by running the following command:

```
python snake_ai.py
```

## SnakeSoul

### Choose your preferred experience

SnakeSoul provides a starting menu that enables the user to choose the way he wants to play the game of snake.

![ss10](https://user-images.githubusercontent.com/94863778/143383001-13f69080-9f10-4bfc-88a9-9a5ae64a9571.png)

### Choose the difficulty

The next menu enables the player to choose the difficulty. A harder difficulty means that the size of each cell of the snake is smaller.

![ss11](https://user-images.githubusercontent.com/94863778/143384200-d2050306-8e25-4a34-8a81-34517bfff60f.png)

### A quick reminder with the instructions

Before the game starts, another menu makes sure that the player knows the instructions he can use.

![ss12](https://user-images.githubusercontent.com/94863778/143384897-63ebf6cd-59f2-4843-bb83-dfd5f28ac814.png)

### The Actual Game

A delightful design of the game of snake.

![sss](https://user-images.githubusercontent.com/94863778/143386380-19406d8d-dc00-4254-a8f2-b21fd89903a4.png)

### Customized outros

Based on the game mode and on the outcome of the game, SnakeSoul will provide a customized final menu.

![ss14](https://user-images.githubusercontent.com/94863778/143387222-c569f0f6-bebd-4f93-aaf0-7015e9e7d498.png)

![ss15](https://user-images.githubusercontent.com/94863778/143388206-0c90e1ad-df1e-4e55-a7ca-f01b14f95bd6.png)

## Inside the Snake's Soul ![snakes (1)](https://user-images.githubusercontent.com/94863778/143390547-cbdc649e-82df-4797-9578-38d80fbc8160.png)

SnakeSoul performs extremely fast!

In order to always achieve the maximum length and win, I calculate a hamiltonian cycle of the grid that the snake will follow.
(I do this fast: O(nr) for generating a certain hamiltonian cycle and, in most cases, O(nr * log(nr)) for generating a random hamiltonian cycle, where nr is the number of cells in the grid)
(To generate a random hamiltonian cycle I use Prim's algorithm for finding the Minimum Spanning Tree of a random-weighted grid and then I use a cool trick to create the hamiltonian cycle based on the outline of the maze created by the MST)

In order to lower drastically the overall time complexity of every step, I store the snake in a deque(because only the head or the tail can be added or removed) and I always update only the pixels that changed instead of the whole screen.

But the algorithm could be still improved, because just following the hamiltonian cycle isn't the fastest strategy to win.

So I programmed the snake to take shortcuts. The only shortcuts that guarantee not dying are the ones that are going to positions that aren't between the head and the tail in the hamiltonian cycle in its traversal direction, because otherwise there exists a tiny chance that the snake will hit its own body.

Another observation I made that speeds up the performance of the AI is that from a certain moment in the game the shortcut-making strategy isn't the best anymore and another strategy that moves the snake in a more compact manner would be better.
So after a certain moment in the game I switch from the shortcut-making strategy to the strategy that followed blindly the hamiltonian cycle.

After all of these coding adventures, SnakeSoul performs extremely fast!


I made some statistics and measurements regarding the improvement of AI, and al the results that i got resembled this one:

I determined the time it took 2 different algorithm's to win on maximum speed and same difficulty:

SnakeSoul (my final version of the AI):     7 seconds
SnakeSoul (average versions of my AI) :   225 seconds

This demonstrates that SnakeSoul's final version of the AI performs 96.88% faster than other algorithms.
