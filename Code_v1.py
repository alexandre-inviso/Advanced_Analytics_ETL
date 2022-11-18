# Databricks notebook source
# MAGIC %md
# MAGIC # Hot 100 since 1958

# COMMAND ----------

# MAGIC %md
# MAGIC Goals:
# MAGIC 
# MAGIC For next time:
# MAGIC 1) find a dataset
# MAGIC 
# MAGIC 2) Do basic EDA
# MAGIC 
# MAGIC 3) Clean data and load into graph (MOST IMPORTANT PART: make sure it is actually a network we can work)
# MAGIC 
# MAGIC Research question, what is the goal, what do we wanna knnow etc.
# MAGIC 
# MAGIC Methods for doing the research

# COMMAND ----------

import pandas as pd
import networkx as nx
import numpy as np
import matplotlib as plt
import itertools

# COMMAND ----------

df = pd.read_csv('charts.csv')
df

# COMMAND ----------

df[90:102]

# COMMAND ----------

u = df['artist'].str.split('x|&|Featuring|With|,', expand = True).add_prefix('artist_')
test = u
#test = test.dropna(subset=['artist_1'])
#test = test.groupby('artist_0')['artist_1'].apply(','.join).reset_index()
test.head()

# COMMAND ----------

# Create an empty list
Row_list =[]
  
# Iterate over each row
for index, rows in test.iterrows():
    # Create list for the current row
    my_list =[rows.artist_1, rows.artist_2, rows.artist_3, rows.artist_4, rows.artist_5, rows.artist_6, rows.artist_7, rows.artist_8, rows.artist_9]
      
    # append the list to the final list
    Row_list.append(my_list)
    
test['new_col'] = Row_list
test['new_col'] = test.new_col.apply(lambda x: [i for i in x if i != None])
test.head()

# COMMAND ----------

test = test.drop(['artist_1', 'artist_2','artist_3','artist_4','artist_5','artist_6','artist_7','artist_8','artist_9'], axis=1)





# COMMAND ----------

text = test
text

# COMMAND ----------

music = text.groupby('artist_0')['new_col'].apply(lambda x: x.sum())

# COMMAND ----------

music = music.to_frame()
music = music.reset_index()
music

# COMMAND ----------

links_explode = music.explode('new_col').reset_index(drop=True)
links_explode

# COMMAND ----------

#creating edges and lists
uni_edges = list(links_explode[['artist_0','new_col']].itertuples(index=False, name=None))

music['n_edges'] = music['artist_0'].apply(lambda x: len(x))

music_no_links = music[music['n_edges']==0]['artist_0'].values


# COMMAND ----------

music_no_links

# COMMAND ----------

music

# COMMAND ----------

#setting up network
G = nx.DiGraph()
G.add_nodes_from(music['artist_0'].values)
G.add_edges_from(uni_edges)

#removing nodes without any link
G.remove_nodes_from(music_no_links)

# COMMAND ----------

print('Q: What is the number of nodes in the network?')
print('A: The number of nodes in the network is:', G.number_of_nodes())

# COMMAND ----------

print('Q: More importantly, what is the number of links?')
print('A: The number of links in the network is:', G.number_of_edges())

# COMMAND ----------

links_explode

# COMMAND ----------

import matplotlib.pyplot as plt

# COMMAND ----------

print('Plot the in and out-degree distributions for the entire network. What do you observe? Can you explain why the in-degree distribution is different from the out-degree distribution')


grouping = links_explode.groupby('artist_0').count().values

plt.rcParams["figure.figsize"] = (15,8)
plt.hist(grouping , bins = 30, color = 'lime')
plt.title("Distribution of Songs Network - Out", fontsize=20)
plt.savefig('out_plot.png', transparent=True)
plt.show()


# COMMAND ----------

print('Plot the in and out-degree distributions for the entire network. What do you observe? Can you explain why the in-degree distribution is different from the out-degree distribution')


grouping = links_explode.groupby('new_col').count().values

plt.rcParams["figure.figsize"] = (15,8)
plt.hist(grouping , bins = 30, color='lime')
plt.title("Distribution of Songs Network - In", fontsize=20)
plt.show()

# COMMAND ----------

print('Who are the top 5 most connected Marvel characters (Report results for in-degrees and out-degrees, that is, who has highest in-degree, who has highest out-degree)? Comment on your findings. Is this what you would have expected?')
print('')
print('In:',links_explode.groupby('artist_0').count().sort_values('new_col', ascending=False).head())

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------


