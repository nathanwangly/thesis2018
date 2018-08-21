import pygame, sys
from pygame.locals import *

import ctypes
import pandas as pd

###  EXPERIMENT PARAMETERS

# COLOURS
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# FONTS
font_default = 'calibri'

# font_default_size = 22
# font_size_large = 28
# font_size_extralarge = 36

font_default_size = 26
font_size_large = 32
font_size_extralarge = 40

# # LINE SPACING
# line_spacing = display_height / 12

# NUMBER OF INSTRUCTIONS
instruction_stage_max = 6

# NUMBER OF ROUNDS
practice_rounds = 10
exp_rounds = 30

# SAVINGS
income = 500

# FINANCIAL EMERGENCY
repair_cost_dict = {'practice': 500, 'exp': 3000}

# POINT-MONEY CONVERSION RATE - $0.10 = X points
reward_rate = 400

### DATA SETUP
practice_responses = []
practice_points = []
practice_savings = []
practice_norms = []

exp_responses = []
exp_points = []
exp_savings = []
exp_norms = []

### STARTING VARIABLES

# EXPERIMENT AND INSTRUCTION STAGE
instructions_mode = 0
instruction_stage = 0
round_number = 1
mode = ''
outcome = ''

# MOUSE VARIABLES
mousex = 0
mousey = 0
mouseClicked = False

#Account Balance and Score
current_savings = 0
points_total = 0

def instructions():
    global instructions_mode, instruction_stage, instruction_stage_max, mousex, mousey, mouseClicked, condition

    displaysurf.fill(white)
    instructions_mode = True

    while instructions_mode:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

            ## Instruction pages

            # Instructions 0 - GAME INTRODUCTION
            if instruction_stage == 0:
                displaysurf.fill(white)
                instruction_string1 = 'In this experiment, you will play a financial decision-making game.'
                instruction_string2 = 'When you are ready to begin, press the NEXT button to proceed to the instructions.'

                textPrint(instruction_string1, (display_width / 2, display_height / 2.5))

                nextLine(instruction_string2)

            # Instructions 1 - GAME CONTEXT
            elif instruction_stage == 1:
                displaysurf.fill(white)
                instruction_string1 = 'You have decided that it is time to open your first savings account at the bank!'
                instruction_string2 = 'Your opening account balance is $0.'
                instruction_string3 = 'Your savings account balance can be tracked in the top left corner of the screen.'

                textPrint(instruction_string1, (display_width / 2, display_height / 2.5))

                nextLine(instruction_string2)
                nextLine(instruction_string3)

                savings_header()

            # Instructions 2 - SPENDING MONEY
            elif instruction_stage == 2:
                displaysurf.fill(white)
                instruction_string1 = 'You have a part-time job which pays you at the start of each month.'
                instruction_string2 = 'Each month, after paying your bills, you are left with a disposable income of $' + str(
                    income) + '.'
                instruction_string3 = 'You will be asked to decide how much of your money you would like to spend each month.'
                instruction_string4 = 'You can spend any amount up to your current savings account balance.'

                textPrint(instruction_string1, (display_width / 2, display_height / 2.8))

                nextLine(instruction_string2)
                nextLine(instruction_string3)
                nextLine(instruction_string4)

                savings_header()

            # Instructions 3 - EARNING POINTS
            elif instruction_stage == 3:
                displaysurf.fill(white)
                instruction_string1 = 'The money you spend will earn you points.'
                instruction_string2 = 'For every ' + str(
                    reward_rate) + ' points you earn, you will be rewarded with $0.10 of real money.'
                instruction_string3 = 'The more money you spend within a month, the more points you will earn.'
                instruction_string4 = 'Your points total can be tracked in the top right corner of the screen.'
                instruction_string5 = 'Any money that you do not spend will remain in your savings account and can be spent in a later month.'

                textPrint(instruction_string1, (display_width / 2, display_height / 3))

                nextLine(instruction_string2, bold=True)
                nextLine(instruction_string3)
                nextLine(instruction_string4)
                nextLine(instruction_string5)

                savings_header()
                points_header()

            # Instructions 4 - NUDGE INFORMATION
            elif instruction_stage == 4:
                displaysurf.fill(white)
                instruction_string1 = 'At the end of the game, you will experience a financial emergency.'
                instruction_string2 = 'If you have enough money in your savings account to cover the cost of the financial emergency, you win the game and will be rewarded based on your points score.'
                instruction_string3 = 'However, if you do not have enough money, you lose the game and will receive NO reward regardless of how many points you have previously earned.'
                instruction_string4 = 'Your objective in this game is to earn as many points as possible while saving enough to withstand the financial emergency.'
                instruction_string5 = 'Note: You will not be warned prior to the financial emergency. You will also not be told how much the financial emergency will cost.'

                textPrint(instruction_string1, (display_width / 2, display_height / 3.3))

                nextLine(instruction_string2)
                nextLine(instruction_string3)
                nextLine(instruction_string4)
                nextLine(instruction_string5, bold=True)

                savings_header()
                points_header()

            # Instructions 5 - GROUP 2
            elif instruction_stage == 5:
                displaysurf.fill(white)
                instruction_string1 = 'You are in the second group of participants to play the game.'
                instruction_string2 = 'You may or may not receive information about the first group of participants.'

                textPrint(instruction_string1, (display_width / 2, display_height / 2.5), bold=True)
                nextLine(instruction_string2)

            # Instructions 6 - COMPREHENSION CHECK
            elif instruction_stage == 6:

                displaysurf.fill(white)
                instruction_string1 = 'You will now be presented with several practice rounds.'
                instruction_string2 = 'The practice rounds are identical to the actual game rounds.'
                instruction_string3 = 'After the final practice round, there will be a financial emergency, like in the real game.'
                instruction_string4 = 'Your points score in the practice rounds will not be recorded.'
                instruction_string5 = 'Press the NEXT button when you are ready to proceed to the practice rounds.'
                textPrint(instruction_string1, (display_width / 2, display_height / 3.3))

                nextLine(instruction_string2)
                nextLine(instruction_string3)
                nextLine(instruction_string4)
                nextLine(instruction_string5)

                savings_header()
                points_header()

            nextButton_instructions()
            backButton_instructions()

        pygame.display.update()


