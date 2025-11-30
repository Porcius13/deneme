"""
Site Configuration
Contains all site-specific selectors and configurations
"""
import re
from urllib.parse import urlparse

# Site-specific configurations
SITE_CONFIGS = {
    "ltbjeans.com": {
        "image_selectors": [
            "img[src*='ltbjeans-hybris-p1.mncdn.com']",
            "img[alt*='Regular Askılı']",
            "img[title*='Regular Askılı']"
        ],
        "price_selectors": [
            "span.dis__new--price",
            ".dis__new--price"
        ],
        "old_price_selectors": [
            "span.dis__old--price",
            ".dis__old--price"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "koton.com": {
        "image_selectors": [
            "img.lg-object.lg-image",
            "img[src*='ktnimg2.mncdn.com']",
            "img[class*='lg-image']"
        ],
        "price_selectors": [
            "pz-price[rendered='true']",
            "pz-price"
        ],
        "old_price_selectors": [],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "defacto.com.tr": {
        "image_selectors": [
            "img.product-image",
            "img[class*='product-image']",
            "img[src*='defacto']"
        ],
        "price_selectors": [
            "div.base-price.campaing-base-price",
            ".campaing-base-price",
            "div.base-price span"
        ],
        "old_price_selectors": [
            "div.base-price.lined-base-price",
            ".lined-base-price"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "mavi.com": {
        "image_selectors": [
            "img[src*='sky-static.mavi.com']",
            "img[src*='mavi.com']",
            "img[alt*='LONDON']"
        ],
        "price_selectors": [
            "span.price",
            ".price",
            "span.nodiscount-price",
            ".nodiscount-price"
        ],
        "old_price_selectors": [],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "pullandbear.com": {
        "image_selectors": [
            "img[data-qa-image]",
            "img#product-image",
            "img#image",
            ".product-media img",
            ".product-image img",
            "img[src*='static.pullandbear.net']",
            "img[srcset*='static.pullandbear.net']",
            "img[src*='pullandbear.net/assets']"
        ],
        "price_selectors": [
            "div[class*='price'] span[class*='current']",
            "span.current-price",
            "span[data-testid='current-price']",
            ".price-current",
            "span.number",
            ".number",
            "span.number:first-of-type"
        ],
        "old_price_selectors": [
            "div[class*='price'] span[class*='old']",
            "span.old-price",
            "span[data-testid='old-price']",
            ".price-old",
            "span.number:last-of-type",
            "span.number",
            ".number"
        ],
        "title_selectors": [
            "h1[data-testid='product-name']",
            "h1.product-name",
            "h1.product-title",
            ".product-name",
            "h1"
        ]
    },
    "marksandspencer.com.tr": {
        "image_selectors": [
            "img[src*='products']",
            "img[alt*='Pantolon']",
            "img[alt*='pantolon']",
            "img[alt*='Keten']",
            "img[alt*='keten']",
            "img[class*='js-image-zoom']",
            "img[src*='a53e12.a-cdn.akinoncloud.com/products']"
        ],
        "price_selectors": [
            ".price",
            ".current-price",
            ".sale-price",
            "[class*='price']"
        ],
        "old_price_selectors": [
            ".old-price",
            ".original-price",
            ".price-old",
            "s.price",
            "del.price",
            "[class*='old'][class*='price']"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name",
            "[class*='product'][class*='title']"
        ]
    },
    "bershka.com": {
        "image_selectors": [
            "img[data-qa-anchor='pdpMainImage']",
            "img[src*='static.bershka.net']",
            "img.image-item"
        ],
        "price_selectors": [
            "span.current-price-elem--discounted",
            ".current-price-elem--discounted",
            "span[data-qa-anchor='productItemDiscount']"
        ],
        "old_price_selectors": [
            "s.old-price-elem",
            ".old-price-elem",
            "s[data-qa-anchor='productItemPrice']"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "shop.mango.com": {
        "image_selectors": [
            "img.ImageGridItem_image__VVZxr",
            "img[src*='shop.mango.com/assets']",
            "img[alt*='Cepli keten gömlek']",
            "img[srcset*='shop.mango.com/assets']",
            "img[decoding='async']",
            "img[data-nimg='1']",
            "img[style*='color:transparent']"
        ],
        "price_selectors": [
            "span.SinglePrice_finalPrice__XBL1k",
            ".SinglePrice_finalPrice__XBL1k",
            "span.SinglePrice_center__TMNty.texts_bodyM__Y2ZHT.SinglePrice_finalPrice__XBL1k",
            "span[class*='SinglePrice_finalPrice']",
            "span[class*='finalPrice']"
        ],
        "old_price_selectors": [
            "span.SinglePrice_crossed__mUCG8",
            ".SinglePrice_crossed__mUCG8",
            "span.SinglePrice_crossed__mUCG8.SinglePrice_center__TMNty.texts_bodyM__Y2ZHT",
            "span[class*='SinglePrice_crossed']",
            "span[class*='crossed']"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name",
            "h1",
            "title",
            "h1[class*='product']",
            "h1[class*='title']"
        ]
    },
    "stradivarius.com": {
        "image_selectors": [
            "img.product-image",
            "img[class*='product-image']",
            "img[src*='stradivarius']"
        ],
        "price_selectors": [
            "span.price",
            ".price"
        ],
        "old_price_selectors": [
            "span.old-price",
            ".old-price"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "kaft.com": {
        "image_selectors": [
            "img.product-image",
            "img[class*='product-image']",
            "img[src*='kaft']"
        ],
        "price_selectors": [
            "span.current",
            ".current",
            "span.price"
        ],
        "old_price_selectors": [],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "wwfmarket.com": {
        "image_selectors": [
            "img.product__media",
            "img[src*='wwfmarket.com/cdn']",
            "img[alt*='Bozayı']"
        ],
        "price_selectors": [
            "span.price-item--sale",
            ".price-item--sale"
        ],
        "old_price_selectors": [
            "span.price-item--regular",
            ".price-item--regular"
        ],
        "title_selectors": [
            "h1.product__title",
            "h1.product-name",
            ".product__title"
        ]
    },
    "lesbenjamins.com": {
        "image_selectors": [
            "img.product__media-image",
            "img.product-single__media-image",
            ".product__media img",
            ".product-single__media img",
            "img[data-product-image]"
        ],
        "price_selectors": [
            ".product__price",
            ".product-single__price",
            "span.price"
        ],
        "old_price_selectors": [],
        "title_selectors": [
            "h1.product__title",
            "h1.product-single__title",
            ".product__title"
        ]
    },
    "zara.com": {
        "image_selectors": [
            "img.product-detail-image",
            "img[src*='static.zara.net']",
            ".product-detail-image img"
        ],
        "price_selectors": [
            "span.price",
            ".price",
            "span.money"
        ],
        "old_price_selectors": [
            "span.old-price",
            ".old-price"
        ],
        "title_selectors": [
            "h1.product-name",
            "h1.product-title",
            ".product-name"
        ]
    },
    "sportime.com.tr": {
        "image_selectors": [
            "img.product__media-image",
            "img.product-single__media-image",
            ".product__media img",
            "img[src*='cdn.shopify.com']"
        ],
        "price_selectors": [
            ".product-price .money",
            ".product__price .money",
            "span.money"
        ],
        "old_price_selectors": [
            ".product-price .money:first-child",
            ".old-price .money"
        ],
        "title_selectors": [
            "h1.product__title",
            "h1.product-single__title",
            ".product__title"
        ]
    }
}

# Standard timeout values (in milliseconds)
TIMEOUT_CONFIG = {
    "page_load": 90000,      # 90 seconds for page load
    "network_idle": 30000,   # 30 seconds for network idle
    "element_wait": 10000,    # 10 seconds for element wait
    "navigation": 20000,     # 20 seconds for navigation
    "default": 15000         # 15 seconds default
}

def get_site_config(url):
    """Get site configuration for a given URL"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace('www.', '')
        
        # Direct match
        if domain in SITE_CONFIGS:
            return SITE_CONFIGS[domain]
        
        # Partial match (e.g., "shop.mango.com" matches "mango.com")
        for config_domain, config in SITE_CONFIGS.items():
            if config_domain in domain or domain in config_domain:
                return config
        
        return None
    except Exception as e:
        print(f"[ERROR] Error getting site config: {e}")
        return None

def get_timeout(timeout_type="default"):
    """Get standardized timeout value"""
    return TIMEOUT_CONFIG.get(timeout_type, TIMEOUT_CONFIG["default"])

