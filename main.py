#----------------------------------------------------------------
# Name:        Escape Room
# Purpose:     To integrate and utilize all aspects of course content into a single project
#
# Author:      Kevin D
# Created:     June 10 2021
# Updated:     June 16 2021
#----------------------------------------------------------------

# References:
# - Sound effects (copyright free):
# - https://freesound.org/people/LittleRobotSoundFactory/sounds/270404/
# - https://freesound.org/people/StavSounds/sounds/546082/
# - https://freesound.org/people/rhodesmas/sounds/342756/
# - https://freesound.org/people/humanoide9000/sounds/466133/
# - https://www.w3schools.com/python/python_lists.asp (.extend method)
# - https://www.pygame.org/docs/ (Pygame documentation)

import pygame
import random

pygame.init()

# Setup
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (150, 252, 255)
PHONESCREEN = (73, 73, 73)
SIZE = (800, 600)
screen = pygame.display.set_mode(SIZE)
background = pygame.image.load("Things/Escape room 2.jpg")
background = pygame.transform.scale(background, (800, 600))
running = True
myClock = pygame.time.Clock()
framecount = 0

# Popup preparation
intro = False  # Boolean that will control the popup of an intro message at the very beginning
found_item = pygame.mixer.Sound("Things/Discovery.wav")  # Sound effect for when an item is found
found_item.set_volume(0.7)
dialogue_lines = open("Things/Messages.txt", "r")
messages = []
for line in dialogue_lines:  # Uses a for loop to add all of the lines in the file Messages.txt into the list "messages"
    line = line.rstrip()
    messages.append(line)
dialogue_lines.close()
message_rect = pygame.Rect(200, 200, 400, 0)  # A rect for popup messages. The height is 0 because it is updated for each popup so it doesn't really matter what the inital value is

# Interaction 1
# Cookies
cookies = pygame.image.load("Things/Cookies.png")
cookies = pygame.transform.scale(cookies, (120, 50))  # Loads and resizes image
cookie_thumbnail = pygame.transform.scale(cookies, (60, 25))  # Prepares a thumbnail version to be used in the inventory
cookie_rect = pygame.Rect(415, 415, 120, 50)  # Sets up a rect around the picture to be used for collisions
# Bird cage
bird_cage = pygame.image.load("Things/Bird cage.png")
bird_cage = pygame.transform.scale(bird_cage, (100, 200))
# Bird, AKA Parry
bird = pygame.image.load("Things/Bird.png")
bird = pygame.transform.scale(bird, (50, 50))
bird_rect = pygame.Rect(70, 110, 50, 50)
# Prepares Parry's dialogue
hint_lines = open("Things/Parry.txt", "r")
hints = []
for line in hint_lines:  # Adds all of the possible clues that Parry may offer into the list "hints"
    line = line.rstrip()
    hints.append(line)
hint_lines.close()
hint_rect = pygame.Rect(145, 75, 150, 0)  # Text box for Parry's hints
start = 0  # Variable for timed events
random_clue = 0  # Variable for picking a random clue
progress = 0  # Keeps track of player progress
# Progress 1 = Found the cookies
# Progress 2 = Gave cookies to Parry
# Progress 3 = Found the phone
# Progress 4 = Found the note with password
# Progress 5 = Found the watering can
# The progress is also the index of the popup message for each event in the list "messages"

# States
popup = False
talking = False  # Boolean to control timed dialogue

# Interaction 2
# Pillow
pillow_rect = pygame.Rect(290, 260, 80, 100)
# Phone
phone = pygame.image.load("Things/Phone.png")  # Loads three images of different states of the phone: blank screen,
# to be used in the inventory. Unlock screen, to be used for clue2, and a notes app screen to be used for clue3. The
# text on the phone screen could have been created using code but since their only function is appearance I thought it
# might be easier to just edit on the text permanently using GIMP.
phone_unlock = pygame.image.load("Things/Phone unlock.png")
phone_notes = pygame.image.load("Things/Phone note.png")
phone_thumbnail = pygame.transform.scale(phone, (30, 60))
phone_rect = phone.get_rect(center=(screen.get_width()/2, screen.get_height()/2))  # Sets up a centered rect for the phone
text = ""  # Empty string to be used for user input
phone_password = "1246"
incorrect = pygame.mixer.Sound("Things/Wrong password.wav")  # Prepares sound effect for wrong password entries
incorrect.set_volume(1.5)
correct = pygame.mixer.Sound("Things/Correct password.wav")  # Prepares sound effect for correct password entries
# Sticky note
sticky_note = pygame.image.load("Things/Note.png")
big_sticky = pygame.transform.scale(sticky_note, (200, 200))  # Makes a larger version so the player can actually read the message once they find it
sticky_note = pygame.transform.scale(sticky_note, (30, 30))  # This small version is the one that the player can click on
note_rect = sticky_note.get_rect(topleft=(400, 160))
# States
phoneout = False
unlock_warning = False
unlocked = False
noteout = False