def game_round():

    global mode, round_number, current_savings

    # refresh screen
    displaysurf.fill(white)

    game_round = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # inputbox setup
    response = ''
    valid_keys = (
        K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8,
        K_KP9)

    # first round savings
    if round_number == 1:
        current_savings = 500
    else:
        current_savings += income

    while game_round:

        savings_header()
        points_header()

        # Instructions
        instruction_string1 = 'You have saved another $' + str(income) + ' this month. Your savings account balance is now $' + str(current_savings) + '.'
        instruction_string2 = 'Please enter the amount you would like to spend this month in the box below.'
        instruction_string3 = 'Press the BACKSPACE key if you would like to edit your response.'

        textPrint(instruction_string1, (display_width / 2, display_height / 4))

        nextLine(instruction_string2)
        nextLine(instruction_string3)

        textPrint('I would like to spend:', (display_width / 2.4, display_height / 1.7), size=font_size_large, bold=True)

        # Input box dimensions
        input_box_width = 280
        input_box_height = 70

        # Amount input box
        input_box = pygame.Rect(display_width / 2, display_height / 1.8, input_box_width, input_box_height)

        pygame.draw.rect(displaysurf, black, input_box, 2)

        textPrint('Press the NEXT button when you are ready to continue.', (display_width / 2, display_height / 1.2))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

            elif event.type == KEYDOWN:

                if event.key == K_BACKSPACE:
                    response = response[:-1]
                elif event.key in valid_keys:

                    # cap response at maximum savings levels
                    new_response = response + event.unicode
                    if int(new_response) <= current_savings:
                        response = new_response

            # Cover existing input text
            input_box_cover = pygame.Rect((display_width + 4) / 2, (display_height + 4) / 1.8, input_box_width - 4, input_box_height - 4)
            pygame.draw.rect(displaysurf, white, input_box_cover)
            response_string = '$ ' + str(response)
            textPrint(response_string, (input_box.centerx, input_box.centery))

            #Remaining balance text (needs to be left aligned)

            if response == '':
                remaining_balance_string = 'Remaining Balance:                 $' + str(current_savings)

            else:
                remaining_balance = int(current_savings) - int(response)
                remaining_balance_string = 'Remaining Balance:                 $' + str(remaining_balance)

            textLeftAlign(remaining_balance_string, size=font_size_large, bold=True, top_left=(display_width / 2.82, display_height / 1.45))

                # Cover remaining balance text
            remaining_balance_cover = pygame.Rect(textLeftAlign.left, textLeftAlign.top, textLeftAlign.width + 100, textLeftAlign.height)
            pygame.draw.rect(displaysurf, white, remaining_balance_cover)

            displaysurf.blit(textLeftAlign.surface, textLeftAlign.rect)

            ## Next button
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

            # If button is hovered over, change to red
            if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                    textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
                textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
                hover = 'Y'
            else:
                hover = 'N'

            # Continue if button is clicked
            if mouseClicked == True and hover == 'Y':

                # only if response has been entered
                if len(response) != 0:

                    # score update screen
                    round_reward(int(response))
                    # update round number
                    round_number += 1

                    game_round = False

                else:
                    invalid_string = 'Please enter a value between $0 and $' + str(current_savings)
                    textPrint(invalid_string, (display_width / 2, display_height / 1.29), colour=red)
                    mouseClicked = False

            pygame.display.update()

