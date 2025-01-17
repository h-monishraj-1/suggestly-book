from flask import Flask, request, jsonify, render_template
from book_recommendation import BookRecommender
import pandas as pd

app = Flask(__name__)

# Initialize book recommender
book_recommender = BookRecommender("book_list.pkl", "similarity.pkl")

books_df = pd.read_pickle("book_list.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend_books", methods=["POST"])
def recommend_books():
    data = request.json
    book_title = data.get("book_title", "")
    recommendations = book_recommender.recommend(book_title)
    return jsonify({"recommendations": recommendations})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"titles": []})
    
    matching_titles = books_df[books_df['title'].str.lower().str.contains(query, na=False)]['title'].head(10).tolist()
    return jsonify({"titles": matching_titles})

if __name__ == "__main__":
    app.run(debug=True)