import pygame
import random

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visual Blackjack")
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 40, bold=True)
clock = pygame.time.Clock()

# --- Game Data ---
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}
suits = ["♠", "♥", "♦", "♣"]

# --- Functions ---
def create_deck():
    return [f"{rank}{suit}" for rank in card_values for suit in suits]

def calculate_total(hand):
    total = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
        value = card_values.get(rank, 0)
        total += value
        if rank == "A":
            aces += 1
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def draw_text(text, x, y, size=28, color=(255,255,255)):
    font_obj = pygame.font.SysFont("arial", size)
    label = font_obj.render(text, True, color)
    screen.blit(label, (x, y))

def draw_card(card, x, y, hidden=False):
    pygame.draw.rect(screen, (255, 255, 255) if not hidden else (50, 50, 50), (x, y, 60, 90), border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 60, 90), 2, border_radius=8)
    if not hidden:
        draw_text(card, x + 8, y + 30, 24, (0, 0, 0))

def draw_hand(hand, x, y, hide_first=False):
    for i, card in enumerate(hand):
        draw_card(card, x + i * 70, y, hidden=(hide_first and i == 0))

# --- Game Start ---
deck = create_deck()
random.shuffle(deck)
player = [deck.pop(), deck.pop()]
dealer = [deck.pop(), deck.pop()]
dealer_hidden = True
player_stand = False
game_over = False

# --- Game Loop ---
running = True
while running:
    screen.fill((30, 30, 60))  # dark blue-purple background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_h and not player_stand:
                player.append(deck.pop())
                if calculate_total(player) > 21:
                    dealer_hidden = False
                    game_over = True

            elif event.key == pygame.K_s and not player_stand:
                player_stand = True
                dealer_hidden = False
                while calculate_total(dealer) < 16:
                    dealer.append(deck.pop())
                game_over = True

    # Draw dealer hand
    draw_text("Dealer's Hand:", 50, 30)
    draw_hand(dealer, 50, 70, hide_first=dealer_hidden)
    if not dealer_hidden:
        draw_text("Total: " + str(calculate_total(dealer)), 50, 170)

    # Draw player hand
    draw_text("Player's Hand:", 50, 250)
    draw_hand(player, 50, 290)
    draw_text("Total: " + str(calculate_total(player)), 50, 390)

    # Instructions
    if not game_over:
        draw_text("[H]it or [S]tay", 550, 30, size=24, color=(200, 200, 50))

    # Game Result
    if game_over:
        pt, dt = calculate_total(player), calculate_total(dealer)
        if pt > 21:
            result = "You BUST! Dealer wins."
        elif dt > 21:
            result = "Dealer BUSTS! You win!"
        elif pt > dt:
            result = "You win!"
        elif dt > pt:
            result = "Dealer wins."
        else:
            result = "It's a tie."
        draw_text(result, 50, 450, size=32, color=(255, 215, 0))
        draw_text("Press ESC to quit", 50, 490, size=24)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
