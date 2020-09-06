import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#Use when needed
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]


# # Read csv file 
df = pd.read_csv("content.csv")
#print(df.columns) #shows the columns
#print(df.head())# shows top 5 indexs data

# #Selecting some features which helps in recommendations
features = ['brand','categories','keys','manufacturer'] #pre cleaned datas

#create new column in df with combined selected features
for feature in features:
	df[features] =  df[features].fillna('') #fill the Nan values with empty strings since in data keywords contins all Nan values

def combine_features(row): #takes entire row as input 
	try:
		return row['brand']+" "+ row['categories']+" "+ row['keys']+" "+ row['manufacturer']
	except:
		print("Error:", row) #shows the eroor

df["combine_features"] = df.apply(combine_features, axis=1) #combines rows, axis used for pass data in rows 
#print("Combined features",df["combine_features"].head())

# #creating count matrix from new combined column
cv = CountVectorizer() #creating new CountVectorizer() object
count_matrix = cv.fit_transform(df["combine_features"])
#print (count_matrix)
#Compute cosine similarity
cosine_sim = cosine_similarity(count_matrix)

product_user_likes = "Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta"

# #get index of this movie from its  title or we can say matrix of the movie
product_index = get_index_from_title(product_user_likes) #gives index of the movie selected

similar_product = list(enumerate(cosine_sim[product_index])) #gives list of tuples with indexes

# #sort and arrange in descending order

sorted_similar_product = sorted(similar_product,key= lambda x:x[1], reverse= True) #lambda for sorting second index of tuples
#and reverse for descending order
i=0
print("Similar products to "+ product_user_likes +" are:\n")
for element in sorted_similar_product:
    print(get_title_from_index(element[0]))
    i=i+1
    if i>50:
        break