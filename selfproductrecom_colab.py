import pandas as pd

ratings = pd.read_csv("ratings.csv")
products = pd.read_csv("prodcutamazon.csv",header= 0, encoding= 'unicode_escape')

# print(ratings)
# print(products)

ratings = pd.merge(products,ratings)
#print(ratings.head())

user_ratings = ratings.pivot_table(index=['username'],columns=['name'],values='ratings')#change matrix rows and columns
#print(user_ratings.head())

#remove movies which have less than 10 users who rated it
# user_ratings = user_ratings.dropna(thresh=2,axis=1)
user_ratings = user_ratings.fillna(0)
#print(user_ratings)

item_similarity_df = user_ratings.corr(method="pearson")
#print(item_similarity_df.head(50))

def get_similar_products(product_name,user_rating):
	similar_score = item_similarity_df[product_name]*(user_rating-2.5)
	similar_score = similar_score.sort_values(ascending=False)
	return similar_score

product_recom = [("Fire TV Stick Streaming Media Player Pair Kit",5),("Certified Refurbished Amazon Echo",5)]
similar_products = pd.DataFrame()
for products,ratings in product_recom:
    similar_products = similar_products.append(get_similar_products(products,ratings),ignore_index = True)

print("Recommended products according to user input are as follows:")
print(similar_products.sum().sort_values(ascending=False).head(20))
