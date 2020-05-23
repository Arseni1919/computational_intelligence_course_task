import pygame
import sys
import os.path
import random
import logging
import threading
import time
import concurrent.futures
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import numpy as np
import pickle
import copy
from scipy.stats import t
from scipy import stats
import itertools
# from tqdm import tqdm
from pprint import pprint
import statistics

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_COLOR = (2, 189, 164)
PADDING = 2
CELL_SIZE = 10
OCCUPIED_COLOR = (0, 0, 0)
NOT_OCCUPIED_COLOR = (255, 255, 255)
PIVOT_COLOR = (75, 145, 219)
PIVOT_CLOSED_COLOR = (157, 75, 219)
STRART_COLOR = (237, 255, 33)
END_COLOR = (33, 255, 81)
CLOSED_COLOR = (255, 131, 122)
OPEN_COLOR = (212, 252, 177)
PATH_COLOR = (153, 0, 140)
EMPTY_COLOR = (255, 255, 255)

PREPARE_AND_RUN_TITLE = 'PREPARE AND RUN'
RESET_TITLE = 'RESET'


# (0, 0, 255, 20)
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)