# Interaction 3
# Watering can
watering_can = pygame.image.load("Things/Watering can.png")
watering_can = pygame.transform.scale(watering_can, (90, 90))
water_thumbnail = pygame.transform.scale(watering_can, (50, 50))
water_rect = pygame.Rect(660, 140, 90, 90)
plant_rect = pygame.Rect(525, 160, 65, 105)
# States
drag = False
won = False

items = [cookie_thumbnail, phone_thumbnail, sticky_note, water_thumbnail]  # A list of item thumbnails
has_items = [False, False, False, False]  # A connected list keeping track of whether an item has been obtained by the player

# Bells and whistles
achievement_messages = ["Parry Skywalker", "Ahhhh...", "Lookin' snazzy"]  # List of achievement names, with matching pictures in a connected list
coffee_image = pygame.image.load("Things/Coffee.png")  # 50x50
hat_image = pygame.image.load("Things/Hat.png")  # 50x25
light_saber = pygame.image.load("Things/Lightsaber.png")  # 50x50
achievement_images = [light_saber, coffee_image, hat_image]
coffee_rect = pygame.Rect(140, 320, 60, 65)
hat_rect = pygame.Rect(760, 90, 40, 60)
congrats_rect = pygame.Rect(0, 0, 0, 57)  # Box for displaying message at the top left of the screen. The width is updated
# For every message so it's initially set to 0.
# States
congrats = False # Boolean to control timed popup
easter_start = 0  # Similar to the "start" variable, but for the easter egg timed popups
easter_egg = 0  # Variable to keep track of which easter egg was obtained
secrets_found = [False, False, False]  # List to keep track of which easter eggs have been found

# Victory screen
victory_music = pygame.mixer.Sound("Things/Victory.wav")
victory_music.set_volume(0.7)
birdX = 0
bird_dir = 1


# Displays mouse coordinates on top left corner of screen
def display_coordinates(screen):
    fontCoords = pygame.font.SysFont("arial", 14)
    # print(pygame.mouse.get_pos())
    textCoords = fontCoords.render(str(pygame.mouse.get_pos()), True, RED)
    textRect = textCoords.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(textCoords, textRect)


def load_sprites(spritesheet, DIMw, DIMh, offset):  # Borrowed from escape room example
    sprites = []
    W = spritesheet.get_width()//DIMw  # Frame width
    H = spritesheet.get_height()//DIMh  # Frame height
    for i in range(DIMw*DIMh-offset):  # Offset is if there are extra blank frames
        x = i%DIMw*W    # x coordinate of frame
        y = i//DIMw*H   # y coordinate of frame
        sprites.append(pygame.transform.scale(spritesheet.subsurface(pygame.Rect(x, y, W, H)), (100, 100))) # Cuts out the frame onto a subsurface then added to list.
        # In this case I also resized each frame to be 100x100 pixels.
    return sprites  # Sends the list back to the main program

# For victory screen
bird_sprite = load_sprites(pygame.image.load("Things/Bird sprite sheet.png"), 5, 5, 3)


# Draws gridlines on screen
def draw_gridlines(screen):
    for i in range(100, screen.get_width(), 100):
        pygame.draw.line(screen, BLACK, (i, 0), (i, screen.get_height()))
    for i in range(100, screen.get_height(), 100):
        pygame.draw.line(screen, BLACK, (0, i), (screen.get_width(), i))


