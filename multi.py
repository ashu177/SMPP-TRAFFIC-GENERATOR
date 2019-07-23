# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:47:08 2019

@author: comviva
"""

import multiprocessing
import time
import sys
import redis


red=redis.Redis("localhost")
red.set("pause","1")
#print("in pause",pause)