def round_reward(money_spent):
    global mode, current_savings, points_total, points_gained, income, round_number, norm_percentage

    round_reward = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    # update score, savings
    points_conversion(money_spent)
    current_savings -= money_spent

    # Amount spent
    spending_string = 'This round you spent $' + str(money_spent) + '.'
    textPrint(spending_string, (display_width / 2, display_height / 4))

    # Points received
    points_string = 'Your spending has earned ' + str(points_gained) + ' points this round.'

    # Remaining balance
    balance_string = 'Your savings account has $' + str(current_savings) + ' remaining.'

    nextLine(points_string)
    nextLine(balance_string, bold=True)

    # Social norm
    calculate_norm(mode, round_number, current_savings)
    norm_percentage = int(calculate_norm.percentage)

    # If percentage is given to 2 decimal places
    # norm_percentage = '{0:.2f}'.format(calculate_norm.percentage)
    norm_string = str(norm_percentage) + '% of previous participants had saved more than you by this month.'
    nextLine(norm_string, bold=True, colour=red)

    # Points total
    points_total_string = 'Total score: ' + str(points_total) + ' points'
    textPrint(points_total_string, (display_width / 2, display_height / 1.3))

    data_storage(mode, money_spent, points_total, current_savings, norm_percentage)

    while round_reward:

        ## Next button
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            round_reward = False

        pygame.display.update()

def financial_emergency():

    financial_emergency = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    savings_header()
    points_header()

    textPrint('FINANCIAL EMERGENCY!', (display_width / 2, display_height / 4), bold=True, size=font_size_extralarge, colour=red)

    # Flood image
    floodImg = pygame.image.load('flood.jpg')

    # Scale image
    floodImg_width = floodImg.get_width()
    floodImg_height = floodImg.get_height()
    scale_factor = 3
    floodImg_scaledwidth = int(round(floodImg_width / scale_factor))
    floodImg_scaledheight = int((floodImg_height / scale_factor))
    floodImg = pygame.transform.scale(floodImg, (floodImg_scaledwidth, floodImg_scaledheight))

    displaysurf.blit(floodImg,
                     ((display_width - floodImg_scaledwidth) / 2, (display_height - floodImg_scaledheight) / 2))

    # Draw border
    flood_border = pygame.Rect((display_width - floodImg_scaledwidth) / 2, (display_height - floodImg_scaledheight) / 2,
                               floodImg_scaledwidth, floodImg_scaledheight)

    pygame.draw.rect(displaysurf, black, flood_border, 2)

    textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10))

    textPrint('Oh no! There was a severe storm and your house was damaged due to a flood.', (display_width / 2, display_height / 1.4))
    nextLine('Hopefully you have saved enough to cover the repair costs!')

    while financial_emergency:

        ## Next button
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            financial_emergency = False

        pygame.display.update()

