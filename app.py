from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "a1b65a57f271d1358ce8b019ae3c277f")

def recommend(movie):
    try:
        idx = movies[movies["title"] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[idx])),
            reverse=True,
            key=lambda x: x[1]
        )
        recommended = []
        for i in distances[1:6]:
            title = movies.iloc[i[0]].title
            poster = fetch_poster(movies.iloc[i[0]].movie_id)
            recommended.append({"title": title, "poster": poster})
        return recommended
    except:
        return []

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url).json()
        poster_path = response.get("poster_path", "")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    searched_movie = ""
    movie_list = sorted(movies["title"].tolist())

    if request.method == "POST":
        searched_movie = request.form.get("movie")
        recommendations = recommend(searched_movie)

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        searched_movie=searched_movie
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)