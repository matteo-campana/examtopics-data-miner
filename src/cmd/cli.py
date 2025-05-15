from scrapers.html_scraper import HtmlScraper
from parsers.html_parser import HtmlParser
from store.data_store import DataStore
import os

def execute():
    """Main command line interface execution function"""
    print("Choose input source:")
    print("1. URL (web scraping)")
    print("2. Local HTML file")
    choice = input("Enter your choice (1 or 2): ").strip() or '2'
    
    html_content = None
    input_filename = None
    if choice == '1':
        url = input("Enter the URL to scrape: ")
        scraper = HtmlScraper()
        html_content = scraper.scrape(url)
        # Use URL as filename for web scraping
        input_filename = url.split('/')[-1] or 'scraped_content'
    elif choice == '2':
        file_path = input("Enter path to HTML file (e.g., data/sample.html): ").strip() or r"data/sample.html"
        input_filename = file_path
        try:
            html_content = DataStore.read_file(file_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Invalid choice")
        return
    
    parser = HtmlParser()
    data = parser.parse(html_content, input_filename=input_filename)
    
    print("\nExtracted Data:")
    print(data)
    
    # Ask if the user wants to save the extracted data
    # save_choice = input("\nDo you want to save the extracted data? (y/n): ").strip().lower()
    # if save_choice == 'y':
    #     output_dir = input("Enter directory to save data (default: 'output'): ").strip() or 'output'
    #     base_filename = os.path.splitext(os.path.basename(input_filename))[0]
    #     output_path = os.path.join(output_dir, f"{base_filename}_extracted.json")
        
    #     try:
    #         DataStore.save_json(output_path, data)
    #         print(f"Data saved to {output_path}")
    #     except Exception as e:
    #         print(f"Error saving data: {e}")