def financial_emergency_calculation():
    global mode, outcome

    financial_emergency_calculation = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    # Set repair cost based on mode (practice/exp)
    repair_cost = repair_cost_dict[mode]

    textPrint('The repair bill comes to a total of $' + str(repair_cost) + '.', (display_width / 2, display_height / 4), size=font_size_extralarge)

    textRightAlign('Your account balance:', size=font_size_large, bold=True, top_right=(display_width / 2, display_height / 2))
    textRightAlign('Repair cost:', size=font_size_large, bold=True, colour=red, top_right=(display_width / 2, display_height / 1.7))
    textRightAlign('Your remaining balance:', size=font_size_large, bold=True, top_right=(display_width / 2, display_height / 1.35))

    account_savings_string = '$' + str(current_savings)
    textLeftAlign(account_savings_string, size=font_size_large, bold=True, top_left=(display_width / 1.8, display_height / 2))

    repair_cost_string = '$' + str(repair_cost)
    textLeftAlign(repair_cost_string, size=font_size_large, bold=True, colour=red, top_left=(display_width / 1.8, display_height / 1.7))

    pygame.draw.line(displaysurf, black, (display_width / 5, display_height / 1.5), (display_width * 4 / 5, display_height / 1.5), 5)

    # Calculating remaining balance
    remaining_balance = int(current_savings) - int(repair_cost)

        #Red text if negative balance, green text if positive balance
    if remaining_balance < 0:
        text_colour = red
        remaining_balance = remaining_balance * -1
        remaining_balance_string = '- $' + str(remaining_balance)
        outcome = 'lose'

    else:
        text_colour = black
        remaining_balance_string = '$' + str(remaining_balance)
        outcome = 'win'

    textLeftAlign(remaining_balance_string, size=font_size_large, bold=True, colour=text_colour, top_left=(display_width / 1.8, display_height / 1.35))

    while financial_emergency_calculation:

        ## Next button
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            financial_emergency_calculation = False

        pygame.display.update()

def game_outcome():
    global mode, outcome, reward

    game_outcome = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    score_string = 'Your final score: ' + str(points_total) + ' points'
    textPrint(score_string, (display_width / 2, display_height / 3), bold=True, size=font_size_extralarge, colour=blue)

    # Inverse norm information ( 100 - norm_percentage )
    norm_percentage2 = int(100 - float(norm_percentage))
    norm_string = 'In that game, you saved more money than ' + str(norm_percentage2) + '% of other players.'

    # Display message based on win/loss
    if outcome == 'win':

        outcome_string = 'Congratulations! You had enough money saved to cover the repair costs.'
        reward_string = 'You will receive $0.10 for every ' + str(reward_rate) + ' points you have earned.'

        textPrint(norm_string, (display_width / 2, display_height / 1.9), size=font_size_extralarge)
        nextLine(outcome_string, size=font_size_extralarge)
        nextLine(reward_string, size=font_size_extralarge)

        #Calculate reward
        reward = int(points_total / reward_rate)
        reward = '{0:.2f}'.format(reward * 0.1)

        if mode == 'practice':
            payment_string = 'Your performance in the practice rounds would have won $' + str(reward) + '.'

        elif mode == 'exp':
            payment_string = 'You have earned $' + str(reward) + ' in this experiment.'

        nextLine(payment_string, size=font_size_extralarge)

    elif outcome == 'lose':

        outcome_string = 'Unfortunately, you did not have enough money saved to cover the repair costs.'

        if mode == 'practice':
            loss_string = 'As a result, your performance in the practice rounds would not have won any real money.'

        elif mode == 'exp':
            loss_string = 'As a result, you will not be rewarded for the points you earned during the game.'

        textPrint(norm_string, (display_width / 2, display_height / 1.9), size=font_size_extralarge)
        nextLine(outcome_string, size=font_size_extralarge)
        nextLine(loss_string, size=font_size_extralarge)

    while game_outcome:

        ## Next button
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            game_outcome = False

        pygame.display.update()

def instructions2():
    global mode, outcome

    instructions2 = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    instruction_string1 = 'You have completed the practice rounds for the experiment.'
    instruction_string2 = 'You will now begin the experimental rounds. Your points and account balance have been reset.'
    instruction_string3 = 'Note: The repair cost will not be the same for the experimental rounds. It will cost at least $1500.'
    instruction_string4 = 'Press the NEXT button when you are ready to proceed to the experimental rounds.'

    textPrint(instruction_string1, (display_width / 2, display_height / 3))
    nextLine(instruction_string2)
    nextLine(instruction_string3, bold=True)
    nextLine(instruction_string4)

    while instructions2:

        ## Next button
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            instructions2 = False

        pygame.display.update()

