#!/usr/bin/env python
# coding: utf-8

# # Welcome to Jupyter!

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
import string
import hmac
import seaborn as sns


e = 2**52
salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c"


# In[2]:


game_hash = '100af1b49f5e9f87efc81f838bf9b1f5e38293e5b4cf6d0b366c004e0a8d9987'

def get_result(game_hash):
    hm = hmac.new(str.encode(game_hash), b'', hashlib.sha256)
    hm.update(salt.encode("utf-8"))
    h = hm.hexdigest()
    if (int(h, 16) % 20 == 0): ## they increased insta-crash from 3% to 5% now.
        return 1
    h = int(h[:13], 16)
    return (((100 * e - h) / (e-h)) // 1) / 100.0

def get_prev_game(hash_code):
    m = hashlib.sha256()
    m.update(hash_code.encode("utf-8"))
    return m.hexdigest()


# In[3]:


first_game = "77b271fe12fca03c618f63dfb79d4105726ba9d4a25bb3f1964e435ccf9cb209"
most_recent = "7bc71aa79b66f474c397a82e7a21d963255217231cc83eff57f24609bbcb39e4"

results = []
count = 0

while most_recent != first_game:
    count += 1
    results.append(get_result(most_recent))
    most_recent = get_prev_game(most_recent)

print(count)


# In[5]:


results = np.array(results)


# In[6]:


### Probabilities
multiplier = 1.99
(results <= multiplier).mean(), 1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier))
## observed prob vs expected prob


# In[7]:


### EV
## expected EV
multiplier = 1.05
((1/33) + (32/33)*(.01 + .99*(1 - 1/(multiplier-.01))))*-1 + (multiplier-1)*(1 - ((1/33) + (32/33)*(.01 + .99*(1 - 1/(multiplier-.01)))))


# In[8]:


## actual EV
(results < multiplier).mean() * -1 + (multiplier - 1)*(results >= multiplier).mean()


# In[11]:


sns.set(rc={'figure.figsize':(11.7,8.27)})

plt.hist(results, range=(0, 25))
plt.title("Histogram of Game Results", fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("Number of Games", fontsize=15)
plt.xlabel("Multiplier", fontsize=15)


# In[10]:


# pip install seaborn


# In[ ]:




