import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load and preprocess the data
def load_data():
    # Load the dataset (assuming it's available via loadFileData in the environment)
    data = loadFileData("C:/Users/kavya/Downloads/imdb_top_1000.csv")
    df = pd.read_csv(data)
    
    # Handle missing values
    df['Genre'] = df['Genre'].fillna('')
    df['IMDB_Rating'] = df['IMDB_Rating'].fillna(df['IMDB_Rating'].mean())
    
    return df

# Step 2: Feature engineering
def preprocess_data(df):
    # Split genres into a list
    df['Genre'] = df['Genre'].apply(lambda x: x.split(', '))
    
    # Create a list of all unique genres
    all_genres = set()
    for genres in df['Genre']:
        all_genres.update(genres)
    all_genres = sorted(list(all_genres))
    
    # One-hot encode genres
    genre_matrix = np.zeros((len(df), len(all_genres)))
    for i, genres in enumerate(df['Genre']):
        for genre in genres:
            if genre in all_genres:
                genre_matrix[i, all_genres.index(genre)] = 1
    
    # Normalize IMDb ratings (scale to 0-1)
    df['Normalized_Rating'] = (df['IMDB_Rating'] - df['IMDB_Rating'].min()) / (df['IMDB_Rating'].max() - df['IMDB_Rating'].min())
    
    return genre_matrix, all_genres, df

# Step 3: Compute similarity
def compute_similarity(genre_matrix):
    # Calculate cosine similarity between movies
    similarity_matrix = cosine_similarity(genre_matrix)
    return similarity_matrix

# Step 4: Recommendation function
def recommend_movies(movie_title, df, similarity_matrix, top_n=5):
    # Find the index of the input movie
    try:
        movie_idx = df.index[df['Series_Title'] == movie_title].tolist()[0]
    except IndexError:
        return f"Movie '{movie_title}' not found in the dataset."
    
    # Get similarity scores for the input movie
    sim_scores = similarity_matrix[movie_idx]
    
    # Combine similarity with normalized IMDb rating (weighted sum)
    combined_scores = sim_scores * 0.7 + df['Normalized_Rating'].values * 0.3
    
    # Get indices of top similar movies
    sim_indices = np.argsort(combined_scores)[::-1][1:top_n+1]
    
    # Return recommended movies
    recommendations = df.iloc[sim_indices][['Series_Title', 'IMDB_Rating', 'Genre']]
    return recommendations

# Main function to run the recommendation system
def main():
    # Load data
    df = load_data()
    
    # Preprocess data
    genre_matrix, all_genres, df = preprocess_data(df)
    
    # Compute similarity
    similarity_matrix = compute_similarity(genre_matrix)
    
    # Example: Recommend movies similar to "The Shawshank Redemption"
    movie_title = "The Shawshank Redemption"
    recommendations = recommend_movies(movie_title, df, similarity_matrix, top_n=5)
    
    print(f"\nRecommendations for '{movie_title}':")
    print(recommendations)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
