import os 
import random  
def clear_console(): 
    os.system('cls' if os.name == 'nt' else 'clear')

class Node:
    def __init__(self, data):
        self.data = data
        self.link = None

suits = 'hcds'
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
deck = [rank + suit for suit in suits for rank in ranks]   

class Cards:
    def __init__(self, rank, suit, faceup=False):
        self.suit = suit
        self.rank = rank
        self.faceup = faceup
        
    def __repr__(self):
        return f"{self.rank}{self.suit}" if self.faceup else 'b'
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.link = new_node
            self.rear = new_node

    def dequeue_front(self):
        if self.is_empty():
            print("No more cards in the stockpile.")
            return None
        else:
            dequeued_node = self.front
            self.front = self.front.link
            if self.front is None:
                self.rear = None
            return dequeued_node.data

    def dequeue_rear(self):
        if self.is_empty():
            print("No more cards in the stockpile.")
            return None
        else:
            current = self.front
            prev = None
            while current.link:
                prev = current
                current = current.link
            if prev:
                prev.link = None
                self.rear = prev
            else:
                self.front = self.rear = None
            return current.data

    def is_empty(self):
        return self.front is None

    def display(self):
        elements = []
        current = self.front
        while current:
            elements.append(repr(current.data))
            current = current.link
        print(f"Stockpile: {elements}")

    def to_list(self):
        elements = []
        current = self.front
        while current:
            elements.append(current.data)
            current = current.link
        return elements

class Stack:
    def __init__(self):
        self.head = None
        
    def push(self, data):
        new_node = Node(data)
        new_node.link = self.head
        self.head = new_node
        
    def pop(self):
        if self.head is None:
            return None
        else:
            popped_node = self.head
            self.head = self.head.link
            popped_node.link = None
            return popped_node.data
        
    def display(self):
        elements = []
        n = self.head
        while n is not None:
            elements.append(n.data)
            n = n.link
        return elements

class Foundation:
    def __init__(self):
        self.stacks = {suit: Stack() for suit in suits}
        
    def valid_move(self, card):
        stack = self.stacks[card.suit]
        if not stack.head and card.rank == 'A':
            return True
        if stack.head:
            top_card = stack.head.data
            return ranks.index(card.rank) == ranks.index(top_card.rank) + 1
        return False
    
    def move_card(self, card):
        if self.valid_move(card):
            stockpile.remove_card(card) 
            self.stacks[card.suit].push(card)
            return True
        return False
    
    def display(self):
        for suit, stack in self.stacks.items():
            pile = stack.display()[::-1]
            pile_display = [repr(card) for card in pile]
            print(f"Foundation {suit}: {pile_display}")



class Stockpile:
    def __init__(self):
        self.cards = Queue()
        self.drawn_cards = []

    def setup(self, remaining_deck):
        for card_string in remaining_deck:
            rank = card_string[:-1]
            suit = card_string[-1]
            card = Cards(rank, suit)
            self.cards.enqueue(card)

    def draw_card(self):
        card = self.cards.dequeue_front()  
        if card:
            card.faceup = True
            self.drawn_cards.append(card)
        else:
            self.reset()
            card = self.cards.dequeue_front()
            if card:
                card.faceup = True
                self.drawn_cards.append(card)
        return card

    def reset(self):
        if self.drawn_cards:
            print("Resetting stockpile...")
            for card in (self.drawn_cards):  
                card.faceup = False
                self.cards.enqueue(card)
            self.drawn_cards = []

    def remove_card(self, card):
        if card in self.drawn_cards:
            self.drawn_cards.remove(card)

    def display(self):
        elements = []
        current = self.cards.front
        count = 0
        while current and count < 5:
            elements.append(repr(current.data))
            current = current.link
            count += 1
        print(f"Stockpile (showing top 5 cards): {elements}...")
class Tableau:
    def __init__(self):
        self.piles = [Stack() for _ in range(7)]

    def setup(self):
        random.shuffle(deck)
        index = 0
        for i in range(7):
            for j in range(i + 1):
                card_string = deck[index]
                rank = card_string[:-1]
                suit = card_string[-1]
                card = Cards(rank, suit, faceup=(j == i))
                self.piles[i].push(card)
                index += 1
        return deck[index:]

    def display(self):
        for i in range(7):
            pile = self.piles[i].display()[::-1]
            pile_display = [repr(card) for card in pile]
            print(f"Pile {i + 1}: {pile_display}")
 
 

         
    def valid_move(self, card1, card2):
        if card2 is None:  # Destination pile is empty
            return card1.rank == 'K'

        red_suits = 'hd'
        black_suits = 'cs'

        print(f"DEBUG: Checking move {card1} to {card2}")

        if (card1.suit in red_suits and card2.suit in black_suits) or (card1.suit in black_suits and card2.suit in red_suits):
            return ranks.index(card1.rank) == ranks.index(card2.rank) - 1  # Correct order for valid moves: card1 rank should be one less than card2 rank

        return False


         
    def move_sequence(self, from_pile, to_pile, num_cards):
        if not self.piles[from_pile].head or num_cards <= 0:
            return False

         
        sequence = []
        for _ in range(num_cards):
            card = self.piles[from_pile].pop()
            if card:
                sequence.append(card)
            else:
 
                while sequence:
                    self.piles[from_pile].push(sequence.pop())
                return False

        
        dest_card = self.piles[to_pile].head.data if self.piles[to_pile].head else None
        if not self.valid_move(sequence[-1], dest_card):
             
            while sequence:
                self.piles[from_pile].push(sequence.pop())
            return False

        
        while sequence:
            self.piles[to_pile].push(sequence.pop())

        
        if self.piles[from_pile].head:
            self.piles[from_pile].head.data.faceup = True

        return True
