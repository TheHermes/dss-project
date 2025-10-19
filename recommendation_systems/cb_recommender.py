#
#   Content base recommender AI has been used as a support in creation of this and assignments as help
#
import ast 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    """
    A content-based recommender system for games based on tags.
    """
    def __init__(self, game_data_path):
        """
        Initializes the recommender by loading the game data.
        
        Args:
            game_data_path (str): The file path to the games.csv file.
        """
        self.games_df = pd.read_csv(game_data_path)
        self.tfidf_matrix = None
        self.game_indices = None
    
    def _preprocess_tags(self, tag_str):
        """
        Convert tag strings like "['Strategy', 'Simulation']" into a clean space-joined string.
        """

        if pd.isna(tag_str):
            return ""
        try:
            tags = ast.literal_eval(tag_str)
            if isinstance(tags, list):
                return " ".join(tag.strip().replace(" ", "_") for tag in tags)
        except Exception:
            pass
        return str(tag_str).replace(",", " ").replace(" ", "_")
    
    def fit(self):
        """
        Preprocesses the data and computes the TF-IDF matrix for game tags.
        Must be called before `recommend`.
        """
        if "tags" not in self.games_df.columns or "title" not in self.games_df.columns:
            raise ValueError("The dataset must contain both 'tags' and 'title' columns.")

        # Drop rows with missing tags or titles
        self.games_df = self.games_df.dropna(subset=["tags", "title"])
    
        # Clean and preprocess tags
        self.games_df["tags_processed"] = self.games_df["tags"].apply(self._preprocess_tags)

        # Add title and tags together so we also may recommended titles of the same series, and if a game doesn't have tags it will recommend based on the name, usually then dlc and sequels prequels
        self.games_df['content'] = self.games_df["title"].apply(lambda x: x.replace(" ", "_")) + " " + self.games_df["tags_processed"]

        # Compute TF-IDF features
        tfidf = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = tfidf.fit_transform(self.games_df["content"])

        # Index by game title
        self.game_indices = pd.Series(self.games_df.index, index=self.games_df["title"]).drop_duplicates()

    def recommend(self, game_title, num_recommendations=5):
        """
        Recommends games similar to the given title.
        """
        if self.tfidf_matrix is None or self.game_indices is None:
            print("Model not fitted. Run `.fit()` first.")
            return []

        if game_title not in self.game_indices:
            print(f"Game '{game_title}' not found in the dataset.")
            return []

        # Get similarity scores
        game_idx = self.game_indices[game_title]
        cosine_scores = cosine_similarity(self.tfidf_matrix[game_idx], self.tfidf_matrix).flatten()

        # Sort scores and pick top N (skip the game itself)
        similar_indices = cosine_scores.argsort()[::-1][1:num_recommendations + 1]

        recommendations = []
        for idx in similar_indices:
            title = self.games_df.iloc[idx]['title']
            score = float(cosine_scores[idx])
            recommendations.append((title, score))

        return recommendations

if __name__ == "__main__":
    recommender = ContentBasedRecommender(game_data_path="data/games_merged.csv")
    recommender.fit()

    # You can choose any game in the dataset!

    #game_title_to_test = "Dying Light 2 Stay Human"
    #game_title_to_test = "The Evil Within"
    #game_title_to_test = "Hearts of Iron IV"
    game_title_to_test = "Assassin's Creed® Origins"
    recommendations = recommender.recommend(game_title_to_test, num_recommendations=5)
    
    if recommendations:
        print(f"\nRecommendations for '{game_title_to_test}':")
        for title, score in recommendations:
            print(f"- {title} (similarity: {score:.3f})")
        print("\n")