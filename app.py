from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "a1b65a57f271d1358ce8b019ae3c277f")

def fetch_poster_and_rating(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10).json()
        poster_path = response.get("poster_path", "")
        rating = round(response.get("vote_average", 0), 1)
        genres = [g["name"] for g in response.get("genres", [])]
        poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/500x750/1a1a1a/ffffff?text=No+Poster"
        return poster, rating, genres
    except:
        return "https://placehold.co/500x750/1a1a1a/ffffff?text=No+Poster", 0, []

def fetch_trending():
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10).json()
        trending = []
        for movie in response.get("results", [])[:8]:
            poster_path = movie.get("poster_path", "")
            poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/500x750/1a1a1a/ffffff?text=No+Poster"
            trending.append({
                "title": movie.get("title", ""),
                "poster": poster,
                "rating": round(movie.get("vote_average", 0), 1)
            })
        return trending
    except:
        return []

def recommend(movie, genre_filter=None):
    try:
        idx = movies[movies["title"] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[idx])),
            reverse=True,
            key=lambda x: x[1]
        )
        recommended = []
        for i in distances[1:20]:
            title = movies.iloc[i[0]].title
            movie_id = movies.iloc[i[0]].movie_id
            poster, rating, genres = fetch_poster_and_rating(movie_id)

            if genre_filter and genre_filter != "All":
                if genre_filter not in genres:
                    continue

            recommended.append({
                "title": title,
                "poster": poster,
                "rating": rating,
                "genres": genres
            })

            if len(recommended) == 5:
                break

        return recommended
    except:
        return []

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    searched_movie = ""
    selected_genre = "All"
    movie_list = sorted(movies["title"].tolist())
    trending = fetch_trending()

    if request.method == "POST":
        searched_movie = request.form.get("movie", "")
        selected_genre = request.form.get("genre", "All")
        if searched_movie:
            recommendations = recommend(searched_movie, selected_genre)

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        searched_movie=searched_movie,
        trending=trending,
        selected_genre=selected_genre
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)