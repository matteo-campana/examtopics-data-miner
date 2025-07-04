from scrapers.html_scraper import HtmlScraper
from parsers.html_parser import HtmlParser
from store.data_store import DataStore
from utils.file_utils import FileUtils
import os
from tqdm import tqdm

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich import box
import re


import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

console = Console()


def execute():
    """Main command line interface execution function"""
    console.print(Panel("[bold cyan]ExamTopics Data Miner[/bold cyan]", expand=False))
    console.print("[bold]Choose input source:[/bold]")
    console.print("[green]1.[/green] URL (web scraping)")
    console.print("[green]2.[/green] Local HTML file")
    console.print("[green]3.[/green] Folder of HTML files")  # New option
    choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")

    html_content = None
    input_filename = None

    if choice == "1":
        scraper = HtmlScraper()
        try:
            # Optional: Print ChromeDriver and Chrome versions for debugging
            try:
                from selenium import webdriver  # type: ignore

                driver = webdriver.Chrome()
                console.print(
                    f"[cyan]Chrome version:[/cyan] {driver.capabilities.get('browserVersion')}"
                )
                console.print(
                    f"[cyan]ChromeDriver version:[/cyan] {driver.capabilities.get('chrome', {}).get('chromedriverVersion')}"
                )
                driver.quit()
            except Exception as version_exc:
                console.print(
                    f"[yellow]Could not determine Chrome/ChromeDriver version:[/yellow] {version_exc}"
                )

            profiles = scraper.get_chrome_profiles_info()
            selected_profile = None
            if profiles:
                table = Table(title="Available Chrome Profiles", box=box.SIMPLE)
                table.add_column("No.", style="cyan", justify="right")
                table.add_column("Profile", style="magenta")
                table.add_column("Name", style="green")
                table.add_column("Email", style="yellow")
                for idx, info in enumerate(profiles):
                    table.add_row(
                        str(idx + 1),
                        str(info["profile"]),
                        str(info["name"]),
                        str(info["email"]),
                    )
                console.print(table)
                sel = Prompt.ask("Select a profile by number", default="1")
                try:
                    sel_idx = int(sel) - 1 if sel else 0
                    selected_profile = profiles[sel_idx]["profile"]
                except Exception:
                    console.print("[red]Invalid selection, using first profile.[/red]")
                    selected_profile = profiles[0]["profile"]
                console.print("\n---\n")
            else:
                console.print("[yellow]No Chrome profiles found.[/yellow]")
            url = Prompt.ask(
                "Enter the URL to scrape",
                default="https://www.examtopics.com/exams/microsoft/az-204/view/",
            )
            html_content = scraper.scrape(url, profile_dir=selected_profile)
            # Build filename based on URL format
            # Examples:
            # https://www.examtopics.com/exams/microsoft/az-204/view/      -> az-204.html
            # https://www.examtopics.com/exams/microsoft/az-204/view/1     -> az-204-1.html
            # https://www.examtopics.com/exams/microsoft/az-204/view/2     -> az-204-2.html
            # https://www.examtopics.com/exams/microsoft/az-204/view/3     -> az-204-3.html
            match = re.search(
                r"/exams/[^/]+/(?P<exam>[^/]+)/view(?:/(?P<page>\d+))?", url
            )
            if match:
                exam = match.group("exam")
                page = match.group("page")
                if page:
                    input_filename = f"{exam}-{page}.html"
                else:
                    input_filename = f"{exam}.html"
            else:
                input_filename = "scraped_content.html"
        except Exception as e:
            console.print(
                "[bold red]Error during Chrome profile selection or scraping:[/bold red]"
            )
            console.print(f"[red]{e}[/red]")
            console.print(
                Panel(
                    "- Ensure ChromeDriver version matches your installed Chrome.\n"
                    "- Make sure Chrome is not running in another user session.\n"
                    "- Try updating both Chrome and ChromeDriver.",
                    title="Tips",
                    style="yellow",
                )
            )
            return
    elif choice == "2":
        file_path = Prompt.ask("Enter path to HTML file", default="data/sample.html")
        input_filename = file_path
        try:
            html_content = DataStore.read_file(file_path)
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {e}")
            return
    elif choice == "3":
        folder_path = Prompt.ask(
            "Enter path to folder with HTML files", default="data/sample_folder"
        )
        if not os.path.isdir(folder_path):
            console.print(f"[bold red]Folder not found:[/bold red] {folder_path}")
            return

        output_base = "output"
        # Use the name of the input directory (not just the last folder)
        input_dir_name = os.path.basename(os.path.normpath(folder_path))
        output_folder = os.path.join(output_base, input_dir_name)
        os.makedirs(output_folder, exist_ok=True)

        parser = HtmlParser()
        processed = 0
        html_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".html")]
        for filename in tqdm(html_files, desc="Processing HTML files", unit="file"):
            file_path = os.path.join(folder_path, filename)
            try:
                html_content = DataStore.read_file(file_path)
                data = parser.parse(
                    html_content, save_output=False, input_filename=filename
                )
                # Save result as .md in output_folder using FileUtils
                file_utils = FileUtils()
                output_file = os.path.join(
                    output_folder, f"{os.path.splitext(filename)[0]}.md"
                )
                file_utils.save_output(data, input_filename=output_file)
                processed += 1
                console.print(f"[green]Processed:[/green] {filename} -> {output_file}")
            except Exception as e:
                console.print(f"[red]Failed to process {filename}: {e}[/red]")
        console.print(f"[bold blue]Processed {processed} HTML files.[/bold blue]")
        console.print(f"[bold green]Results saved in:[/bold green] {output_folder}")
        return
    else:
        console.print("[red]Invalid choice[/red]")
        return

    if not html_content:
        console.print("[red]No HTML content to parse[/red]")
        return

    console.print(f"[bold blue]Input filename:[/bold blue] {input_filename}")

    parser = HtmlParser()
    data = parser.parse(html_content, save_output=False, input_filename=input_filename)

    # Save output for single file/URL
    file_utils = FileUtils()
    file_utils.save_output(data, input_filename=input_filename)
    console.print(f"[green]Saved output to output folder.[/green]")

    console.print(Panel("[bold green]Extracted Data:[/bold green]", expand=False))
    console.print(data)
