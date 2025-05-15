from bs4 import BeautifulSoup
from src.parsers.file_utils import FileUtils
from src.parsers.exam_info_extractor import ExamInfoExtractor
from src.parsers.question_processor import QuestionProcessor

class HtmlParser:
    def __init__(self):
        self.file_utils = FileUtils()
        self.exam_info_extractor = ExamInfoExtractor()
        self.question_processor = QuestionProcessor(self.file_utils)
        
    def parse(self, html_content, save_output=True, output_filename=None, input_filename=None):
        """
        Parse HTML content and extract relevant information.
        Preserves scripts containing vote data, but removes unnecessary styles.
        Converts to markdown format and preserves images.
        
        Args:
            html_content (str): HTML content to parse
            save_output (bool): Whether to save output to file
            output_filename (str): Optional filename for output
            input_filename (str): Optional input filename to base output filename on
            
        Returns:
            str: Markdown formatted content
        """
        assets_folder = self.file_utils.get_assets_folder_path()
        soup = self._prepare_soup(html_content)
        
        exam_info = self.exam_info_extractor.extract_exam_info(soup)
        markdown_output = self.exam_info_extractor.format_exam_info(exam_info)
        
        questions_markdown = self.question_processor.process_questions(soup, assets_folder)
        markdown_output.extend(questions_markdown)
        
        markdown_content = "\n".join(markdown_output)
        
        # Save output if requested
        if save_output:
            self.file_utils.save_output(markdown_content, output_filename, input_filename)
        
        return markdown_content
    
    def _prepare_soup(self, html_content):
        """Parse HTML while preserving necessary elements for vote data extraction"""
        # Use html.parser to ensure better preservation of script content
        soup = BeautifulSoup(html_content, 'html.parser', preserve_whitespace_tags=['script'])
        
        # Remove only unnecessary style elements but keep all scripts and data attributes
        for element in soup.find_all('style'):
            if not element.parent or 'vote' not in str(element.parent):
                element.decompose()
                
        return soup