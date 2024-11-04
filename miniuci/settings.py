import pygame

##################################################
# Main cell size (this controls everything else) #
##################################################

CELL_SIZE = 80

##############
# Active bar #
##############

ACTIVE_BAR_X = 0
ACTIVE_BAR_Y = 0
ACTIVE_BAR_WIDTH = CELL_SIZE * 0.25
ACTIVE_BAR_HEIGHT = CELL_SIZE * 8

############
# Eval bar #
############

EVAL_BAR_X = ACTIVE_BAR_WIDTH
EVAL_BAR_Y = 0
EVAL_BAR_WIDTH = CELL_SIZE * 0.25
EVAL_BAR_HEIGHT = CELL_SIZE * 8

#########
# Board #
#########

BOARD_X = ACTIVE_BAR_WIDTH + EVAL_BAR_WIDTH
BOARD_Y = 0
BOARD_SIZE = CELL_SIZE * 8
BOARD_LIGHT_SQUARE_COLOR = pygame.Color(0xF0, 0xD9, 0xB5)
BOARD_DARK_SQUARE_COLOR = pygame.Color(0xB5, 0x88, 0x63)
BOARD_FROM_SQUARE_COLOR = pygame.Color(0xFF, 0x00, 0x00)
BOARD_BEST_SQUARE_COLOR = pygame.Color(0xFF, 0xFF, 0x00)

################
# Window stuff #
################

WINDOW_WIDTH = ACTIVE_BAR_WIDTH + EVAL_BAR_WIDTH + BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE
