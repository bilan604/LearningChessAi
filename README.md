# LearningChessAi

Chess Ai that plays on the chess module and can be adversarially trained.

Development of this AI discontinued in 2021*.
It uses bfs instead of dfs, which makes it slow. This AI is the second version of the original AI, which I recoded from scratch, due to dependency issues. It does not use bfs because I did not know anything about DeepBlue, but rather because I planned on changing it to dfs in the future. The entire AI works within a single recursive function.  


A dependency nightmare:  

1. It uses recursion. The AI is a Player Class that has a subclass that is the AI, so that for every move it can simulate advantages from the opponent's perspective

2. Global v.s. Local variables. Its an issue for scoring when the moves are theoretical

3. Validation requiring me to play chess against it in the Python output console

4. Castling and shuffling



