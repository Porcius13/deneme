"""
Scrapers Module
Site-specific scraping logic organized by domain
"""

from scrapers.site_specific import SiteSpecificExtractor
from scrapers.config import SITE_CONFIGS, get_site_config

__all__ = ['SiteSpecificExtractor', 'SITE_CONFIGS', 'get_site_config']