def display_message(screen, message, text_rect, tcolour, tbcolour, size, has_border):  # Inspired by escape room example

    # Sets up the things needed for displaying text
    font = pygame.font.SysFont("Times new roman", size)
    linelength = 0  # Keeps track of how long the current line is
    linecount = 1  # Keeps track of how many lines there are
    padding = 15  # Determines the distance between the text and edge of the box
    words = message.split()  # Splits given message into individual words

    # Draws background
    pygame.draw.rect(screen, tbcolour, text_rect)  # A box in the background colour
    if has_border:
        pygame.draw.rect(screen, tcolour, text_rect, 2)  # An outline in the text colour, if has_border is true

    for word in words:
        onscreen = font.render(word+" ", True, tcolour)
        word_rect = onscreen.get_rect()  # Renders each word and gets the rect of that word
        if word_rect.width + padding*2 + linelength > text_rect.width:  # If the word is going to go off the textbox, then
            linelength = 0  # Move it to the start of next line
            linecount += 1  # Add a new line
        x = text_rect.topleft[0] + padding + linelength  # x position is the x coordinate of the text box, plus left
        # side padding, plus the existing line length
        y = text_rect.topleft[1] + padding + word_rect.height * (linecount-1)  # y position is the y coordinate of the
        # text box, plus padding from the top, plus height of all previous lines.
        # I'm using linecount-1 because it takes the y value of the top left corner, and the number of lines above the
        # current line is linecount-1.
        word_rect.topleft = (x, y)  # Sets the position for the word
        linelength += word_rect.width  # Updates line length
        screen.blit(onscreen, word_rect)
    text_rect.height = padding * 2 + word_rect.height * linecount  # Updates text box height, which is the top and bottom
    # padding + height of all the lines


def clue1(screen):
    global talking

    # Blits images
    if not intro:  # Displays intro message
        display_message(screen, messages[0], message_rect, BLACK, WHITE, 15, True)
    if not won:  # Only shows Parry if the game isn't finished, because at the end he will fly out of the cage
        screen.blit(bird, bird_rect)
    screen.blit(bird_cage, (45, 0))
    if progress == 0:
        screen.blit(cookies, cookie_rect)  # Only shows the cookies if the player hasn't already found them

    # Displaying messages
    if progress == 1 and popup:  # If the player has just found the cookie and hasn't dismissed the pop up yet.
        display_message(screen, messages[progress], message_rect, BLACK, WHITE, 15, True)
    elif progress == 2 and popup:  # If the player gave a cookie to Parry
        display_message(screen, messages[progress], message_rect, BLACK, WHITE, 15, True)

    # Timed dialogue for Parry
    if talking:
        display_message(screen, hints[random_clue], hint_rect, BLACK, WHITE, 15, True)
    if talking and timer-start > 4:  # If Parry's dialogue box has been displaying for more than 4 seconds, turn it off
        talking = False


def clue2(screen):
    if progress < 4:  # Blits sticky note to screen, if the player hasn't picked it up already
        screen.blit(sticky_note, note_rect)

    # Displays messages
    if progress == 3 and not unlock_warning and popup:  # If the player found the phone after talking to Parry
        # but before getting the note. The unlock_warning boolean stops this initial message from appearing again if the
        # user tries to unlock the phone without finding the note first
        display_message(screen, messages[progress], message_rect, BLACK, WHITE, 15, True)
    elif progress == 3 and unlock_warning and popup:  # Shows warning message if the player tries to unlock the phone without the note
        display_message(screen, "Find the note first!", message_rect, BLACK, WHITE, 15, True)
    elif progress == 4 and popup:  # If the player finds the note after finding the phone
        display_message(screen, messages[progress], message_rect, BLACK, WHITE, 15, True)

    # Displays the phone/note
    if phoneout and not unlocked:  # Shows the unlocking screen, prompting the user to enter a password
        screen.blit(phone_unlock, phone_rect)
        screen_rect = pygame.Rect(0, 0, 140, 50)
        screen_rect.topleft = (330, 280)
        display_message(screen, "Password: " + text, screen_rect, WHITE, PHONESCREEN, 15, False)
    elif phoneout and unlocked:  # If the phone is already unlocked, then show the notes app
        screen.blit(phone_notes, phone_rect)
    if noteout:  # Shows the sticky note
        screen.blit(big_sticky, (300, 200))


def phone_interaction(key):
    global unlock_warning, popup, phoneout, noteout, text, unlocked

    if popup and progress >= 4:
        popup = False  # Automatically turns off any popups currently on screen if the player opens the note/phone

    # Pulls out or puts back phone/note
    if key == pygame.K_TAB and progress == 3:  # Only allows player to open the phone after obtaining the note
        unlock_warning = True
        popup = True
    elif key == pygame.K_TAB and progress >= 4:  # If the player tries to open the phone after getting the note
        phoneout = not phoneout  # Reverses the current phone state. If it was shown then hide it, if it was hidden then show it
        if noteout:  # Puts back the note if it is currently out, so that only the note/phone is on screen at a time
            noteout = False
        text = ""  # Resets text input to be blank
    if key == pygame.K_LSHIFT and progress >= 4:  # Similar to phoneout, but for the note
        noteout = not noteout
        if phoneout:
            phoneout = False

    # Phone input/password checking
    if key == pygame.K_SPACE and phoneout and not unlocked:  # If the user has the phone out and hasn't unlocked it yet
        entered_password = text.strip()
        if entered_password != phone_password:  # Incorrect password, plays incorrect sound and resets input
            incorrect.play()
            text = ""
        else:  # Correct password, turns unlocked to true
            correct.play()
            unlocked = True
    elif key == pygame.K_BACKSPACE and phoneout and not unlocked:  # Deletes a character
        text = text[:-1]
    elif phoneout and len(text.strip()) < 4 and not unlocked:  # Only allows player to enter four digits, max
        text += event.unicode


