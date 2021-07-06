TEST_HTML_FILE = "test_html"
BODY_START = "<body"
BODY_END = "</body>"
BODY_END_LEN = len(BODY_END)


def get_body_of_html(html_text):
    return html_text[html_text.find(BODY_START):
                     html_text.find(BODY_END) + BODY_END_LEN]


if __name__ == "__main__":
    total_html = None
    with open(TEST_HTML_FILE, encoding="utf_8") as file:
        total_html = file.read()
    print(get_body_of_html(total_html))
