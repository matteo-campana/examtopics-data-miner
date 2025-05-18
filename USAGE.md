# ExamTopics Data Miner - Usage Manual

This manual describes how to use the ExamTopics Data Miner command-line interface.

## Starting the Application

Run the following command from the project root:

```sh
python -m src.main
```

## Input Source Selection

When prompted, choose the input source:

- **1. URL (web scraping):** Scrape live data from ExamTopics using Selenium.
- **2. Local HTML file:** Parse a previously saved HTML file.

## Web Scraping Mode

1. The tool will attempt to detect available Chrome profiles and display them in a table.
2. Select a Chrome profile by number (or press Enter for the default).
3. Enter the ExamTopics URL to scrape (default is a sample Microsoft AZ-204 exam page).
4. The tool will launch a browser, scrape the page, and extract questions and answers.
5. The output filename is generated based on the exam and page number in the URL.

## Local HTML File Mode

1. Enter the path to your HTML file (default: `data/sample.html`).
2. The tool will read and parse the file.

## Output

- The extracted data is displayed in the terminal.
- Markdown output is saved in the `output/` directory, with a filename based on the input.

## Troubleshooting

- If ChromeDriver or Chrome versions are mismatched, or Chrome is running, you may see errors. Follow the on-screen tips to resolve.
- Ensure all dependencies are installed (`pip install -r requirements.txt`).

---

For more details, see [src/cmd/cli.py](src/cmd/cli.py).