def clue3(screen):
    global won

    # Blit images
    if progress < 5:  # Draws the watering can if the player hasn't found it yet
        screen.blit(watering_can, water_rect)
    if progress == 5 and popup:  # If the player has found the watering can
        display_message(screen, messages[progress], message_rect, BLACK, WHITE, 15, True)

    # Dragging
    mx, my = pygame.mouse.get_pos()
    if drag:
        dragging_rect = watering_can.get_rect(center=(mx, my))
        screen.blit(watering_can, dragging_rect)  # If the player is dragging the watering can, then draw it centered at the mouse cursor
        if plant_rect.collidepoint(mx, my) and not won:  # If the watering can is dragging and touches the plant, then the player has won
            won = True
            victory_music.play()


def mouse_clicked(mx, my):  # Master function controlling all events based on mouse clicks
    global intro, progress, popup, has_items, talking, start, random_clue, unlock_warning, drag, easter_egg, easter_start, secrets_found, congrats
    if intro == False:  # Turns off introduction message
        intro = True
    elif cookie_rect.collidepoint(mx, my) and progress == 0:  # If the player finds the cookies for the first time.
        progress += 1
        popup = True  # Shows the popup for getting the cookie
        has_items[0] = True  # Draw cookies in the inventory
        found_item.play()  # Plays the discovery sound effect
    elif bird_rect.collidepoint(mx, my) and progress == 1:  # If the player has found the cookie and clicks on Parry
        progress += 1
        popup = True
        found_item.play()
    elif bird_rect.collidepoint(mx, my) and progress >= 2 and not talking:  # If the player has already made friends with Parry and wants some dialogue
        start = timer  # Resets the start time equal to the timer for timed events, only if there is no timed dialogue currently on screen
        # This way even if the player spam clicks, the timed dialogue will still disappear instead of staying on screen forever.
        talking = True  # Turns on talking
        hint_rect.topleft = (random.randint(140, 170), random.randint(70, 100))  # Randomizes the hint text box position
        random_clue = random.randint(0, len(hints)-1)  # Picks a random line of dialogue
        if random_clue == 4 and not secrets_found[0]:  # If the random message was the easter egg, display its congratulation message
            easter_egg = 0  # The number of the easter egg variable is also the list index of the achievement name and image
            if not congrats:  # There's two separate timers, one for Parry's dialogue and one for the easter egg popup so they don't interfere
                easter_start = timer
            congrats = True  # Boolean used to later turn off easter egg popup
    elif pillow_rect.collidepoint(mx, my) and progress == 2:  # If the player finds the phone after getting clues from Parry
        progress += 1
        popup = True
        has_items[1] = True  # Draw the phone in the inventory
        found_item.play()
    elif note_rect.collidepoint(mx, my) and progress == 3:  # If the player finds the note after getting the phone
        progress += 1
        unlock_warning = False  # Allows the player to actually try and unlock the phone
        popup = True
        has_items[2] = True
        found_item.play()
    elif water_rect.collidepoint(mx, my) and progress == 4 and unlocked:  # If the player gets the watering can after unlocking the phone
        progress += 1
        popup = True
        has_items[3] = True
        found_item.play()
    elif progress == 5 and 700 <= mx <= 765 and 520 <= my <= 585:  # If the player has the watering can and drags from the inventory, it'll follow the cursor
        drag = True
        has_items[3] = False  # This stops the inventory function from drawing the watering can while it's being dragged, as if the player took it out of their inventory
    elif coffee_rect.collidepoint(mx, my) and not secrets_found[1]:  # If the player clicks on the coffee cup for the first time, show them the secret message
        easter_egg = 1
        if not congrats:
            easter_start = timer
        congrats = True
    elif hat_rect.collidepoint(mx, my) and not secrets_found[2]:  # If the player clicks on the hat, show them the secret message
        easter_egg = 2
        if not congrats:
            easter_start = timer
        congrats = True


