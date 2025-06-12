import re
import json
import requests
from bs4 import BeautifulSoup
from src.parsers.image_handler import ImageHandler


class QuestionProcessor:
    def __init__(self, file_utils):
        self.file_utils = file_utils
        self.image_handler = ImageHandler(file_utils)

    def process_questions(self, soup, assets_folder):
        """Process all question cards and convert to markdown"""
        markdown_output = []
        question_cards = soup.find_all("div", class_="exam-question-card")

        for card in question_cards:
            header_md = self._process_question_header(card)
            markdown_output.extend(header_md)

            body_md = self._process_question_body(card, assets_folder)
            markdown_output.extend(body_md)

            markdown_output.append("\n---\n")

        return markdown_output

    def _process_question_header(self, card):
        """Extract question header information (number and topic)"""
        markdown_lines = []
        header = card.find("div", class_="card-header")
        if header:
            question_number = header.get_text().strip().split("\n")[0].strip()
            topic = ""
            topic_span = header.find("span", class_="question-title-topic")
            if topic_span:
                topic = topic_span.text.strip()

            markdown_lines.append(f"## {question_number} ({topic})")

        return markdown_lines

    def _process_question_body(self, card, assets_folder):
        """Process the question body including text, images, choices and answers"""
        markdown_lines = []
        body = card.find("div", class_="card-body")
        if not body:
            return markdown_lines

        # Add question ID if available
        question_id = body.get("data-id")
        if question_id:
            markdown_lines.append(f"*Question ID: {question_id}*\n")

        # Process question text and images
        question_text = self._process_question_text(body, assets_folder)
        markdown_lines.extend(question_text)

        # Process choices
        choices_container = body.find("div", class_="question-choices-container")
        if choices_container:
            choices_md = self._process_choices(choices_container, assets_folder)
            markdown_lines.extend(choices_md)

        # Process correct answer
        answer_md = self._process_correct_answer(body, assets_folder)
        markdown_lines.extend(answer_md)

        # Fetch and add top 3 discussion comments
        if question_id:
            top_comments = self.fetch_top_discussion_comments(question_id)
            if top_comments:
                markdown_lines.append("\n**Top 3 Discussion Comments:**")
                for idx, comment in enumerate(top_comments, 1):
                    markdown_lines.append(
                        f"\n> **{comment['author']}** ({comment['votes']} votes):\n> {comment['content']}"
                    )

        return markdown_lines

    def _process_question_text(self, body, assets_folder):
        """Extract and process the question text with images"""
        markdown_lines = []
        question_text = body.find("p", class_="card-text")
        if not question_text:
            return markdown_lines

        # Process images inside question text
        self.image_handler.process_images_in_element(question_text, assets_folder)

        text_content = question_text.get_text().strip()
        if text_content:
            markdown_lines.append(text_content)
            markdown_lines.append("")

        # Check for any remaining images directly in question text
        for img in question_text.find_all("img"):
            img_md = self.image_handler.get_image_markdown(img, assets_folder)
            if img_md:
                markdown_lines.append(img_md)
                markdown_lines.append("")

        return markdown_lines

    def _process_choices(self, choices_container, assets_folder):
        """Process question choices and convert to markdown"""
        markdown_lines = []
        choice_items = choices_container.find_all("li", class_="multi-choice-item")

        for item in choice_items:
            choice_letter = item.find("span", class_="multi-choice-letter")
            letter = ""
            if choice_letter:
                letter = choice_letter.get_text().strip()

            # Check if this is the correct answer
            is_correct = "correct-hidden" in item.get("class", [])

            # Process images in choice text
            self.image_handler.process_images_in_element(item, assets_folder)

            # Get the choice text (excluding the letter part)
            choice_text = item.get_text().strip()
            choice_text = re.sub(rf"^{letter}\s*", "", choice_text).strip()
            # Also remove "Most Voted" if present
            choice_text = re.sub(r"Most Voted\s*$", "", choice_text).strip()

            # Mark correct answer
            markdown_choice = f"- **{letter}** {choice_text}"
            if is_correct:
                markdown_choice += " ✓"  # Mark correct answer

            markdown_lines.append(markdown_choice)

            # Check if there are any images in this choice that weren't processed via text
            for img in item.find_all("img"):
                img_md = self.image_handler.get_image_markdown(img, assets_folder)
                if img_md:
                    markdown_lines.append(f"  {img_md}")

        return markdown_lines

    def _process_correct_answer(self, body, assets_folder):
        """Process the correct answer section"""
        markdown_lines = []
        # Use a more flexible selector that looks for elements containing both required classes
        answer_p = body.find(
            "p",
            class_=lambda c: c
            and all(cls in c.split() for cls in ["card-text", "question-answer"]),
        )
        if not answer_p:
            return markdown_lines

        markdown_lines.append("\n**Correct Answer:**")

        correct_span = answer_p.find("span", class_="correct-answer")
        if correct_span:
            markdown_lines.append(f"**{correct_span.text.strip()}**")

        # Process images in explanation
        for img in answer_p.find_all("img"):
            img_md = self.image_handler.get_image_markdown(img, assets_folder)
            if img_md:
                markdown_lines.append(img_md)

        vote_div = answer_p.find("div", class_="voting-summary")
        if vote_div:
            markdown_lines.append("\n**Community vote distribution:**")

            progress_bar = vote_div.find("div", class_="vote-distribution-bar")
            if progress_bar:
                vote_bars = progress_bar.find_all("div", class_="vote-bar")

                for bar in vote_bars:
                    # Only process visible vote bars (display: flex)
                    if bar.get("style") and "display: flex" in bar.get("style"):
                        option_text = bar.text.strip()
                        width_match = re.search(
                            r"width:\s*(\d+)%", bar.get("style", "")
                        )
                        percentage = width_match.group(1) if width_match else "?"

                        # Get vote count from tooltip
                        vote_count = "?"
                        if (
                            bar.has_attr("data-original-title")
                            and "vote" in bar["data-original-title"]
                        ):
                            vote_count_match = re.search(
                                r"(\d+)\s*vote", bar["data-original-title"]
                            )
                            if vote_count_match:
                                vote_count = vote_count_match.group(1)

                        markdown_lines.append(f"- {option_text}: {vote_count} votes")

        return markdown_lines

    def fetch_top_discussion_comments(self, question_id, top_n=3):
        """
        Fetch and parse the top N most voted comments for a question.
        Returns a list of dicts: [{'author': ..., 'votes': ..., 'content': ...}, ...]
        """
        url = f"https://www.examtopics.com/ajax/discussion/exam-question/{question_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            comments = []
            # Each comment is a div with class "media comment-container"
            for comment_div in soup.find_all("div", class_="media comment-container"):
                # Author
                author = "Anonymous"
                username_tag = comment_div.find("h5", class_="comment-username")
                if username_tag:
                    author = username_tag.get_text(strip=True)
                # Votes
                votes = 0
                upvote_span = comment_div.find("span", class_="upvote-count")
                if upvote_span:
                    try:
                        votes = int(upvote_span.get_text(strip=True))
                    except Exception:
                        votes = 0
                # Content
                content = ""
                content_div = comment_div.find("div", class_="comment-content")
                if content_div:
                    content = content_div.get_text(separator="\n").strip()
                # Only add if there is content
                if content:
                    comments.append(
                        {"author": author, "votes": votes, "content": content}
                    )
            # Sort by votes descending and return top N
            comments.sort(key=lambda c: c["votes"], reverse=True)
            return comments[:top_n]
        except Exception as e:
            print(f"Failed to fetch discussion for question {question_id}: {e}")
            return []
