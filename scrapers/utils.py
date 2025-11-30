"""
Scraping Utilities
Common helper functions for scraping
"""
import re
import json
from urllib.parse import urlparse


def format_price(price_value, min_price=10, max_price=1000000):
    """Format price to Turkish format (X.XXX,XX TL)"""
    try:
        if isinstance(price_value, str):
            # Clean price string
            price_clean = re.sub(r'[^\d,\.]', '', price_value)
            if ',' in price_clean and '.' in price_clean:
                # Format: 12,999.00 (English)
                price_clean = price_clean.replace(',', '')
            elif '.' in price_clean:
                # Format: 12.999,00 (Turkish)
                price_clean = price_clean.replace('.', '').replace(',', '.')
            elif ',' in price_clean:
                # Format: 12999,00
                price_clean = price_clean.replace(',', '.')
            price_value = float(price_clean)
        
        if isinstance(price_value, (int, float)):
            if min_price <= price_value <= max_price:
                if price_value >= 1000:
                    return f"{price_value:,.2f} TL".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    return f"{price_value:.2f} TL".replace('.', ',')
    except (ValueError, TypeError):
        pass
    return None


def extract_price_from_text(text):
    """Extract price from text using regex"""
    if not text:
        return None
    
    # Turkish format (12.999,00)
    price_match = re.search(r'([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2})', text)
    if not price_match:
        # English format (12,999.00)
        price_match = re.search(r'([0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2})', text)
    if not price_match:
        # Simple format (12999.00 or 12999,00)
        price_match = re.search(r'([0-9]+[.,][0-9]{2})', text)
    if not price_match:
        # Just number (12999)
        price_match = re.search(r'([0-9]{3,})', text)
    
    if price_match:
        found_price_str = price_match.group(1)
        try:
            # Convert to float
            if ',' in found_price_str and '.' in found_price_str:
                price_clean = found_price_str.replace(',', '')
            elif '.' in found_price_str:
                price_clean = found_price_str.replace('.', '').replace(',', '.')
            elif ',' in found_price_str:
                price_clean = found_price_str.replace(',', '.')
            else:
                price_clean = found_price_str
            
            return float(price_clean)
        except ValueError:
            return None
    return None


async def extract_json_ld_price(page):
    """Extract price from JSON-LD structured data"""
    try:
        json_ld_scripts = await page.query_selector_all('script[type="application/ld+json"]')
        for script in json_ld_scripts:
            script_content = await script.text_content()
            if script_content and ('offers' in script_content or 'price' in script_content):
                try:
                    data = json.loads(script_content)
                    
                    # Handle different JSON-LD structures
                    if isinstance(data, dict):
                        # Direct offers
                        if 'offers' in data:
                            offers = data['offers']
                            if isinstance(offers, dict) and 'price' in offers:
                                price_value = offers['price']
                                if isinstance(price_value, (int, float)) and price_value > 0:
                                    return price_value, offers.get('highPrice')
                            elif isinstance(offers, list) and len(offers) > 0:
                                if 'price' in offers[0]:
                                    price_value = offers[0]['price']
                                    if isinstance(price_value, (int, float)) and price_value > 0:
                                        return price_value, None
                        # @graph structure
                        elif '@graph' in data:
                            for item in data['@graph']:
                                if isinstance(item, dict) and item.get('@type') == 'Product' and 'offers' in item:
                                    offers = item['offers']
                                    if isinstance(offers, dict) and 'price' in offers:
                                        price_value = offers['price']
                                        if isinstance(price_value, (int, float)) and price_value > 0:
                                            return price_value, offers.get('highPrice')
                    # Array structure
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get('@type') == 'Product' and 'offers' in item:
                                offers = item['offers']
                                if isinstance(offers, dict) and 'price' in offers:
                                    price_value = offers['price']
                                    if isinstance(price_value, (int, float)) and price_value > 0:
                                        return price_value, offers.get('highPrice')
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"[DEBUG] JSON-LD extraction error: {e}")
    
    return None, None


async def extract_meta_price(page, meta_selectors=None):
    """Extract price from meta tags"""
    if meta_selectors is None:
        meta_selectors = [
            'meta[property="product:price:amount"]',
            'meta[name="twitter:data1"]',
            'meta[property="og:price:amount"]'
        ]
    
    for meta_selector in meta_selectors:
        try:
            meta_price = await page.query_selector(meta_selector)
            if meta_price:
                price_value = await meta_price.get_attribute('content')
                if price_value:
                    try:
                        price_float = float(price_value)
                        if price_float > 0:
                            return price_float
                    except ValueError:
                        continue
        except Exception:
            continue
    
    return None


def normalize_image_url(src, base_url):
    """Normalize image URL to absolute URL"""
    if not src:
        return None
    
    if src.startswith('//'):
        return 'https:' + src
    elif src.startswith('/'):
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}{src}"
    elif src.startswith('http'):
        return src
    
    return None


def should_skip_image(src, skip_keywords=None):
    """Check if image should be skipped based on keywords"""
    if skip_keywords is None:
        skip_keywords = ['logo', 'banner', 'icon', 'header', 'footer', 'ad', 'promo', 'campaign', 'placeholder', 'loading']
    
    if not src:
        return True
    
    src_lower = src.lower()
    return any(keyword in src_lower for keyword in skip_keywords)

