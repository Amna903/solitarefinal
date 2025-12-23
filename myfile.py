import random
import pygame
from pygame.locals import *
import time
import sys
pygame.init()

timer_start = 10 * 60 
timer = timer_start 
font = pygame.font.Font(None, 26)
screen_wid, screen_hei = 1150, 900
card_wid, card_height = 130, 180
bg_clr = (0, 128, 0)
white = (255, 255, 255)
green = (0, 128, 0)
found_to_tab_gap = 100  
bg_img = pygame.image.load('bgimg.jpeg')
bg_img = pygame.transform.scale(bg_img, (screen_wid, screen_hei))  # Scale to fit screen size
 
class Button:
    def __init__(self, x, y, width, height, text, font, image, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.image = pygame.transform.scale(image, (width, height))   
        self.action = action

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
        image_rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.image, image_rect)
        if self.text:
            text_surf = self.font.render(self.text, True, (0, 128, 0))
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surf, text_rect)

    def click(self): 
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height: 
            if self.action: 
                self.action() 
            return True 
        return False

#card images
cardimg = {}
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = 'hcds'
for suit in suits:
    for rank in ranks:
        card_image = pygame.image.load(f'card1/{rank.lower()}{suit}.jpg')
        card_image = pygame.transform.scale(card_image, (card_wid, card_height))
        cardimg[f'{rank}{suit}'] = card_image
cardimg['Back'] = pygame.transform.scale(pygame.image.load('card1/back.jpg'), (card_wid, card_height))

#Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = False 
        self.highlighted = False   

    def __str__(self):
        return f'{self.rank}{self.suit}' if self.face_up else 'Back'

    def draw(self, screen, x, y):
        card_image = cardimg[str(self)]
        screen.blit(card_image, (x, y))
        if self.highlighted:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, card_wid, card_height), 1)  # Draw red outline if highlighted

#   class
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

# node class for linked list stack and queue
class Node:
    def __init__(self, data):
        self.data = data
        self.link = None
  
#Queue 
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0   

    def is_empty(self):
        return self.size == 0   

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.link = new_node
            self.rear = new_node
        self.size += 1   

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.link
        self.size -= 1   
        return temp.data

    def peek_front(self):
        if self.is_empty():
            return None
        return self.front.data

    def peek_rear(self):
        if self.is_empty():
            return None
        return self.rear.data

    def __len__(self):
        return self.size   

#Stack 
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
        temp = self.head
        self.head = self.head.link
        return temp.data

    def peek(self):
        if self.head is None:
            return None
        return self.head.data

    def is_empty(self):
        return self.head is None

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.link
        print("None")
        
def get_face_up_cards_from(stack, start_card):
    cards = []
    temp = stack.head
    found = False
    while temp:
        if temp.data == start_card:
            found = True
        if found and temp.data.face_up:
            cards.append(temp.data)
        temp = temp.link
    return cards

def remove_cards_from_stack(stack, num_cards):
    cards_to_remove = []
    for _ in range(num_cards):
        if stack.head:
            cards_to_remove.append(stack.pop())
    return cards_to_remove[::-1] 
        
#Tableau 
class Tableau:
    def __init__(self, deck):
        self.piles = [Stack() for _ in range(7)]
        for i in range(7):
            for j in range(i + 1):
                card = deck.draw()
                self.piles[i].push(card)
            
            last_card = self.piles[i].peek()
            if last_card:
                last_card.face_up = True
    
    def move(self, from_pile, to_pile, cards):
        if self.can_move(cards, to_pile):  
            for card in cards: 
                self.piles[to_pile].push(card)
        else:
            for card in reversed(cards):
                self.piles[from_pile].push(card)

    def can_move(self, cards, to_pile):
        if not cards:
            return False
        if self.piles[to_pile].is_empty():
            return cards[0].rank == 'K'   
        top_card = self.piles[to_pile].peek()
        return self.is_descending(cards[0], top_card) and self.is_alternating_color(cards[0], top_card)
 
    def is_descending(self, card, top_card):
        rank_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        return rank_order[card.rank] == rank_order[top_card.rank] - 1
    

    def is_alternating_color(self, card, top_card):
        red_suits = {'h', 'd'}
        black_suits = {'c', 's'}
        return (card.suit in red_suits and top_card.suit in black_suits) or (card.suit in black_suits and top_card.suit in red_suits)
  
    
    def display(self, screen):
        display_piles(screen, self.piles, 100, 150 + found_to_tab_gap)

