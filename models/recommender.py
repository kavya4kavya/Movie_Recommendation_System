import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset
movies_df = pd.read_csv('data/movies.csv')

# Combine genre and overview for content-based filtering
movies_df['combined_features'] = movies_df['Genre'].fillna('') + ' ' + movies_df['Overview'].fillna('')

# Vectorize the combined features
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(movies_df['combined_features'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def get_recommendations(movie_id, top_n=10):
    if movie_id not in movies_df['Movie_ID'].values:
        return []

    idx = movies_df[movies_df['Movie_ID'] == movie_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return movies_df.iloc[top_indices][['Movie_ID', 'Series_Title', 'Genre']].to_dict(orient='records')
