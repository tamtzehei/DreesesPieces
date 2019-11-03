# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:08:50 2019

@author: Romik
"""

from absl import logging

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

tf.compat.v1.enable_resource_variables()

module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

embed = hub.Module(module_url)

tf.saved_model.save(embed, 'embed_v2', signatures=None)

