import pickle
import streamlit as st
import requests
import os


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


file_path1 = 'C:/Users/SIDDHARTH/Downloads/movie_list.pkl'  # Substitute this with your actual file path

if os.path.exists(file_path1):
    with open(file_path1, 'rb') as file:
        movies = pickle.load(file)
else:
    st.error(f"File '{file_path1}' not found.")
    st.stop()

file_path2 = 'C:/Users/SIDDHARTH/Downloads/similarity.pkl'  # Substitute this with your actual file path

if os.path.exists(file_path2):
    with open(file_path2, 'rb') as file:
        similarity = pickle.load(file)
else:
    st.error(f"File '{file_path2}' not found.")
    st.stop()

st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names and recommended_movie_posters:
        col1, col2, col3, col4, col5 = st.beta_columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
    else:
        st.warning("No recommendations found for this movie.")