def display_piles(screen, piles, start_x, start_y, show_border=False, foundation=False):
    for i, pile in enumerate(piles):
        x = start_x + i * (card_wid + 10)
        y = start_y
        temp = pile.head
        cards = []
        if show_border:
            pygame.draw.rect(screen, white, (x, y, card_wid, card_height), 1)
        while temp:
            cards.append(temp.data)
            temp = temp.link
        for card in reversed(cards):
            card.draw(screen, x, y)
            if not foundation:
                y += 20   

# Foundation
class Foundation:
    def __init__(self):
        self.piles = [Stack() for _ in range(4)]

    def add(self, card, to_pile):
        self.piles[to_pile].push(card)

    def display(self, screen):
        
        start_x_positions = [100 + (i + 3) * (card_wid + 10) for i in range(4)]
        for i, x in enumerate(start_x_positions):
            display_piles(screen, [self.piles[i]], x, 50, show_border=True, foundation=True)
 
    def can_add(self,card,to_pile):
        if self.piles[to_pile].is_empty():
            return card.rank == 'A'
        top_card = self.piles[to_pile].peek()
        return (card.suit == top_card.suit) and (self.rank_to_int(card.rank) == self.rank_to_int(top_card.rank) + 1)
    def rank_to_int(self,rank): 
        rank_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13} 
        return rank_order[rank]
    
class Stockpile:
    def __init__(self):
        self.queue = Queue()
        self.drawn_cards = []

    def add_to_stockpile(self, card):
        card.face_up = False   
        self.queue.enqueue(card)

    def draw_card(self):
        if self.queue.is_empty():
            
            return None
        card = self.queue.dequeue()
        card.face_up = True  
        self.drawn_cards.append(card)
        
        return card

    def reset_drawn_cards(self):
         
        for card in (self.drawn_cards):
            card.face_up = False   
            self.queue.enqueue(card)
        self.drawn_cards.clear()  
        
    def is_empty(self): 
        return self.queue.is_empty()  

    def display(self, screen):
        stockpile_x, stockpile_y = 100, 50   
        if not self.queue.is_empty():
            card_back = cardimg['Back']
            screen.blit(card_back, (stockpile_x, stockpile_y))
        else:
            pygame.draw.rect(screen, white, (stockpile_x, stockpile_y, card_wid, card_height), 1)
        draw_x = stockpile_x + card_wid + 10 
        draw_y = stockpile_y
        for drawn_card in self.drawn_cards:
            drawn_card.draw(screen, draw_x, draw_y)