def experiment_end():

    global outcome, reward

    experiment_end = True

    # mouse variables
    mousex = 0
    mousey = 0
    mouseClicked = False

    # refresh screen
    displaysurf.fill(white)

    score_string = 'Your final score: ' + str(points_total) + ' points'
    textPrint(score_string, (display_width / 2, display_height / 3), bold=True, size=font_size_extralarge, colour=blue)

    textPrint('Thank you for participating in this experiment :)', (display_width / 2, display_height / 2), size=font_size_large)

    finished_string = 'Please let the experimenter know that you are finished!'

    if outcome == 'win':
        reward_string = 'You have won $' + str(reward) + '.'

        nextLine(reward_string, size=font_size_large)
        nextLine(finished_string, size=font_size_large)

    elif outcome == 'lose':
        nextLine(finished_string, size=font_size_large)

    while experiment_end:

        ## Next button
        textPrint('Finish', (display_width * 1 / 10, display_height * 9 / 10), bold=True, colour=white)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if mouse moves
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mouseClicked = False

            # if mouse is clicked
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Finish', (display_width * 1 / 10, display_height * 9 / 10), bold=True, colour=red)
            hover = 'Y'
        else:
            hover = 'N'

        # Continue if button is clicked
        if mouseClicked == True and hover == 'Y':
            experiment_end = False

        pygame.display.update()

def points_conversion(money_spent):
    global points_total, points_gained

    S = money_spent

    if S <= 250 or S >= 5000:
        points_gained = S
        points_gained = int(round(points_gained))

    elif 750 >= S > 250:
        points_gained = ((S ** 2) - (3000 * S) + 562500) / -500
        points_gained = int(round(points_gained))

    else:
        points_gained = ((11 * (S ** 2)) - (110000 * S) - 86250000) / -72250
        points_gained = int(round(points_gained))

    points_total += points_gained

def textPrint(text, centre, size=font_default_size, bold=False, colour=black, background=white):
    global displaysurf

    fontObj = pygame.font.SysFont(font_default, size, bold)
    textSurfaceObj = fontObj.render(text, True, colour, background)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = centre

    textPrint.width = textSurfaceObj.get_width()
    textPrint.height = textSurfaceObj.get_height()
    textPrint.centre = centre

    displaysurf.blit(textSurfaceObj, textRectObj)

def textLeftAlign(text, size=font_default_size, bold=False, colour=black, background=white, top_left=(0,0)):
    global font_default

    fontObj = pygame.font.SysFont(font_default, size, bold)
    textSurfaceObj = fontObj.render(text, bold, colour, background)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = top_left

    # For calling outside function
    textLeftAlign.left = textRectObj.left
    textLeftAlign.top = textRectObj.top
    textLeftAlign.width = textRectObj.width
    textLeftAlign.height = textRectObj.height
    textLeftAlign.surface = textSurfaceObj
    textLeftAlign.rect = textRectObj

    displaysurf.blit(textSurfaceObj, textRectObj)

def textRightAlign(text, size=font_default_size, bold=False, colour=black, background=white, top_right=(0,0)):
    global font_default

    fontObj = pygame.font.SysFont(font_default, size, bold)
    textSurfaceObj = fontObj.render(text, bold, colour, background)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topright = top_right

    # For calling outside function
    textRightAlign.left = textRectObj.left
    textRightAlign.top = textRectObj.top
    textRightAlign.width = textRectObj.width
    textRightAlign.height = textRectObj.height
    textRightAlign.surface = textSurfaceObj
    textRightAlign.rect = textRectObj

    displaysurf.blit(textSurfaceObj, textRectObj)

def savings_header():
    global current_savings

    # Savings account balance
    savings_string = 'Account Balance: $' + str(current_savings)
    textPrint(savings_string, (display_width / 10, display_height / 10))

def points_header():
    global points_total

    # Points score
    points_string = 'Score: ' + str(points_total) + ' points'
    textPrint(points_string, (display_width * 9 / 10, display_height / 10))

def nextLine(text, bold=False, size=font_default_size, colour=black):
    global line_spacing

    textPrint(text, centre=(textPrint.centre[0], textPrint.centre[1] + line_spacing), bold=bold, size=size, colour=colour)

