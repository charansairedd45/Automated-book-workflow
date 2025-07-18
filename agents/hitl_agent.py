import os

class HumanInTheLoopAgent:
    """
    Facilitates the human review and editing process.
    """
    def review_and_edit(self, original_text: str, ai_reviewed_text: str, chapter_name: str) -> str:
        """
        Presents the texts to a human for final approval or editing.

        Args:
            original_text: The initial scraped text.
            ai_reviewed_text: The text after processing by AI agents.
            chapter_name: The name of the chapter being reviewed.

        Returns:
            The finalized text after human intervention.
        """
        print("\n" + "="*50)
        print("Human-in-the-Loop (HITL) Review Stage")
        print("="*50)
        print(f"Chapter: {chapter_name}\n")
        print("The AI has produced a refined version of the chapter.")
        print("Please review the result below and choose an action.\n")
        
        print("--- AI REVIEWED VERSION ---")
        print(ai_reviewed_text[:1000] + "..." if len(ai_reviewed_text) > 1000 else ai_reviewed_text)
        print("---------------------------\n")

        while True:
            print("Choose an action:")
            print("1. Approve the AI Reviewed Version as is.")
            print("2. Manually edit the text.")
            print("3. View the original scraped text.")
            
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                print("HITL: AI version approved.")
                return ai_reviewed_text
            elif choice == '2':
                print("HITL: Please enter your final, edited version of the text.")
                print("      (You can copy-paste the AI version and modify it.)")
                print("      Press Ctrl+D (on Linux/Mac) or Ctrl+Z then Enter (on Windows) when you are finished.")
                
                edited_lines = []
                while True:
                    try:
                        line = input()
                        edited_lines.append(line)
                    except EOFError:
                        break
                edited_text = "\n".join(edited_lines)
                print("HITL: Your edited version has been saved.")
                return edited_text
            elif choice == '3':
                print("\n--- ORIGINAL SCRAPED TEXT ---")
                print(original_text[:1000] + "..." if len(original_text) > 1000 else original_text)
                print("-----------------------------\n")
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