class SolitaireGame:
    def __init__(self):
        self.deck = Deck()
        self.tableau = Tableau(self.deck)
        self.foundation = Foundation()
        self.stockpile = Stockpile()
        self.undo_stack = Stack()

        while self.deck.cards:
            self.stockpile.add_to_stockpile(self.deck.draw())

    def save_state(self):
        state = {
            'tableau': [[(card.rank + card.suit, card.face_up) for card in self.get_stack_cards(pile)] for pile in self.tableau.piles],
            'foundation': [[(card.rank + card.suit, card.face_up) for card in self.get_stack_cards(pile)] for pile in self.foundation.piles],
            'stockpile': [(card.rank + card.suit) for card in self.get_stack_cards(self.stockpile.queue)],
            'drawn_cards': [(card.rank + card.suit, card.face_up) for card in self.stockpile.drawn_cards]
        }
        self.undo_stack.push(state)

    def get_stack_cards(self, stack_or_queue):
        cards = []
        if isinstance(stack_or_queue, Stack) or isinstance(stack_or_queue, Queue):
            temp = stack_or_queue.front if isinstance(stack_or_queue, Queue) else stack_or_queue.head
            while temp:
                cards.append(temp.data)
                temp = temp.link
        return cards

    def load_state(self, state):
        self.tableau.piles = [Stack() for _ in range(7)]
        for i, pile in enumerate(state['tableau']):
            for card_str, face_up in reversed(pile):
                rank, suit = card_str[:-1], card_str[-1]
                card = Card(rank, suit)
                card.face_up = face_up
                self.tableau.piles[i].push(card)

        self.foundation.piles = [Stack() for _ in range(4)]
        for i, pile in enumerate(state['foundation']):
            for card_str, face_up in reversed(pile):
                rank, suit = card_str[:-1], card_str[-1]
                card = Card(rank, suit)
                card.face_up = face_up
                self.foundation.piles[i].push(card)

        self.stockpile.queue = Queue()
        for card_str in (state['stockpile']):
            rank, suit = card_str[:-1], card_str[-1]
            self.stockpile.add_to_stockpile(Card(rank, suit))

        self.stockpile.drawn_cards = []
        for card_str, face_up in state['drawn_cards']:
            rank, suit = card_str[:-1], card_str[-1]
            card = Card(rank, suit)
            card.face_up = face_up
            self.stockpile.drawn_cards.append(card)

    def find_possible_moves(self):
        hints = []
        for i, pile in enumerate(self.tableau.piles):
            if not pile.is_empty():
                card = pile.peek()
                for j in range(4):
                    if self.foundation.can_add(card, j):
                        hints.append((card, f'Tableau {i+1}', f'Foundation {j+1}'))

        for i, pile in enumerate(self.tableau.piles):
            if not pile.is_empty():
                cards = get_face_up_cards_from(pile, pile.peek())
                for card in cards:
                    for j, target_pile in enumerate(self.tableau.piles):
                        if i != j and self.tableau.can_move([card], j):
                            hints.append((card, f'Tableau {i+1}', f'Tableau {j+1}'))

       
        if self.stockpile.drawn_cards:
            card = self.stockpile.drawn_cards[-1]
            for i, pile in enumerate(self.tableau.piles):
                if self.tableau.can_move([card], i):
                    hints.append((card, 'Stockpile', f'Tableau {i+1}'))

        
        if self.stockpile.drawn_cards:
            card = self.stockpile.drawn_cards[-1]
            for i in range(4):
                if self.foundation.can_add(card, i):
                    hints.append((card, 'Stockpile', f'Foundation {i+1}'))

        return hints

    def highlight_move(self, move):
        card, source, destination = move
        card.highlighted = True
        print(f'Move {card} from {source} to {destination}')
        highlight_destinations(self, move)

def highlight_destinations(game, move):
    card, source, destination = move
    card.highlighted = True

    if "Tableau" in destination:
        pile_index = int(destination.split()[-1]) - 1
        top_card = game.tableau.piles[pile_index].peek()
        if top_card is not None:
            top_card.highlighted = True
    elif "Foundation" in destination:
        pile_index = int(destination.split()[-1]) - 1
        if not game.foundation.piles[pile_index].is_empty():
            top_card = game.foundation.piles[pile_index].peek()
            if top_card is not None:
                top_card.highlighted = True
        else:
            print("Foundation Slot")

def reset_highlights(game):
    for pile in game.tableau.piles:
        temp = pile.head
        while temp:
            temp.data.highlighted = False
            temp = temp.link

    for pile in game.foundation.piles:
        temp = pile.head
        while temp:
            temp.data.highlighted = False
            temp = temp.link

    for card in game.stockpile.drawn_cards:
        card.highlighted = False

def check_win_condition(game):  
    for pile in game.foundation.piles: 
        if len(game.get_stack_cards(pile)) != 13: 
            return False 
    if not game.stockpile.is_empty() or any(len(game.get_stack_cards(pile)) > 0 for pile in game.tableau.piles): 
            return False 
    return True

 
