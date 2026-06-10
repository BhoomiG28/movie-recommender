# 🎬 CineMatch — Movie Recommendation System

A Netflix-style movie recommendation web app that suggests 
similar movies based on your selection.

## 🔴 Live Demo
👉 [Try the app here](https://movie-recommender-1-tal7.onrender.com)

## 📌 About The Project
CineMatch uses Content Based Filtering and Cosine Similarity 
to recommend 5 similar movies from a database of 4800+ movies.
Real movie posters are fetched using the TMDB API.

## 🛠️ Tech Stack
- **Python** — Core programming language
- **Scikit-learn** — Cosine similarity calculation
- **Pandas & Numpy** — Data processing
- **Flask** — Web framework
- **TMDB API** — Real movie posters
- **HTML/CSS** — Netflix-style frontend
- **Render** — Deployment

## 🤖 How It Works
1. Movie tags are created from genres, keywords, cast and director
2. CountVectorizer converts tags into vectors
3. Cosine Similarity finds most similar movies
4. TMDB API fetches real posters for recommendations

## 🚀 How To Run Locally
1. Clone the repository
