import re

TEST_HTML_FILE = "test_html"


def get_link_from_html(html_text):
    link_list = []

    while len(html_text):
        match_object = re.search(r'("https://[^"]*")'
                                 r'|("http://[^"]*")', html_text)
        if not match_object:
            break
        html_text = html_text[match_object.end():]
        link_list.append(match_object.group(0))

    return link_list


if __name__ == "__main__":
    link_list = None

    with open(TEST_HTML_FILE, encoding="utf_8") as file:
        link_list = get_link_from_html(file.read())

    print(link_list)
