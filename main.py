# Boilerplate code

import pandas as pd
import numpy as np
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF

# NOTE: Detta är en fungerande lösning från tidigare uppgift.
# Använd gärna din egna kod

# HybridRecommender klassen behöver inte modifieras
class HybridRecommender:
    def __init__(self, movie_data_path, rating_data_path):
        self.movies_df = pd.read_csv(movie_data_path)
        self.ratings_df = pd.read_csv(rating_data_path)
        self.content_recommender = self._ContentBasedRecommender(self.movies_df)
        self.nmf_model = None; self.user_item_matrix = None; self.user_mapper = None
        self.movie_mapper = None; self.movie_inv_mapper = None

    def fit(self):
        self.content_recommender.fit()
        self.user_item_matrix = self.ratings_df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        self.user_mapper = {uid: i for i, uid in enumerate(self.user_item_matrix.index)}
        self.movie_mapper = {mid: i for i, mid in enumerate(self.user_item_matrix.columns)}
        self.nmf_model = NMF(n_components=20, init='random', random_state=42, max_iter=500)
        self.nmf_model.fit(self.user_item_matrix)

    def recommend(self, user_id, movie_title_seed, num_recommendations=10):
        content_recs = self.content_recommender.recommend(movie_title_seed, num_recommendations)
        collaborative_recs = [];
        if user_id in self.user_mapper:
            user_idx = self.user_mapper[user_id]
            user_vector = self.user_item_matrix.iloc[user_idx].values.reshape(1, -1)
            user_P = self.nmf_model.transform(user_vector)
            item_Q = self.nmf_model.components_
            predicted_scores = np.dot(user_P, item_Q).flatten()
            scores_series = pd.Series(predicted_scores, index=self.user_item_matrix.columns)
            rated_movies = self.ratings_df[self.ratings_df['userId'] == user_id]['movieId']
            scores_series = scores_series.drop(index=rated_movies, errors='ignore')
            top_movie_ids = scores_series.nlargest(num_recommendations).index.tolist()
            collaborative_recs = self.movies_df[self.movies_df['movieId'].isin(top_movie_ids)]['title'].tolist()
        combined_recs = collaborative_recs + content_recs
        unique_recs = list(dict.fromkeys(combined_recs).keys())
        return unique_recs[:num_recommendations]

    class _ContentBasedRecommender:
        def __init__(self, movies_df): self.movies_df = movies_df
        def fit(self):
            self.movies_df['genres'] = self.movies_df['genres'].fillna('')
            tfidf = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = tfidf.fit_transform(self.movies_df['genres'])
            self.movie_indices = pd.Series(self.movies_df.index, index=self.movies_df['title']).drop_duplicates()
        def recommend(self, title, n=10):
            if title not in self.movie_indices: return []
            idx = self.movie_indices[title]
            sim_scores = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
            sim_indices = sim_scores.argsort()[-n-1:-1][::-1]
            return self.movies_df['title'].iloc[sim_indices].tolist()

