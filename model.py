import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep only useful columns
movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]

# Drop missing values
movies.dropna(inplace=True)

# Helper functions to extract data
def convert(text):
    return [i["name"] for i in ast.literal_eval(text)]

def convert_cast(text):
    return [i["name"] for i in ast.literal_eval(text)][:5]

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i["job"] == "Director":
            return [i["name"]]
    return []

def collapse(lst):
    return [i.replace(" ", "") for i in lst]

# Apply transformations
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)
movies["overview"] = movies["overview"].apply(lambda x: x.split())

movies["genres"] = movies["genres"].apply(collapse)
movies["keywords"] = movies["keywords"].apply(collapse)
movies["cast"] = movies["cast"].apply(collapse)
movies["crew"] = movies["crew"].apply(collapse)

# Create tags column
movies["tags"] = (
    movies["overview"] +
    movies["genres"] +
    movies["keywords"] +
    movies["cast"] +
    movies["crew"]
)

# Final dataframe
df = movies[["movie_id", "title", "tags"]].copy()
df["tags"] = df["tags"].apply(lambda x: " ".join(x).lower())

# Vectorize
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(df["tags"]).toarray()

# Cosine similarity
similarity = cosine_similarity(vectors)

# Save
pickle.dump(df, open("movies.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Total movies:", len(df))
print("Model saved!")