class GameState:
    def __init__(self, tableau, foundation, stockpile, drawn_cards):
        self.tableau = [[(card.rank, card.suit, card.faceup) for card in pile.display()] for pile in tableau.piles]
        self.foundation = {suit: [(card.rank, card.suit, card.faceup) for card in stack.display()] for suit, stack in foundation.stacks.items()}
        self.stockpile = [(card.rank, card.suit, card.faceup) for card in stockpile.cards.to_list()]
        self.drawn_cards = [(card.rank, card.suit, card.faceup) for card in drawn_cards]

game_states = []
def save_state():
    state = GameState(tableau, foundation, stockpile, stockpile.drawn_cards)
    game_states.append(state)

def undo_move():
    if game_states:
        state = game_states.pop()
        tableau.piles = [Stack() for _ in range(7)]
        for i, pile in enumerate(state.tableau):
            for rank, suit, faceup in reversed(pile):
                card = Cards(rank, suit, faceup)
                tableau.piles[i].push(card)

        foundation.stacks = {suit: Stack() for suit in suits}
        for suit, stack in state.foundation.items():
            for rank, suit, faceup in reversed(stack):
                card = Cards(rank, suit, faceup)
                foundation.stacks[suit].push(card)

        stockpile.cards = Queue()
        for rank, suit, faceup in state.stockpile:
            card = Cards(rank, suit, faceup)
            stockpile.cards.enqueue(card)

        stockpile.drawn_cards = [Cards(rank, suit, faceup) for rank, suit, faceup in state.drawn_cards]
    else:
        print("No moves to undo!")

# Main code
tableau = Tableau()
foundation = Foundation()
stockpile = Stockpile()

remaining_deck = tableau.setup()
stockpile.setup(remaining_deck)

def display_all():
    clear_console()
    tableau.display()
    foundation.display()
    stockpile.display()

display_all()
def check_win_condition():
    for suit in suits:
        if len(foundation.stacks[suit].display()) != 13:  # 
            return False
    return True

while True:
    
    user_input = input("Enter the pile number to move from (1-7) or enter '0' to draw from stockpile: ")
    if user_input.lower() == 'u': 
        undo_move() 
        display_all() 
        continue
    if user_input == '0':
        from_pile = -1
    else:
        try:
            from_pile = int(user_input) - 1
        except ValueError:
            display_all()
            continue
    save_state()
    while from_pile == -1:
        drawn_card = stockpile.draw_card()
        display_all()
        if drawn_card:
            print(f"Drawn card: {drawn_card}")
            user_input = input("Enter the pile number to move from (1-7) or enter '0' to draw another card from stockpile or enter '8' for drawn card: ")
            if user_input == '8':
                from_pile = 8
            else:
                try:
                    from_pile = int(user_input) - 1
                except ValueError:
                    from_pile = -1
        else:
            from_pile = 0

    if from_pile == 8:
        valid_move_found = False
        while not valid_move_found:
            to_pile = input("Enter the destination (1-7 for tableau, f for foundation): ")

            if to_pile == 'f':
                if foundation.move_card(drawn_card):
                    stockpile.remove_card(drawn_card)
                    print(f"Moved {drawn_card} to foundation")
                    drawn_card = None
                    valid_move_found = True
                else:
                    print("Invalid move to foundation! Try again.")
            else:
                try:
                    to_pile = int(to_pile) - 1
                    if tableau.valid_move(drawn_card, tableau.piles[to_pile].head.data if tableau.piles[to_pile].head else None):
                        stockpile.remove_card(drawn_card)
                        tableau.piles[to_pile].push(drawn_card)
                        print(f"Moved {drawn_card} to Pile {to_pile + 1}")
                        drawn_card = None
                        valid_move_found = True
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Invalid destination input!")

            if not valid_move_found:
                choice = input("No valid move found. Do you want to try moving the drawn card again (y/n)? ")
                if choice.lower() == 'n':
                    drawn_card = None
                    valid_move_found = True

        display_all()
        continue

    if not tableau.piles[from_pile].head:
        print("Invalid move! The source pile is empty.")
        display_all()
        continue

    move_sequence = input("Do you want to move a sequence of cards (y/n)? ").lower() == 'y'
    if move_sequence:
        num_cards = int(input("Enter the number of cards to move: "))
        to_pile = int(input("Enter the destination (1-7 for tableau): ")) - 1
        if tableau.move_sequence(from_pile, to_pile, num_cards):
            print(f"DEBUG: Moved {num_cards} cards from Pile {from_pile + 1} to Pile {to_pile + 1}")
        else:
            print("DEBUG: Invalid move!")
        display_all()
        continue
    else:
        to_pile = input("Enter the destination (1-7 for tableau, f for foundation): ")

        if to_pile == 'f':
            from_card = tableau.piles[from_pile].pop()
            if foundation.move_card(from_card):
                if tableau.piles[from_pile].head:
                    tableau.piles[from_pile].head.data.faceup = True
            else:
                tableau.piles[from_pile].push(from_card)
                print("Invalid move to foundation! Try again.")
        else:
            try:
                to_pile = int(to_pile) - 1
                if not tableau.move_sequence(from_pile, to_pile, 1):
                    print("Invalid move to tableau! Try again.")
            except ValueError:
                print("Invalid destination input!")
        if check_win_condition(): 
            display_all() 
            print("Congratulations! You've won the game!") 
            break
        display_all()
