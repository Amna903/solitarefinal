
Instructed By
Mr. Nazeef Ul Haq

Developed by Amna Atiq(2023-CS-83) for a midterm project in CSC200 - Data Structures & Algorithms.

Solitaire Game

Project Description
    This is implementation of a classic card game: Solitaire. The game is built in Python, and it uses Pygame libraries for an interactive graphical experience. The game features user interactions, and fluid transitions across game states.

Features
Classic Solitaire gameplay
- Smooth animations and transitions
    - User-friendly interface
    - Undo functionality
    - Hint system
    - Victory detection
    - Foundation, Tableau, and Stockpile implementation
    - Timer to track duration

    Libraries
     - Python 3.12
     - Pygame

Running the Game
1. Install Python 3.12
2. Install Dependencies:
        pip install pygame
3. Run the Game:
       python myfile.py
       
myfile.py. The primary Solitaire game logic, user interface.
      
Game Controls
    - Mouse Click: Select and move cards
    - Undo: Bring the prev state
    - Quit: Exits the game
    - Hint: Give hint
    
Key Functions
1. get_face_up_cards_from: Retrieves face-up cards from tableau pile starting from given card.
2. remove_cards_from_stack: Removes and returns specified number of cards from stack.
3. display_piles: Displays cards in specified pile.
4. save_state: Saves the game state for undo function to work.
5. load_state: Loads previously saved game state for undo.


Testing Cases
Test Case 1: Card Movement
    Steps:
    1.Run the game
    2.Try to move a card from one tableau pile to another.
    3.Check the movement validity and state update of the game .
    Expected Result: The card moves with regard to the Solitaire game rules and the game state update .

Test Case 2: Undo Move
    Steps:
    1. Run the game.
    2. Make some legal moves.
    3. Undo.
    4. Verify that the state of the game reverts to the pre-moves state.
    What is Expected: The state of the game correctly goes back to the previous state.

Test Case 3: Winning Condition
    Steps:
    1.Run the game.
    2.Move all cards manually to their corresponding foundation piles
    3.The game detects the win condition and shows a congratulatory message.
    Expected Result: The game detects the win condition and displays the win message.

Test Case 4: Setup Verification
    Expected Result: Tableau should have 7 piles, with each pile containing the right number of cards (1 in pile 1, 2 in pile 2 ... 7 in pile 7).
    Stockpile should have the remaining cards (24).
    Foundation piles should be empty.

Test Case 5: Reset Stockpile 
    Steps: 
    1.Draw cards continuously from stockpile until it's empty, then draw again to reset.
    Expected Result: Stockpile should reset, moving all drawn_cards back into the stockpile face-down.

Test Case 6: Moving a Card to Foundation (Invalid Move)
    Steps: 
    1.Attempt to place card that does not follow sequential order in foundation (i.e a 4 on an Ace).
    Expected Outcome: The move should be denied bringing card back to its orginal position.

    # solitarefinal
