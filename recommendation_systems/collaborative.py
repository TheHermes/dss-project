#
#   Collaborative Recommender for Games (NMF-based)
#

import pandas as pd
import numpy as np
from sklearn.decomposition import NMF


class CollaborativeRecommender:
    """
    Collaborative filtering recommender using Non-negative Matrix Factorization (NMF).
    """

    def __init__(self, games_path, recommendations_path):
        """
        Initialize recommender with paths to game metadata and user–game interactions.

        Args:
            games_path (str): Path to games_merged.csv
            recommendations_path (str): Path to recommendations_1000.csv
        """
        self.games_df = pd.read_csv(games_path)
        self.recs_df = pd.read_csv(recommendations_path)

        self.user_item_matrix = None
        self.nmf_model = None
        self.user_mapper = None
        self.game_mapper = None

    def _prepare_data(self):
        """
        Prepare and clean the interaction data for NMF.
        Converts 'is_recommended' and 'hours' into a numerical rating.
        """
        df = self.recs_df.copy()

        # Convert recommendation boolean to numeric
        df["is_recommended"] = df["is_recommended"].astype(int)

        # Handle missing hours and normalize it
        df["hours"] = df["hours"].fillna(0)

        # Normalize hours to a 0–1 range for fairness
        df["hours_normalized"] = df["hours"] / (df["hours"].max() + 1e-6)

        # Weighted rating: more hours + positive rec = stronger signal
        df["rating"] = (0.7 * df["is_recommended"]) + (0.3 * df["hours_normalized"])

        return df

    def fit(self):
        """
        Build user–game matrix and train the NMF model.
        """
        print("Preparing data...")
        df = self._prepare_data()

        print("Building user–game matrix...")
        self.user_item_matrix = df.pivot_table(
            index="user_id",
            columns="app_id",
            values="rating",
            fill_value=0
        )

        #print(f"Matrix shape: {self.user_item_matrix.shape} (users × games)")

        self.user_mapper = {user_id: i for i, user_id in enumerate(self.user_item_matrix.index)}
        self.game_mapper = {app_id: i for i, app_id in enumerate(self.user_item_matrix.columns)}

        print("Training NMF model...")
        model = NMF(
            n_components=20,
            init="random",
            random_state=42,
            max_iter=400
        )
        model.fit_transform(self.user_item_matrix.values)
        self.nmf_model = model

        print("NMF model fitted successfully.")

    def recommend(self, user_id, num_recommendations=5):
        """
        Recommend top-N games for a specific user.
        """
        if self.nmf_model is None:
            print("Model not trained yet. Run `.fit()` first.")
            return []

        if user_id not in self.user_mapper:
            print(f"User ID {user_id} not found in data.")
            return []

        # Get user latent vector and reconstruct predicted scores
        user_idx = self.user_mapper[user_id]
        user_vector = self.user_item_matrix.iloc[user_idx].values
        user_P = self.nmf_model.transform(user_vector.reshape(1, -1))
        user_Q = self.nmf_model.components_
        predicted_scores = np.dot(user_P, user_Q).flatten()

        scores = pd.Series(predicted_scores, index=self.user_item_matrix.columns)

        # Remove games the user already interacted with
        rated_games = self.user_item_matrix.iloc[user_idx]
        scores = scores[rated_games == 0]

        # Get top games
        top_app_ids = scores.nlargest(num_recommendations).index
        rec_titles = self.games_df[self.games_df["app_id"].isin(top_app_ids)]["title"].tolist()

        return rec_titles

    def print_recommendations(self, user_id, n=5):
        recs = self.recommend(user_id, n)
        if recs:
            print(f"\nTop {n} Recommendations for user {user_id}:\n")
            for i, title in enumerate(recs, start=1):
                print(f"{i}. {title}")
        else:
            print(f"No recommendations found for user {user_id}.")


if __name__ == "__main__":
    # Data with 1 000 users and ca 50 000 recommendations
    """recommender = CollaborativeRecommender(
        games_path="data/games_merged.csv",
        recommendations_path="data/recommendations_1000.csv"
    )"""

    # Data with 10 000 users and ca 500 000 recommendations
    recommender = CollaborativeRecommender(
        games_path="data/games_merged.csv",
        recommendations_path="data/recommendations_10000.csv"
    )

    recommender.fit()

    # Test user (replace with an existing user_id)
    #test_user_id = 6956683 # user for 1000 user data
    test_user_id = 8075017 # user for 10000 user data
    recommender.print_recommendations(test_user_id, n=10)
