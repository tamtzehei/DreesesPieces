# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:03:32 2019

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

print('text_to_cmd 1')

module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

messages = [
    "Bug dick dominick",
    "Deposit 5 dollars in account number 1117",
    "How much money did I send to Joanna?",
    "What is my Balance",
    "Transfer 5 dollars from account 11117 to 11115"]
commands = [
    "withdraw",
    "deposit",
    "transfer",
    "balance","not a command"]

print('text_to_cmd 2')

def run(session_, input_tensor_, messages_, encoding_tensor):
  message_embeddings_ = session_.run(
      encoding_tensor, feed_dict={input_tensor_: messages_})
  corr = get_similarity_matrix(messages_, message_embeddings_)
  return corr

def get_similarity_matrix(command_set,features):
  corr = np.inner(features, features)
  return corr

def return_command_type(text):
    messages.append(text)
    similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
    similarity_message_encodings = embed(similarity_input_placeholder)
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        session.run(tf.tables_initializer())
        corr_matrix = run(session, similarity_input_placeholder, messages,
               similarity_message_encodings)
    corr_matrix[len(messages)-1,len(messages)-1] = 0
    return commands[np.argmax(corr_matrix[:,len(messages)-1],axis = 0)]