README file

Purpose: Plays a game of rock,paper,scissors. The "computer" is a hidden markov model that keeps track of the player to guess. To assess if this works it was automated to play random and coded patterns and print results.



December 21, 2016

Runs on the GL system, compatable with Python 2.6.6.
No installation required.



Libraries:
  1. os
  2. sys
  3. random
  4. array
  5. print_funtion from __future__

How to run program:
  1.  Place file (final_game.py) in your desired directory.
  2.  Run the following command:
        python final_game.py
  3.  Be patient because it takes a while.



How to change opponent RPS strategy:
  1.  Use your prefered text editor to open the file.
        <text editor command> final_game.py
  2.  Locate main() function at the end of the file.
  3.  Change the instantiation of 'player2'
        player2 = <insert RPS strategy function>
  4.  Re-run the program.
To change # of states set by HMM model, change the FIRST parameter of HMMAI(a,b) in player1.
To change # of moves viewed by HMM model, change the SECOND parameter of HMMAI(a,b) in player1.