def draw_inventory(screen, startx, starty, size):
    for i in range(len(items)):  # Uses a for loop to draw the inventory boxes based on number of items, which is 4.
        pygame.draw.rect(screen, LIGHTBLUE, (startx + size*i, starty, size, size))
        pygame.draw.rect(screen, WHITE, (startx + size*i, starty, size, size), 5)
        if has_items[i]:  # If this index of has_items is true meaning the player has that item, draw its thumbnail in the connected list
            item_rect = items[i].get_rect(center=(startx + i*size + size//2, starty + size//2))  # Sets the center for the item thumbnail, based on each box's dimensions of 70 by 70.
            screen.blit(items[i], item_rect)


def achievements(screen, start, timer, tcolour, tbcolour, congrats_rect, size):  # Essentially a combination of the display message and timed clue functions
    global congrats, secrets_found

    font = pygame.font.SysFont("Times new roman", size)
    linelength = 0
    padding = 20
    words = ["Secret found:"]
    words.extend(achievement_messages[easter_egg].split())  # Prepares the message for that specific easter egg

    # Draws textbox and text
    pygame.draw.rect(screen, tbcolour, congrats_rect)
    pygame.draw.rect(screen, tcolour, congrats_rect, 2)
    for word in words:
        onscreen = font.render(" " + word, True, tcolour)
        word_rect = onscreen.get_rect()
        x = congrats_rect.topleft[0] + padding + linelength
        y = congrats_rect.topleft[1] + padding
        word_rect.topleft = (x, y)
        linelength += word_rect.width
        screen.blit(onscreen, word_rect)
    congrats_rect.width = linelength + padding*5  # After blitting all the words, update the length of the text rectangle to also make room for the image.
    # Padding * 5 gives the image 60px of space on the right side. There will be two that makes up the left and right padding for the text, and the
    # remaining 3 will be the space for the image and 3 * 20 = 60.

    # Displays image accompanying text
    image_rect = achievement_images[easter_egg].get_rect(center=(congrats_rect.width - 30, congrats_rect.height // 2))
    screen.blit(achievement_images[easter_egg], image_rect)

    if congrats and timer - start > 4:  # Only displays the text if this is the first time the secret was found
        congrats = False  # Turns off the text if it has been more than 4 seconds
        secrets_found[easter_egg] = True  # Set the index in secrets_found to be true so that this only works once


def victory(screen):
    global birdX, bird_dir

    # Displays text
    font = pygame.font.SysFont("Times new roman", 60)
    victory_message = font.render("You win, congratulations!", True, BLACK)
    victory_rect = victory_message.get_rect(center=(screen.get_width()/2, screen.get_height()/2))

    # Draws background
    victory_background = victory_rect.copy()
    victory_background.width = victory_rect.width * 1.2
    victory_background.height = victory_rect.height * 1.2
    victory_background.center = (screen.get_width()/2, screen.get_height()/2)
    pygame.draw.rect(screen, BLACK, victory_background, 7)
    pygame.draw.rect(screen, WHITE, victory_background)
    screen.blit(victory_message, victory_rect)

    birdX += 5 * bird_dir
    if birdX <= -100 or birdX >= 800:  # If Parry is off screen
        bird_dir *= -1  # Reverse his direction
    if bird_dir == -1:
        screen.blit(bird_sprite[framecount//2%len(bird_sprite)], (birdX, 80))  # Draws the sprite depending on his current direction
    else:
        screen.blit(pygame.transform.flip(bird_sprite[framecount//2%len(bird_sprite)], True, False), (birdX, 80))


def scene_draw(screen):
    screen.blit(background, (0, 0))
    #draw_gridlines(screen)
    draw_inventory(screen, 490, 520, 70)


# main
while running:
    framecount += 1
    timer = framecount//60  # Creates a timer in seconds
    scene_draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if user has clicked 'x' to exit program
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if popup == True:  # Turns off any popups currently on screen
                popup = False
            mx, my = event.pos
            mouse_clicked(mx, my)

        elif event.type == pygame.KEYDOWN and progress >= 3:  # Calls the function for phone interaction
            phone_interaction(event.key)

        elif event.type == pygame.MOUSEBUTTONUP and progress == 5 and drag:  # If the player has just finished dragging
            drag = False  # Stops drag if the player lets go of the mouse
            has_items[3] = True  # Redraws the watering can in the inventory like the player has put it back

    clue1(screen)
    clue2(screen)
    clue3(screen)

    if congrats and not secrets_found[easter_egg]:  # Calls achievements to display an easter egg message if it hasn't been discovered yet
        achievements(screen, easter_start, timer, BLACK, WHITE, congrats_rect, 15)
    if won:  # Calls victory function
        victory(screen)

    display_coordinates(screen)
    pygame.display.flip()
    myClock.tick(60)
pygame.quit()