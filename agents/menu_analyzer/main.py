import sys
from menu_analyzer import ask_user, nlp_query

def main():
    """Main NLP Menu Analyzer for your existing data"""
    print("🧠 === NLP MENU ANALYZER FOR YOUR DATA ===")
    print("Uses YOUR existing CSV file with NLP processing")
    print("✨ Now with downloadable results!")
    print("="*60)

    while True:
        print("\n🚀 NLP Options:")
        print("(1) 🗣️ Conversational NLP Search - Chat naturally")
        print("(2) ⚡ Quick NLP Query - Single search")
        print("(3) 📥 Bulk Download - Get comprehensive results")
        print("(4) 🚪 Exit")
        print("-" * 40)

        try:
            mode = input("Choose (1-4): ").strip()

            if mode == "1":
                print("\n🗣️ Starting NLP Conversational Search...")
                print("💡 After each search, you'll get download options!")
                ask_user()  # This will ask for your CSV file path
                
            elif mode == "2":
                print("\n⚡ Quick NLP Query")
                query = input("🧠 Enter your natural language query: ").strip()
                
                if query:
                    result = nlp_query(query)  # This will ask for your CSV file path
                else:
                    print("Please enter a query.")
            
            elif mode == "3":
                print("\n📥 Bulk Download Mode")
                from menu_analyzer import initialize_with_your_file
                searcher = initialize_with_your_file()
                if searcher:
                    query = input("🧠 Enter query for bulk download: ").strip()
                    if query:
                        searcher.download_full_filtered_results(query, max_results=200)
                    
            elif mode == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Choose 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()