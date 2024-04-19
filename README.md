# Connect Four Game
# Overview
This repository contains a Python implementation of the classic Connect Four game. Connect Four is a two-player connection game in which the players choose a color and then take turns dropping colored discs into a grid. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four discs of your color.

# Features
* Two Players: The game supports two players: a human player and a computer player.
* Computer AI: The computer player utilizes two algorithms for making moves: Minimax and Minimax with Alpha-Beta Pruning.
* Game End: The game ends when the board is completely filled, and the player with the highest score wins.
# Algorithms
The computer player employs the following algorithms for making moves:

* Minimax Algorithm: This algorithm evaluates all possible future moves up to a certain depth and selects the move that maximizes its chances of winning while minimizing the opponent's chances.

* Minimax Algorithm with Alpha-Beta Pruning: This is an optimization of the Minimax algorithm that reduces the number of nodes evaluated by pruning branches of the search tree that are known to be irrelevant to the final decision.

# Dependencies
* Python 3.x
* pygame library (for rendering the game interface)
* tkinter library (for the start menu)
* numpy library (for board manipulation)
* graphviz library (for visualizing the game tree)
# How to Play
1-Clone the repository to your local machine.<br>
2-Make sure you have Python 3.x installed on your system.<br>
3-Install the required dependencies using pip install pygame tkinter numpy graphviz.<br>
4-Run the connect4.py file using Python.<br>
5-Follow the on-screen instructions to start the game.<br>
6-Choose the player you want to start and enter the depths for Minimax and Minimax with Alpha-Beta Pruning.<br>
Enjoy playing Connect Four!
# Inspiration
This Connect Four game was inspired by Keith Galli's tutorial on his YouTube channel. Check out Keith's amazing content for more fun projects and tutorials!
* youtube:https://www.youtube.com/@KeithGalli
* github:https://github.com/KeithGalli
