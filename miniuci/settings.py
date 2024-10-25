import pygame

##################################################
# Main cell size (this controls everything else) #
##################################################

CELL_SIZE = 80

LIGHT_SQUARE_COLOR = pygame.Color(0xF0, 0xD9, 0xB5)
DARK_SQUARE_COLOR = pygame.Color(0xB5, 0x88, 0x63)

#########
# Board #
#########

BOARD_SIZE = CELL_SIZE * 8

############
# Eval bar #
############

EVAL_BAR_WIDTH = CELL_SIZE / 4
EVAL_BAR_HEIGHT = BOARD_SIZE

################
# Window stuff #
################

WINDOW_WIDTH = EVAL_BAR_WIDTH + BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE
