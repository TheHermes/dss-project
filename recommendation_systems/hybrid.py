#
#   Hybrid recommender (content based + collaborative) then Weighted Hybrid (Score Blending)
#
from collaborative import CollaborativeRecommender
from cb_recommender import ContentBasedRecommender
import pandas as pd

class HybridRecommender:
    """
    A hybrid recommender system that combines content-based and collaborative filtering.
    """
    def __init__(self, game_data_path, user_game_data_path, recommendations_path, alpha=0.5):
        """
        Initializes the hybrid recommender by loading the game data and user-game interaction data.
        
        alpha = 0 means only collaborative filtering, alpha = 1 means only content-based filtering.
        """
        self.content_recommender = ContentBasedRecommender(game_data_path)
        self.collaborative_recommender = CollaborativeRecommender(game_data_path, recommendations_path) # path needed
        self.alpha = alpha
        self.games_df = pd.read_csv(game_data_path)
    
    def fit(self):
        """
        Fits both the content-based and collaborative recommenders.
        Must be called before `recommend`.
        """
        self.content_recommender.fit()
        self.collaborative_recommender.fit()

    def normalize_scores(self, scores_dict):
        """
        Normalizes the scores in a dictionary to a range of 0 to 1.
        
        Args:
            scores_dict (dict): A dictionary with items as keys and scores as values.

        Returns:
            dict: A dictionary with normalized scores.
        """
        if not scores_dict:
            return scores_dict
        max_score = max(scores_dict.values())
        if max_score == 0:
            return {k: 0 for k in scores_dict}
        return {k: v / max_score for k, v in scores_dict.items()}
    
    def print_recommendations(self, recommendations):
        """
        Prints the recommended game titles from a list of (title, score) tuples.
        
        """
        print(f"\nTop {len(recommendations)} recommendations for user {user_id}:\n")

        for i, rec in enumerate(recommendations, start=1):
            title, score = rec
            print(f"{i:>2}. {title:<40} Score: {score:.3f}")
        print("\n")
    
    
    def recommend(self, user_id, top_n):
        """
        Recommends games for a given user by combining scores from both recommenders.
        
        Args:
            user_id (int): The ID of the user for whom to make recommendations.
            top_n (int): The number of top recommendations to return.

        Returns:
            List of recommended game titles.    
        """
        # Get collaborative filtering recommendations
        collab_recs = self.collaborative_recommender.recommend(user_id, num_recommendations=top_n)
        #collab_titles = [title for title, score in collab_recs] # probably needs to be changed to set for weighted
        collab_scores = {title: score for title, score in collab_recs}

        # Get content-based recommendations for each game the user has interacted with
        user_games = self.collaborative_recommender.recs_df[self.collaborative_recommender.recs_df['user_id'] == user_id]['app_id'].unique()
        # Get titles for those app_ids 
        user_games_titles = self.collaborative_recommender.games_df[self.collaborative_recommender.games_df['app_id'].isin(user_games)]['title'].unique()
        '''content_titles = []
        for game in user_games_titles:
            try:
                content_recs = self.content_recommender.recommend(game, num_recommendations=top_n)
                for title, score in content_recs:
                    if title not in user_games and title not in content_titles:  # Avoid recommending games the user already has
                        content_titles.append(title)
            except ValueError:
                continue  # Skip games not found in the content-based recommender'''
        content_scores = {}
        # Get content based recommendations based on every game the user has played
        for game in user_games_titles:
            try: 
                content_recs = self.content_recommender.recommend(game, num_recommendations=top_n)
                for title, score in content_recs:
                    if title not in user_games_titles:  
                        content_scores[title] = content_scores.get(title, 0) + score
            except (ValueError, IndexError): 
                continue

        # Normalize scores
        collab_scores = self.normalize_scores(collab_scores)
        content_scores = self.normalize_scores(content_scores)

        # Combine scores using weighted sum
        combined_scores = {}
        for title in set(collab_scores.keys()).union(content_scores.keys()):
            cf = collab_scores.get(title, 0)
            cb = content_scores.get(title, 0)
            combined = self.alpha * cf + (1 - self.alpha) * cb
            combined_scores[title] = combined

        # Sort by combined score and return top N recommendations
        ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return ranked
                
        #all_titles = list(dict.fromkeys(content_titles + collab_titles)) # Preserve order and remove duplicates
        # Sort by combined score and return top N recommendations
        #recommended_titles = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        #return recommended_titles
        #return all_titles[:top_n]
    
if __name__ == "__main__":
    hybrid_recommender = HybridRecommender(game_data_path="data/games_merged.csv", user_game_data_path="data/users_1000.csv", recommendations_path="data/recommendations_1000.csv", alpha=0.8)
    hybrid_recommender.fit()
    #game_seed = 
    user_id = 11895026  # Example user ID
    #user_id = 657825
    recommendations = hybrid_recommender.recommend(user_id, top_n=10)
    hybrid_recommender.print_recommendations(recommendations)