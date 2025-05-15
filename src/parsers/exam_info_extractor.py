class ExamInfoExtractor:
    def extract_exam_info(self, soup):
        """Extract exam information from the HTML soup"""
        exam_info = {}
        exam_qa_div = soup.find('div', class_='examQa')
        if exam_qa_div:
            # Get exam title
            title_element = exam_qa_div.find('h2')
            if title_element:
                exam_info['title'] = title_element.text.strip()
            
            # Get last updated date
            date_element = exam_qa_div.find('span', class_='examQa__date')
            if date_element:
                exam_info['last_updated'] = date_element.text.strip()
            
            # Get exam details from items
            exam_items = exam_qa_div.find_all('div', class_='examQa__item')
            for item in exam_items:
                spans = item.find_all('span')
                if len(spans) >= 2:
                    key = spans[0].text.strip().replace(':', '').strip()
                    value = spans[1].text.strip()
                    exam_info[key] = value
        
        return exam_info
    
    def format_exam_info(self, exam_info):
        """Convert exam info to markdown format"""
        markdown_output = []
        markdown_output.append(f"# {exam_info.get('title', 'Exam Questions')}")
        markdown_output.append("")
        markdown_output.append(f"*{exam_info.get('last_updated', '')}*")
        markdown_output.append("")
        
        # Add other exam information
        for key, value in exam_info.items():
            if key not in ['title', 'last_updated']:
                markdown_output.append(f"**{key}:** {value}")
        
        markdown_output.append("\n---\n")
        
        return markdown_output
