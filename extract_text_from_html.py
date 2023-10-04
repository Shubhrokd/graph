from bs4 import BeautifulSoup


def extract_text_from_html(html_content):
    """This function extracts the text from the articles"""

    soup = BeautifulSoup(html_content, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    article_tag = soup.find('article')
    if article_tag:
        return " ".join(article_tag.stripped_strings)
