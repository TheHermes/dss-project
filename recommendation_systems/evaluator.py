#
#   Evaluate the system
#
from hybrid import HybridRecommender
import pandas as pd
import numpy as np

class RecommenderEvaluator:
    def __init__(self, game_data_path, user_game_data_path, rec_data_path, alpha=0.8):
        """
        Args:
            recommender: The recommender system (e.g., HybridRecommender)
            recs_df: The dataset with user–item interactions
            all_items: Set of all unique item IDs in the catalog
        """
        self.recommender = HybridRecommender(
            game_data_path=game_data_path,
            user_game_data_path=user_game_data_path,
            recommendations_path=rec_data_path,
            alpha=alpha
        )
        self.games_df = self.recommender.games_df
        self.recs_df = self.recommender.recs_df
        #self.popularity_scores = None
        #self.title_to_appid = pd.Series(self.games_df['app_id'].values, index=self.games_df['title'].str.lower()).to_dict()
        #self.popularity = self.recs_df['app_id'].value_counts(normalize=True).to_dict()
    def precision_at_k(self, all_recs, k=10):
        '''
        This version gave score 1
        precision_scores = []
        for user_id, recommendations in all_recommendations.items():
            if not recommendations:
                continue
            hits = sum(1 for item in recommendations if item not in self.recs_df.get(user_id, set()))
            precision = hits / k
            precision_scores.append(precision)
        return precision_scores
        #mean_precision = np.mean(precision_scores)
        #return mean_precision   
        rec_items = {self.title_to_appid.get(r) for r in rec_titles if self.title_to_appid.get(r) is not None}
            true_items = set(self.recs_df[(self.recs_df['user_id'] == user_id) &(self.recs_df['is_recommended'] == True)]['app_id']) 
            if not rec_items:
                continue
        '''
         # Ground truth (items the user actually interacted with)        
        #true_items = set(self.recs_df[(self.recs_df['user_id'] == user_id) &(self.recs_df['is_recommended'] == True)]['app_id']) 
        #Alternative with app_id^^^^
        precision_scores = []
        for user_id, rec_titles in all_recs.items():
        
            user_data = self.recs_df[self.recs_df["user_id"] == user_id]
            liked_titles = set(self.games_df[self.games_df["app_id"].isin(user_data[user_data["is_recommended"] == True]["app_id"])]["title"].dropna().tolist())
                # Map titles to app_id
            if not liked_titles:
                precision_scores.append(0.0)
                    #continue
                
            rec_set = set(rec_titles[:k])
            hits = len(rec_set & liked_titles)
            precision_scores.append(hits / k)
            
        return np.mean(precision_scores)
    
    def calculate_coverage(self, all_recommendations):
        recommended_games = set()
        for recs in all_recommendations.values(): # loop over users instead?
            if recs and isinstance(recs[0], tuple):
                 recs = [r[0] for r in recs]
            recommended_games.update(recs)

        total_games = self.games_df['title'].nunique() # or should recs_df appid be used?
        coverage = len(recommended_games) / total_games if total_games > 0 else 0
        return coverage
    
    def calculate_novelty(self, all_recommendations):
        novelty = []

        popularity_counts = self.recs_df['app_id'].value_counts(normalize=True)
        for recs in all_recommendations.values():
            for title in recs:
               
            # Map title to app_id
                app_row = self.games_df[self.games_df['title'] == title]
                if not app_row.empty:
                    app_id = app_row.iloc[0]['app_id']
            pop = popularity_counts.get(app_id, 0)
            if pop > 0:
                novelty.append(-np.log2(pop))

        mean_novelty = np.mean(novelty) if novelty else 0
        return mean_novelty

    def fit_recommender(self):
        """Fits the hybrid recommender and precomputes data for evaluation."""
        print("Fitting hybrid recommender...")
        self.recommender.fit()
        print("Recommender fitted.")
        '''
        # Popularity: fraction of users who interacted with each game
        game_counts = self.recs_df['app_id'].value_counts()
        num_users = self.recs_df['user_id'].nunique()
        self.popularity_scores = game_counts / num_users

        # Map titles to app_id
        games_unique = self.games_df.drop_duplicates(subset='title')
        self.title_to_id = pd.Series(games_unique.app_id.values, index=games_unique.title)
        print("Precomputed popularity scores and title-to-appid mapping.")
        '''

    def generate_all_recommendations(self, user_ids, top_n=10):
        all_recommendations = {}
        
        for user_id in user_ids:
            recs = self.recommender.recommend(user_id, top_n=top_n)
            rec_titles = [r[0] if isinstance(r, tuple) else r for r in recs]
            all_recommendations[user_id] = rec_titles
        
        return all_recommendations
   
if __name__ == "__main__":
    # Load data
    recs_df = pd.read_csv("data/recommendations_1000.csv")
    all_items = set(recs_df['app_id'].unique())
    '''
    # Initialize recommender
    hybrid_recommender = HybridRecommender(
        game_data_path="data/games_merged.csv",
        user_game_data_path="data/users_1000.csv",
        recommendations_path="data/recommendations_1000.csv",
        alpha=0.8 # alpha influences results of evaluation
    )
    '''
   # hybrid_recommender.fit()

    #evaluator = RecommenderEvaluator(hybrid_recommender, recs_df, all_items)
    evaluator = RecommenderEvaluator(
        game_data_path="data/games_merged.csv",
        user_game_data_path="data/users_1000.csv",
        rec_data_path="data/recommendations_1000.csv",
        alpha=0.8
    )

    evaluator.fit_recommender()

    # Example user IDs to evaluate
    user_ids = recs_df['user_id'].unique()[:1000]  
    #user_ids = [11895026]
    #user_ids = [9843409]

    all_recommendations = evaluator.generate_all_recommendations(user_ids, top_n=5) 

    precision = evaluator.precision_at_k(all_recommendations, k=10)
    coverage = evaluator.calculate_coverage(all_recommendations)
    novelty = evaluator.calculate_novelty(all_recommendations)
# Do concurrent.futures?
    
    print(f"Mean Precision@10: {precision:.4f}")
    print(f"Coverage: {coverage:.4f}")
    print(f"Novelty: {novelty:.4f}")