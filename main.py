import asyncio
from agents.scraping_agent import ScrapingAgent
from agents.ai_agents import AIWriterAgent, AIReviewerAgent
from agents.hitl_agent import HumanInTheLoopAgent
from agents.versioning_agent import VersioningAgent

class WorkflowOrchestrator:
    def __init__(self):
        print("Initializing workflow orchestrator and agents...")
        self.scraping_agent = ScrapingAgent()
        self.ai_writer_agent = AIWriterAgent()
        self.ai_reviewer_agent = AIReviewerAgent()
        self.hitl_agent = HumanInTheLoopAgent()
        self.versioning_agent = VersioningAgent()
        print("All agents initialized.")

    async def run_full_workflow(self, url: str, chapter_name: str):
        """
        Executes the complete book publication workflow for a single chapter.
        """
        print("\n" + "#"*60)
        print(f"Starting New Workflow for: {chapter_name}")
        print("#"*60 + "\n")

        # 1. Scraping & Screenshots
        print("--- Step 1: Scraping ---")
        original_text, screenshot_path = await self.scraping_agent.scrape(url, chapter_name)
        if not original_text:
            print("Workflow failed at scraping stage. Aborting.")
            return
        print(f"Scraping complete. Screenshot at: {screenshot_path}\n")

        # 2. AI Writing
        print("--- Step 2: AI Writing ---")
        writer_prompt = f"Rewrite the chapter '{chapter_name}' in a more dramatic and modern narrative style."
        spun_text = self.ai_writer_agent.spin_chapter(original_text, writer_prompt)
        print("AI Writing complete.\n")

        # 3. AI Review
        print("--- Step 3: AI Reviewing ---")
        reviewer_prompt = "Refine the text, ensuring it is grammatically correct, coherent, and engaging. Fix any awkward phrasing."
        reviewed_text = self.ai_reviewer_agent.review_chapter(spun_text, reviewer_prompt)
        print("AI Reviewing complete.\n")

        # 4. Human-in-the-Loop
        print("--- Step 4: Human-in-the-Loop (HITL) ---")
        final_text = self.hitl_agent.review_and_edit(original_text, reviewed_text, chapter_name)
        print("HITL stage complete.\n")

        # 5. Versioning and Storage (with RL Reward Calculation)
        print("--- Step 5: Versioning and Storage ---")
        # The 'text_before_hitl' is the AI's best attempt (the reviewed_text)
        self.versioning_agent.save_final_version(chapter_name, final_text, reviewed_text)
        print("Versioning complete.\n")

        # 6. Semantic Search and RL-based Search Demonstration
        print("--- Step 6: Search Demonstration ---")
        # A) Semantic search for a specific phrase
        search_query = "the gates of morning" # A phrase from the text
        search_results = self.versioning_agent.search_versions(query=search_query, chapter_name=chapter_name)
        print(f"Semantic search results for '{search_query}':")
        print(search_results)
        
        # B) RL-based search for the "best" version
        print("\nPerforming RL-based search to find the highest-reward version...")
        best_version = self.versioning_agent.get_highest_reward_version(chapter_name)
        print("Result of RL-based search:")
        if best_version:
            print(f"Found best version: ID {best_version['ids'][0]}")
            print(f"Reward: {best_version['metadatas'][0]['rl_reward']:.4f}")
            # print(f"Content: {best_version['documents'][0][:200]}...")
        else:
            print("Could not find a best version.")
            
        print("\n" + "#"*60)
        print(f"Workflow for '{chapter_name}' has completed successfully.")
        print("#"*60 + "\n")


async def main():
    # The URL from the assignment
    target_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter_name = "The_Gates_of_Morning_Ch1"

    orchestrator = WorkflowOrchestrator()
    await orchestrator.run_full_workflow(url=target_url, chapter_name=chapter_name)

if __name__ == "__main__":
    # In some environments, you might need to run playwright install first
    # from the command line: playwright install
    asyncio.run(main())