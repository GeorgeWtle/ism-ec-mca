## Other imports
from os import listdir
import string
import re
import warnings
import subprocess

import numpy as np
import xarray as xr
from xmca.xarray import xMCA
from datetime import datetime
import pandas as pd
import seaborn as sb
import xskillscore as xs
from scipy.stats import *
import statsmodels.api as sm

import geocat.viz as gv

import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point

from shapely.ops import unary_union
import shapely.geometry as shp
from skimage import measure

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import Polygon

