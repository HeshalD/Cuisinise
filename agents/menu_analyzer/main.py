import sys
from menu_analyzer import ask_user, nlp_query

# Optional: colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    C = {
        "title": Fore.CYAN + Style.BRIGHT,
        "option": Fore.YELLOW,
        "input": Fore.GREEN,
        "error": Fore.RED,
        "success": Fore.MAGENTA,
        "info": Fore.BLUE
    }
except ImportError:
    C = {k: "" for k in ["title", "option", "input", "error", "success", "info"]}


def main():
    """Main NLP Menu Analyzer for your existing CSV data"""
    print(f"{C['title']}🧠 === NLP MENU ANALYZER FOR YOUR DATA ===")
    print(f"{C['info']}Uses YOUR existing CSV file with NLP processing")
    print(f"{C['info']}✨ Now with downloadable results!")
    print("="*60)

    while True:
        print(f"\n{C['option']}🚀 NLP Options:")
        print(f"{C['option']}(1) 🗣️ Conversational NLP Search - Chat naturally")
        print(f"{C['option']}(2) ⚡ Quick NLP Query - Single search")
        print(f"{C['option']}(3) 📥 Bulk Download - Get comprehensive results")
        print(f"{C['option']}(4) 🚪 Exit")
        print("-" * 40)

        try:
            mode = input(f"{C['input']}Choose (1-4): ").strip()

            if mode == "1":
                print(f"\n{C['success']}🗣️ Starting NLP Conversational Search...")
                print(f"{C['info']}💡 After each search, you'll get download options!")
                ask_user()  # prompts for CSV file path and starts conversation

            elif mode == "2":
                print(f"\n{C['success']}⚡ Quick NLP Query")
                query = input(f"{C['input']}🧠 Enter your natural language query: ").strip()

                if query:
                    result = nlp_query(query)  # processes query on CSV
                    if result:
                        print(f"{C['success']}✅ Query processed successfully!")
                else:
                    print(f"{C['error']}❌ Please enter a valid query.")

            elif mode == "3":
                print(f"\n{C['success']}📥 Bulk Download Mode")
                from menu_analyzer import initialize_with_your_file
                searcher = initialize_with_your_file()
                if searcher:
                    query = input(f"{C['input']}🧠 Enter query for bulk download: ").strip()
                    if query:
                        searcher.download_full_filtered_results(query, max_results=200)
                        print(f"{C['success']}✅ Bulk download complete!")
                    else:
                        print(f"{C['error']}❌ Query cannot be empty.")

            elif mode == "4":
                print(f"{C['info']}👋 Goodbye! Have a great day!")
                break

            else:
                print(f"{C['error']}❌ Invalid choice. Please choose 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print(f"\n{C['info']}👋 Goodbye! Exiting gracefully...")
            break


if __name__ == "__main__":
    main()
