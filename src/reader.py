from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import json


class PdfReader:
    def __init__(self, dpf_path, interface=None, title_max_length=40):
        self.pdf_path = dpf_path
        self.title_max_length = title_max_length
        self.interface = interface
        self.contents, self.titles = self.get_contents_and_titles()
        self.titles = self.filter_title(self.titles)
        self.sections = self.format_section(self.contents, self.titles)
        self.interface.construct_section_prompt(self.sections)

    def get_contents_and_titles(self):
        contents = []
        possible_titles = []
        for page_layout in extract_pages(self.pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    txt = element.get_text().strip()
                    if len(txt) < 5:
                        continue
                    if len(txt.split("\n")) > len(txt)/10:
                        continue
                    contents.append(txt)
                    if len(txt) < self.title_max_length:
                        possible_titles.append(txt)
        return contents, possible_titles 

    def filter_title(self, titles):
        prompt = (
            f"I will provide you a list of potential titles from a scholar paper.\n"
            f"Your task is to find out the title of each section. For example, abstract, introduction, etc.\n"
            f"The paper might include appendix.\n\n"
            f"Potential title list: {titles}\n\n"
            f"You need to return all possible titles that are the same as the original text.\n"
            f"Please return a python list without any extra text."
        )
        response = self.interface.completion(prompt, temperature=0)
        titles = [x.strip("\'\"").lower() for x in response.strip('][').split(', ')]
        return titles

    def format_section(self, contents, titles):
        sections = {}
        title = "header (it might include paper's title, authors' name and affiliations)"
        text = ""
        for content in contents:
            if len(sections) > 5:
                break
            content = content.strip()
            if len(content) < self.title_max_length and content.lower() in titles:
                sections[title] = text
                text = content
                title = content
            text = "\n".join((text, content))
        sections[title] = text
        return sections
