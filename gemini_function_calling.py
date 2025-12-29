"""
Gemini API Function Calling Demo - CLI Version
Command-line interface with detailed logging
"""

from gemini_functions import chat_with_gemini


def run_predefined_examples():
    """Run predefined examples to demonstrate function calling."""
    print("\n" + "="*60)
    print("🚀 RUNNING PREDEFINED EXAMPLES")
    print("="*60 + "\n")

    examples = [
        "Show me all speed cameras in zipcode 10036",
        "Are there any cameras on Broadway in zipcode 10001?",
        "What speed cameras are in the 90212 area code?",
        "Find cameras on Market St in San Francisco's 94103 zipcode"
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n{'#'*60}")
        print(f"EXAMPLE {i}/{len(examples)}")
        print(f"{'#'*60}\n")

        result = chat_with_gemini(example, verbose=True)

        # Check for errors
        if "error" in result:
            print(f"\n⚠️ Stopping examples due to error.\n")
            break

        if i < len(examples):
            input("Press Enter to continue to next example...")

    print(f"\n{'='*60}")
    print("✅ EXAMPLES COMPLETED")
    print(f"{'='*60}\n")


def run_interactive_mode():
    """Run interactive mode where users can ask questions."""
    print("\n" + "="*60)
    print("💬 INTERACTIVE MODE")
    print("="*60)
    print("Ask questions about speed cameras!")
    print("Type 'quit', 'exit', or 'q' to stop\n")
    print("Example questions:")
    print("  - Show me cameras in zipcode 10036")
    print("  - Are there cameras on 5th Ave in 10036?")
    print("  - What's the speed limit on Broadway in 10001?")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            result = chat_with_gemini(user_input, verbose=True)

            # Error is already printed by chat_with_gemini when verbose=True
            # Just continue to next input

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected Error: {e}\n")


def main():
    """Main entry point for the CLI program."""
    print("\n" + "="*60)
    print("🎯 GEMINI FUNCTION CALLING DEMO - CLI")
    print("Speed Camera API Integration")
    print("="*60)

    while True:
        print("\nChoose an option:")
        print("1. Run predefined examples")
        print("2. Interactive mode")
        print("3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            run_predefined_examples()
        elif choice == "2":
            run_interactive_mode()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()