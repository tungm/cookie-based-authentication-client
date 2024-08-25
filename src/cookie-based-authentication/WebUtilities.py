import requests
from lxml import etree

class WebUtilities:

    def get_page_content(url):
        response = requests.get(url)
        return response.content

    def get_elements_by_xpath(self, html_text, xpath):
        tree = etree.HTML(html_text)
        return tree.xpath(xpath)