class Evaluator:
    def __init__(self, movie_data_path, rating_data_path):
        """Initializes the evaluator and the recommender it will evaluate."""
        self.recommender = HybridRecommender(movie_data_path, rating_data_path)
        self.movies_df = self.recommender.movies_df
        self.ratings_df = self.recommender.ratings_df
        self.popularity_scores = None
        self.title_to_id = None

    def fit_recommender(self):
        """Fits the recommender and pre-calculates necessary data for evaluation."""
        print("Fitting the recommender model...")
        self.recommender.fit()
        print("Recommender fitted.")
        
        print("Pre-calculating popularity scores...")
        # Calculate popularity as the fraction of users who have rated each movie.
        rating_counts = self.ratings_df['movieId'].value_counts()
        num_users = self.ratings_df['userId'].nunique()
        self.popularity_scores = rating_counts / num_users
        # Ensure we only get a single movieId
        movies_unique_titles = self.movies_df.drop_duplicates(subset='title')
        self.title_to_id = pd.Series(movies_unique_titles.movieId.values, index=movies_unique_titles.title)

        print("Popularity scores calculated.")

    def generate_all_recommendations(self):
        """Generates recommendations for all users to create a dataset for evaluation."""
        print("Generating recommendations for all users... (This may take a moment)")
        all_recommendations = {}
        # - life is like a box of chocolates...
        movie_seed = "Forrest Gump (1994)" # Ta en populär film
        
        for user_id in self.ratings_df['userId'].unique():
            recs = self.recommender.recommend(user_id, movie_seed, 10)
            all_recommendations[user_id] = recs
        print("All recommendations generated.")
        return all_recommendations

    def calculate_precision_at_k(self, all_recommendations, k=10):
        """
        Calculates the average Precision@k for all users.
        """
        # TODO:
        
        precision_scores = []

        for user_id, recommendations in all_recommendations.items():
            user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
            liked_movies = set(user_ratings[user_ratings['rating'] >= 4.0]['movieId'])

            if not liked_movies:
                continue

            rec_movie_ids = [self.title_to_id.get(title) for title in recommendations if title in self.title_to_id]

            hits = 0

            for movie_id in rec_movie_ids:
                if movie_id in liked_movies:
                    hits +=1

            # Fancy one liner
            #hits = sum(1 for movie_id in rec_movie_ids[:k] if movie_id in liked_movies)

            precision = hits / k
            precision_scores.append(precision)
        
        avg_precision = sum(precision_scores) / len(precision_scores)
        return avg_precision

    def calculate_coverage(self, all_recommendations):
        """
        Calculates the catalog coverage of the recommendations.
        """
        # TODO:

        # AI hjälpte för att hitta lösning till att testerna inte gick igenom, jag satt en god stund och hittade inte på vad man kunde göra

        recommended_movies = set()

        for user_id, recommendations in all_recommendations.items():

            if self.title_to_id is not None:
                movie_ids = [self.title_to_id.get(title) for title in recommendations if self.title_to_id.get(title) is not None]
            else:
                movie_ids = recommendations

            recommended_movies.update(movie_ids)
                                                                # Den här if satsen existerar för att testerna inte ska misslyckas, den söker efter movieId som inte finns i testerna?!?
        total_movies = len(self.movies_df['movieId'].unique()) if 'movieId' in self.movies_df.columns else len(self.movies_df)

        coverage = len(recommended_movies) / total_movies 
        return coverage

    def calculate_novelty(self, all_recommendations):
        """
        Calculates the average novelty of the recommendations.
        """
        user_novelties = []

        for user_id, recommendations in all_recommendations.items():
            
            rec_movie_ids = [self.title_to_id.get(title) for title in recommendations if title in self.title_to_id]

            novelty_scores = []
            for movie_id in rec_movie_ids:
                popularity = self.popularity_scores.get(movie_id)
                novelty = -math.log2(popularity)
                novelty_scores.append(novelty)

            # Hoppa över om det inte finns scores
            if len(novelty_scores) == 0:
                continue
            
            avg_novelty_user = sum(novelty_scores) / len(novelty_scores)

            user_novelties.append(avg_novelty_user)

        avg_novelty = sum(user_novelties) / len(user_novelties)        
        return avg_novelty

if __name__ == '__main__':
    evaluator = Evaluator(
        movie_data_path='data/movies.csv',
        rating_data_path='data/ratings.csv'
    )
    evaluator.fit_recommender()
    all_recs = evaluator.generate_all_recommendations()
    
    precision = evaluator.calculate_precision_at_k(all_recs)
    coverage = evaluator.calculate_coverage(all_recs)
    novelty = evaluator.calculate_novelty(all_recs)
    
    print("\n--- Evaluation Metrics ---")
    print(f"Average Precision@10: {precision:.4f}")
    print(f"Catalog Coverage: {coverage:.4f}")
    print(f"Average Novelty: {novelty:.4f}")