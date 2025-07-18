import time

class AIWriterAgent:
    """
    Simulates an AI agent that "spins" or rewrites text.
    """
    def spin_chapter(self, text: str, prompt: str) -> str:
        """
        Applies a "spin" to the text based on a prompt.

        Args:
            text: The original chapter text.
            prompt: The instruction for rewriting.

        Returns:
            The rewritten text.
        """
        print(f"AIWriterAgent: Receiving text and prompt: '{prompt}'")
        print("AIWriterAgent: Simulating AI-powered rewriting...")
        time.sleep(2) # Simulate processing time
        spun_text = f"--- Start of AI Writer Output ---\n\n"
        spun_text += f"Prompt: {prompt}\n\n"
        spun_text += text + "\n\n--- This chapter has been re-imagined by the AI Writer. ---\n"
        spun_text += f"--- End of AI Writer Output ---"
        print("AIWriterAgent: Rewriting complete.")
        return spun_text

class AIReviewerAgent:
    """
    Simulates an AI agent that reviews and refines text.
    """
    def review_chapter(self, text: str, prompt: str) -> str:
        """
        Reviews and refines the given text based on a prompt.

        Args:
            text: The text to be reviewed (typically from the AI Writer).
            prompt: The instruction for reviewing.

        Returns:
            The refined text.
        """
        print(f"AIReviewerAgent: Receiving text and prompt: '{prompt}'")
        print("AIReviewerAgent: Simulating AI-powered review and refinement...")
        time.sleep(2) # Simulate processing time
        reviewed_text = f"--- Start of AI Reviewer Output ---\n\n"
        reviewed_text += f"Review Prompt: {prompt}\n\n"
        # Simulate a refinement by removing the writer's headers
        text_to_review = text.replace("--- Start of AI Writer Output ---\n\n", "").replace("--- End of AI Writer Output ---", "")
        reviewed_text += text_to_review
        reviewed_text += "\n--- This version has been polished and verified for quality by the AI Reviewer. ---\n"
        reviewed_text += f"--- End of AI Reviewer Output ---"
        print("AIReviewerAgent: Review complete.")
        return reviewed_text