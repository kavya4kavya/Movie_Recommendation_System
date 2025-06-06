from flask import Flask, jsonify, request
import pandas as pd
import random

# Load the preprocessed dataset
movies_df = pd.read_csv('data/movies.csv')

# Initialize Flask app
app = Flask(__name__)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to get a random movie card
@app.route('/get_movie', methods=['GET'])
def get_movie():
    random_movie = movies_df.sample().to_dict(orient='records')[0]
    return jsonify(random_movie)

# Endpoint to receive user swipe feedback
@app.route('/swipe', methods=['POST'])
def swipe():
    data = request.json
    movie_id = data.get('Movie_ID')
    swipe_direction = data.get('swipe_direction')  # 'like', 'dislike', 'maybe'
    
    # Log or store feedback (for now, just print it)
    print(f"Movie ID: {movie_id}, Swipe Direction: {swipe_direction}")
    
    return jsonify({"message": "Feedback received"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