def nextButton_instructions():
    global instructions_mode, instruction_stage, instruction_stage_max, mousex, mousey, mouseClicked

    ## Next button
    textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True)

    # If button is hovered over, change to red
    if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
            textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
        textPrint('Next', (display_width * 9 / 10, display_height * 9 / 10), bold=True, colour=red)
        hover_next = 'Y'
    else:
        hover_next = 'N'

    # Continue if button is clicked
    if mouseClicked == True and hover_next == 'Y':
        instruction_stage += 1

        # End Instruction Stage
        if instruction_stage > instruction_stage_max:
            instructions_mode = False

def backButton_instructions():
    global instruction_stage, mousex, mousey, mouseClicked

    if instruction_stage != 0:
        ## Back button
        textPrint('Back', (display_width / 10, display_height * 9 / 10), bold=True)

        # If button is hovered over, change to red
        if textPrint.centre[0] + textPrint.width / 2 > mousex > textPrint.centre[0] - textPrint.width / 2 and \
                textPrint.centre[1] + textPrint.height / 2 > mousey > textPrint.centre[1] - textPrint.height / 2:
            textPrint('Back', (display_width / 10, display_height * 9 / 10), bold=True, colour=red)
            hover_back = 'Y'
        else:
            hover_back = 'N'

        # Go back if button is clicked
        if mouseClicked == True and hover_back == 'Y':
            instruction_stage -= 1

def calculate_norm(mode, round_number, current_savings):

    # Variable column name based on mode and round number
    column_name = str(mode) + str(round_number)

    # Obtain correct list
    norm_data = list(dfNorm[column_name])

    # Count percentage of savings which are greater than participant's score
    count_greater = sum(i > current_savings for i in norm_data)
    percentage_greater = count_greater * 100 / len(norm_data)

    calculate_norm.percentage = percentage_greater

def data_storage(mode, money_spent, points_total, current_savings, norm_percentage):

    if mode == 'practice':
        practice_responses.append(money_spent)
        practice_points.append(points_total)
        practice_savings.append(current_savings)
        practice_norms.append(norm_percentage)

    elif mode == 'exp':
        exp_responses.append(money_spent)
        exp_points.append(points_total)
        exp_savings.append(current_savings)
        exp_norms.append(norm_percentage)

def data_output():
    output_list = []

    data_list = [participant_ID, practice_responses, practice_points, practice_savings, practice_norms, exp_responses, exp_points,
                 exp_savings, exp_norms]

    for data in data_list:
        output_list.append(data)

    output_list = [item for sublist in output_list for item in sublist]

    dfNew = pd.DataFrame([output_list])

    # Compatibility with Python 2.7
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # Import from previous Participant File
        prev_participant_ID = participant_ID[0] - 1
        inputFileName = str(prev_participant_ID) + '.xlsx'
        dfExisting = pd.read_excel(inputFileName)

    except FileNotFoundError:
        inputFileName = 'Blank Sheet.xlsx'
        dfExisting = pd.read_excel(inputFileName)

    dfExisting = dfExisting.append(dfNew, ignore_index=True)

    # Output to new Participant File
    outputFileName = str(participant_ID[0]) + '.xlsx'
    dfExisting.to_excel(outputFileName, index=False)

def game_init():

    global display_width, display_height, displaysurf, line_spacing

    pygame.init()

    ### LOAD FULL SCREEN

    ctypes.windll.user32.SetProcessDPIAware()
    true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
    displaysurf = pygame.display.set_mode(true_res, pygame.FULLSCREEN)

    display_width, display_height = displaysurf.get_size()

    # LINE SPACING
    line_spacing = display_height / 12

def participant_ID():

    global participant_ID

    participant_ID = []
    participant_ID.append(int(input('Enter Participant ID: ')))


def main():

    global mode, points_total, current_savings, round_number, dfNorm

    ### NORM DATA LOAD
    dfNorm = pd.read_excel('Comparison Data.xlsx')

    participant_ID()

    game_init()

    # Starting exp instructions
    instructions()

    # Practice rounds
    mode = 'practice'
    for i in range(practice_rounds):
        game_round()
    financial_emergency()
    financial_emergency_calculation()
    game_outcome()

    # Transition from practice rounds to exp rounds
        # Reset score, balance and round numbers
    points_total = 0
    current_savings = 0
    round_number = 1

    instructions2()

    # Experimental rounds
    mode = 'exp'
    for i in range(exp_rounds):
        game_round()
    financial_emergency()
    financial_emergency_calculation()
    game_outcome()

    experiment_end()

    data_output()

main()