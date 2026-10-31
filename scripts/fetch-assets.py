"""Download public product images for the curated catalogue; no API credentials."""
import concurrent.futures
import html
import io
import json
import pathlib
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'dist' / 'catalog.mjs'

class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = []
        self.images = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('property', a.get('name', '')) in ('og:image', 'twitter:image'):
            self.meta.append(a.get('content', ''))
        if tag == 'img':
            self.images.append(a)

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=35) as response:
        return response.read()

pages = {
    'lite16': 'https://store.acer.com/en-my/acer-consumer-laptop-acer-aspire-lite-16-al16-71p-54r5-light-silver-windows-11-home-intelr-coretm-ultra-5-processor-125h',
    'go14': 'https://store.acer.com/en-my/acer-consumer-laptop-aspire-go-14-ag14-i71m-52dp-steel-gray-windows-11-home-intelr-coretm-ultra-5-processor-125h',
    'lite14': 'https://store.acer.com/en-my/acer-consumer-laptop-aspire-lite-14-amd-al14-45p-r1lf',
    'aspire7': 'https://store.acer.com/en-my/acer-gaming-notebook-acer-aspire-7-gaming-a715-59g-555y-geforce-rtxtm-4050-windows-11-home-intelr-coretm-5-processor-210h',
    'air': 'https://www.apple.com/my/macbook-air/',
    'a17': 'https://www.senheng.com.my/product/samsung-galaxy-a17-5g-8256gb/',
    'redmi14': 'https://www.mi.com/my/product/redmi-note-14/',
    'redmipro': 'https://www.mi.com/my/product/redmi-note-14-pro-5g/',
    'iphone17': 'https://www.apple.com/my/iphone-17/',
    'iphone16': 'https://www.apple.com/my/iphone-16/',
}

def download(item):
    key, page = item
    try:
        source = get(page).decode('utf-8', errors='replace')
        parser = Images()
        parser.feed(source)
        candidates = parser.meta[:]
        # Acer's Open Graph photograph is normally the product hero.
        if 'acer.com' in page:
            matches = re.findall(r'"(?:img|full)"\s*:\s*"([^\"]+)"', source)
            candidates = [s.replace('\\/', '/') for s in matches] + candidates
        if 'mi.com' in page:
            candidates += [a.get('src', '') for a in parser.images if 'product' in a.get('alt', '').lower()]
        if not candidates:
            candidates = [a.get('src', a.get('data-src', '')) for a in parser.images if a.get('src', '').startswith('http')]
        image_url = next((urllib.parse.urljoin(page, html.unescape(x)) for x in candidates if x and 'logo' not in x.lower()), None)
        if not image_url:
            raise ValueError('No product image found')
        raw = get(image_url)
        (ROOT / 'dist' / 'assets' / (key + '.jpg')).write_bytes(raw)
        return {'id': key, 'image_url': image_url, 'bytes': len(raw)}
    except Exception as error:
        return {'id': key, 'error': str(error)}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(download, pages.items()))
    (ROOT / 'asset-sources.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
