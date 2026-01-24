from bs4 import BeautifulSoup
from bs4.element import NavigableString

from configs.settings import settings
from pkg.utils.text import add_trademark


def process_html(html: str, proxy_url: str) -> str:
    soup = BeautifulSoup(html, 'lxml')

    for element in soup.find_all(text=True):
        if isinstance(element, NavigableString) and element.parent.name not in ['script', 'style']:
            new_text = add_trademark(str(element))
            element.replace_with(new_text)

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/'):
            link['href'] = f'{proxy_url}{href}'
        elif settings.hn_base_url in href:
            link['href'] = href.replace(settings.hn_base_url, proxy_url)

    for form in soup.find_all('form', action=True):
        action = form['action']
        if action.startswith('/'):
            form['action'] = f'{proxy_url}{action}'
        elif settings.hn_base_url in action:
            form['action'] = action.replace(settings.hn_base_url, proxy_url)

    return str(soup)
