import chromadb 
import time
import Levenshtein 

class VersioningAgent:
    """
    Manages storing and retrieving chapter versions in ChromaDB.
    Implements a simple reward model for a conceptual RL system.
    """
    def __init__(self, path="outputs/db", collection_name="book_chapters"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"VersioningAgent: Connected to ChromaDB. Collection '{collection_name}' is ready.")

    def _calculate_reward(self, text_before_hitl: str, text_after_hitl: str) -> float:
        """
        Calculates a reward based on the similarity between the AI's final output
        and the human's finalized version. Fewer edits = higher reward.
        This simulates a Reinforcement Learning reward signal.
        """
        # Levenshtein distance measures the number of edits (insertions, deletions,
        # substitutions) needed to change one string into the other.
        distance = Levenshtein.distance(text_before_hitl, text_after_hitl)
        
        # Normalize the reward. A smaller distance is better.
        # We use a simple inverse relationship. Add 1 to avoid division by zero.
        # The reward is higher when the distance is smaller.
        reward = 1.0 / (1.0 + float(distance))
        
        print(f"VersioningAgent (RL): Edit distance = {distance}. Calculated reward = {reward:.4f}")
        return reward

    def save_final_version(self, chapter_name: str, final_text: str, text_before_hitl: str):
        """
        Saves the finalized version of a chapter to the database.

        Args:
            chapter_name: The name of the chapter.
            final_text: The text content after all processing and human review.
            text_before_hitl: The text just before the human review step.
        """
        # Determine the next version number
        existing_versions = self.collection.get(where={"chapter_name": chapter_name})
        next_version = len(existing_versions['ids']) + 1
        
        doc_id = f"{chapter_name}_v{next_version}"
        timestamp = time.time()
        
        reward = self._calculate_reward(text_before_hitl, final_text)

        print(f"VersioningAgent: Saving document to ChromaDB with ID: {doc_id}")
        self.collection.add(
            documents=[final_text],
            metadatas=[{
                "chapter_name": chapter_name,
                "version": next_version,
                "timestamp": timestamp,
                "status": "finalized",
                "rl_reward": reward
            }],
            ids=[doc_id]
        )
        print("VersioningAgent: Save complete.")

    def search_versions(self, query: str, chapter_name: str, n_results: int = 1) -> list:
        """
        Performs a semantic search for a query within a specific chapter's versions.

        Args:
            query: The text to search for.
            chapter_name: The chapter to search within.
            n_results: The number of results to return.

        Returns:
            A list of search results.
        """
        print(f"VersioningAgent: Searching for '{query}' in chapter '{chapter_name}'...")
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"chapter_name": chapter_name}
        )
        return results

    def get_highest_reward_version(self, chapter_name: str):
        """
        RL-based Search: Retrieves the version of a chapter with the highest reward.
        This simulates an RL agent choosing the "best" path.
        """
        print(f"VersioningAgent (RL Search): Finding highest reward version for '{chapter_name}'")
        versions = self.collection.get(where={"chapter_name": chapter_name}, include=["metadatas"])
        
        if not versions['ids']:
            print("No versions found for this chapter.")
            return None

        highest_reward = -1
        best_version_id = None
        for i, meta in enumerate(versions['metadatas']):
            if meta.get('rl_reward', 0) > highest_reward:
                highest_reward = meta['rl_reward']
                best_version_id = versions['ids'][i]

        if best_version_id:
            print(f"Highest reward found: {highest_reward:.4f} for version ID: {best_version_id}")
            return self.collection.get(ids=[best_version_id], include=["documents", "metadatas"])
        
        return None