def main():
    screen = pygame.display.set_mode((screen_wid, screen_hei))
    pygame.display.set_caption('Solitaire')
   
    game = SolitaireGame()
    CLEAR_HIGHLIGHTS = pygame.USEREVENT + 1
    pygame.time.set_timer(CLEAR_HIGHLIGHTS, 0)   


    button_image = pygame.image.load('/Users/amanmalik/Downloads/e01f1b1f-45b3-4409-bf2f-525e34ecfe69-removebg-preview.png')
    btn_img = pygame.image.load('/Users/amanmalik/Downloads/bn-removebg-preview.png')
    undo = pygame.image.load('/Users/amanmalik/Downloads/Undo-removebg-preview.png')
    # Create buttons
    button_font = pygame.font.Font(None, 20)
    new_game_button = Button(130, 795, 50, 75, '', button_font, button_image)
    undo_button = Button(180, 762, 150, 130, '', button_font, undo)
    hint_button = Button(330, 790, 70, 70, '', button_font, btn_img)


    dragging = False
    drag_cards = []
    drag_pile = None
    drag_offset_x = 0
    drag_offset_y = 0
    dragged_from_drawn_pile = False
    dragged_card = None
    timer = timer_start 
    start_ticks = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if new_game_button.click():
                    pygame.quit()
                    sys.exit()
                if undo_button.click() and not game.undo_stack.is_empty(): 
                    previous_state = game.undo_stack.pop() 
                    game.load_state(previous_state)     
                if hint_button.click():
                    reset_highlights(game)  
                    possible_moves = game.find_possible_moves() 
                    if possible_moves: 
                        move = possible_moves[0] 
                        game.highlight_move(move)  
                        pygame.time.set_timer(CLEAR_HIGHLIGHTS, 4000)  
                    else: 
                        print("No possible moves")
                game.save_state()
                x, y = event.pos

                stockpile_rect = pygame.Rect(100, 50, card_wid, card_height)
                if stockpile_rect.collidepoint(x, y):
                    if game.stockpile.is_empty():
                        game.stockpile.reset_drawn_cards()
                    else:
                        game.stockpile.draw_card()

                draw_pile_rect = pygame.Rect(100 + card_wid + 10, 50, card_wid, card_height)
                if draw_pile_rect.collidepoint(x, y):
                    if game.stockpile.drawn_cards:
                        card = game.stockpile.drawn_cards[-1]
                        drag_cards = [card]
                        dragging = True
                        dragged_from_drawn_pile = True
                        dragged_card = card
                        game.stockpile.drawn_cards.remove(card) 
                        drag_offset_x = x - (100 + card_wid + 10)
                        drag_offset_y = y - 50

                for i, pile in enumerate(game.tableau.piles):
                    temp = pile.head
                    position = 0
                    while temp:
                        card = temp.data
                        card_rect = pygame.Rect(100 + i * (card_wid + 10), 150 + found_to_tab_gap + position * 20, card_wid, card_height)
                        if temp.data.face_up and card_rect.collidepoint(x, y):
                            drag_cards = get_face_up_cards_from(pile, temp.data)
                            dragging = True
                            drag_pile = i
                            drag_offset_x = x - card_rect.x
                            drag_offset_y = y - card_rect.y
                            drag_cards = remove_cards_from_stack(pile, len(drag_cards))
                            break
                        temp = temp.link
                        position += 1
                    if dragging:
                        break

                for i in range(4):
                    pile_rect = pygame.Rect(100 + (i + 3) * (card_wid + 10), 50, card_wid, card_height)
                    if pile_rect.collidepoint(x, y) and not game.foundation.piles[i].is_empty():
                        card = game.foundation.piles[i].peek()
                        drag_cards = [card]
                        dragging = True
                        drag_pile = i
                        drag_offset_x = x - pile_rect.x
                        drag_offset_y = y - pile_rect.y
                        game.foundation.piles[i].pop()
                        dragged_from_drawn_pile = False
                        break
                    
            elif event.type == KEYDOWN:
                if event.key == K_u and not game.undo_stack.is_empty(): 
                    previous_state = game.undo_stack.pop() 
                    game.load_state(previous_state) 
                elif event.key == K_h: 
                    reset_highlights(game)  
                    possible_moves = game.find_possible_moves() 
                    if possible_moves: 
                        move = possible_moves[0] 
                        game.highlight_move(move)  
                        pygame.time.set_timer(CLEAR_HIGHLIGHTS, 4000) 
                    else: 
                        print("No possible moves")
            elif event.type == CLEAR_HIGHLIGHTS:
                reset_highlights(game)
                pygame.time.set_timer(CLEAR_HIGHLIGHTS, 0)

            elif event.type == MOUSEBUTTONUP:
                if dragging:
                    x, y = event.pos
                    found_pile = False
                    # for dropping in tableau
                    for i, pile in enumerate(game.tableau.piles):
                        pile_rect = pygame.Rect(100 + i * (card_wid + 10), 150 + found_to_tab_gap, card_wid, screen_hei - (150 + found_to_tab_gap))
                        if pile_rect.collidepoint(x, y):
                            if game.tableau.can_move(drag_cards, i):  # Validate the entire stack of cards
                                game.tableau.move(drag_pile, i, drag_cards)
                                found_pile = True
                            break
                    # for dropping in foundation
                    if not found_pile:
                        for i in range(4):
                            pile_rect = pygame.Rect(100 + (i + 3) * (card_wid + 10), 50, card_wid, card_height)
                            if pile_rect.collidepoint(x, y):
                                if len(drag_cards) == 1 and game.foundation.can_add(drag_cards[0], i):
                                    game.foundation.add(drag_cards[0], i)
                                    found_pile = True
                                    break
                    if not found_pile:
                        if drag_pile is not None:
                            if dragged_from_drawn_pile:
                                game.stockpile.drawn_cards.append(dragged_card)
                            else:
                                for card in drag_cards:
                                    game.tableau.piles[drag_pile].push(card)
                    else:
                        if not dragged_from_drawn_pile and drag_pile is not None and game.tableau.piles[drag_pile].head and not game.tableau.piles[drag_pile].head.data.face_up:
                            game.tableau.piles[drag_pile].head.data.face_up = True

                    if dragged_from_drawn_pile and not found_pile:
                        game.stockpile.drawn_cards.append(dragged_card)

                dragging = False
                drag_cards = []
                drag_pile = None
                dragged_from_drawn_pile = False
                dragged_card = None
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000 
        timer = max(timer_start - seconds, 0) 
        mins, secs = divmod(timer, 60) 
        timer_text = f'Time Left: {int(mins):02}:{int(secs):02}'
        screen.fill(bg_clr)
        screen.blit(bg_img, (0, 0))
        new_game_button.draw(screen) 
        undo_button.draw(screen) 
        hint_button.draw(screen)
        timer_surf = font.render(timer_text, True, (255, 255, 255)) 
        timer_rect = timer_surf.get_rect(center=(screen_wid -155, screen_hei - 75)) 
        screen.blit(timer_surf, timer_rect)
        game.tableau.display(screen)
        game.foundation.display(screen)
        game.stockpile.display(screen)
        if dragging and drag_cards:
            x, y = pygame.mouse.get_pos()
            for index, card in enumerate(drag_cards):
                card.draw(screen, x - drag_offset_x, y - drag_offset_y + index * 20)
        running = True
  

        #  Game Over 
        if timer <= 0: 
            game_over_font = pygame.font.Font(None, 72) 
            game_over_surf = game_over_font.render("Game Over", True, (255, 0, 0)) 
            game_over_rect = game_over_surf.get_rect(center=(screen_wid // 2, screen_hei // 2)) 
            screen.blit(game_over_surf, game_over_rect) 
            pygame.display.update() 
            time.sleep(2) 
            running = False  
        if check_win_condition(game): 
            win_font = pygame.font.Font(None, 72) 
            win_surf = win_font.render("You Win!", True, (0, 255, 0)) 
            win_rect = win_surf.get_rect(center=(screen_wid // 2, screen_hei // 2)) 
            screen.blit(win_surf, win_rect) 
            pygame.display.update() 
            time.sleep(2) 
            running = False
    
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
