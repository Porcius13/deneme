"""
Test Suite for Scraping Functionality
Tests site-specific scrapers, cache, and timeout configurations
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scrapers.config import SITE_CONFIGS, get_site_config, get_timeout, TIMEOUT_CONFIG
    from scrapers.utils import format_price, extract_price_from_text, normalize_image_url
except ImportError:
    # Skip tests if scrapers module not available
    pytest.skip("Scrapers module not available", allow_module_level=True)


class TestSiteConfig:
    """Test site configuration functionality"""
    
    def test_site_configs_exists(self):
        """Test that SITE_CONFIGS is not empty"""
        assert SITE_CONFIGS is not None
        assert len(SITE_CONFIGS) > 0
    
    def test_get_site_config_bershka(self):
        """Test getting config for Bershka"""
        url = "https://www.bershka.com/tr/product/test.html"
        config = get_site_config(url)
        assert config is not None
        assert "price_selectors" in config
        assert "image_selectors" in config
        assert "title_selectors" in config
    
    def test_get_timeout_default(self):
        """Test getting default timeout"""
        timeout = get_timeout()
        assert timeout == TIMEOUT_CONFIG["default"]
    
    def test_get_timeout_page_load(self):
        """Test getting page load timeout"""
        timeout = get_timeout("page_load")
        assert timeout == TIMEOUT_CONFIG["page_load"]
        assert timeout > 0


class TestPriceUtils:
    """Test price utility functions"""
    
    def test_format_price_integer(self):
        """Test formatting integer price"""
        result = format_price(1299)
        assert result == "1.299,00 TL"
    
    def test_format_price_float(self):
        """Test formatting float price"""
        result = format_price(1299.99)
        assert result == "1.299,99 TL"
    
    def test_extract_price_from_text_turkish(self):
        """Test extracting price from Turkish format text"""
        text = "Fiyat: 1.299,99 TL"
        result = extract_price_from_text(text)
        assert result == 1299.99


class TestImageUtils:
    """Test image utility functions"""
    
    def test_normalize_image_url_absolute(self):
        """Test normalizing absolute URL"""
        base_url = "https://example.com"
        result = normalize_image_url("https://example.com/image.jpg", base_url)
        assert result == "https://example.com/image.jpg"
    
    def test_normalize_image_url_relative(self):
        """Test normalizing relative URL"""
        base_url = "https://example.com"
        result = normalize_image_url("/image.jpg", base_url)
        assert result == "https://example.com/image.jpg"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
