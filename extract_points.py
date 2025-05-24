#!/usr/bin/env python3
"""
Extract Upper Class points for specific dates from Virgin Atlantic
"""

import asyncio
import re
from playwright.async_api import async_playwright

async def extract_upper_class_points():
    """Extract Upper Class points for Oct 19 and Oct 20"""
    url = "https://www.virginatlantic.com/reward-flight-finder/results/month?origin=LHR&destination=BLR&month=10&year=2025"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print(f"Navigating to: {url}")
        await page.goto(url, wait_until="domcontentloaded")
        
        # Handle cookie consent
        try:
            reject_button = await page.wait_for_selector('button:has-text("Reject All")', timeout=5000)
            if reject_button:
                await reject_button.click()
                print("Clicked 'Reject All' button")
                await page.wait_for_timeout(2000)
        except:
            print("No cookie consent dialog found")
        
        # Wait for page to load and try multiple approaches
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)  # Wait 5 seconds for content to load
        
        print("Extracting Upper Class points...")
        
        # Get all page text content
        page_text = await page.inner_text('body')
        
        # Also get HTML content for more detailed parsing
        page_html = await page.content()
        
        # Save debug info
        with open('/Users/sahil/reward-seat-tracker/page_content.txt', 'w') as f:
            f.write(page_text)
        
        print("Searching for Upper Class points...")
        
        # Look for patterns in the text
        oct_19_points = None
        oct_20_points = None
        
        # More specific patterns that match the actual calendar structure
        patterns = [
            # Look for "Sun 19" or "Mon 20" followed by Upper Class pricing
            r'(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+19\s+.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
            r'(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+20\s+.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
            # Alternative patterns with different spacing
            r'19\s+Economy.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
            r'20\s+Economy.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.finditer(pattern, page_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                points = match.group(1).replace(',', '')
                full_match = match.group(0)
                
                print(f"Pattern {i+1} found: {full_match.strip()}")
                
                if '19' in full_match and not oct_19_points:
                    oct_19_points = points
                    print(f"Set Oct 19 points: {points}")
                elif '20' in full_match and not oct_20_points:
                    oct_20_points = points
                    print(f"Set Oct 20 points: {points}")
        
        # Try to find calendar elements or table structure
        try:
            print("Looking for calendar elements...")
            calendar_elements = await page.query_selector_all('td, .day, .date, [data-date]')
            
            for element in calendar_elements:
                element_text = await element.inner_text()
                element_html = await element.inner_html()
                
                if '19' in element_text or '19' in element_html:
                    print(f"Found element with 19: {element_text}")
                    points_match = re.search(r'(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)', element_text, re.IGNORECASE)
                    if points_match and not oct_19_points:
                        oct_19_points = points_match.group(1).replace(',', '')
                        
                if '20' in element_text or '20' in element_html:
                    print(f"Found element with 20: {element_text}")
                    points_match = re.search(r'(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)', element_text, re.IGNORECASE)
                    if points_match and not oct_20_points:
                        oct_20_points = points_match.group(1).replace(',', '')
                        
        except Exception as e:
            print(f"Error searching calendar elements: {e}")
        
        # Format results - convert raw points to k format
        if oct_19_points:
            oct_19_k = int(oct_19_points) // 1000
            oct_19_display = f"{oct_19_k}k pts"
        else:
            oct_19_display = "Not found"
            
        if oct_20_points:
            oct_20_k = int(oct_20_points) // 1000  
            oct_20_display = f"{oct_20_k}k pts"
        else:
            oct_20_display = "Not found"
        
        result = f"Oct 19: {oct_19_display}, Oct 20: {oct_20_display}"
        
        print(f"\n{'='*50}")
        print(f"FINAL RESULTS: {result}")
        print(f"{'='*50}")
        
        # Save results
        with open('/Users/sahil/reward-seat-tracker/extracted_points.txt', 'w') as f:
            f.write(result)
        
        # Take screenshot for debugging
        await page.screenshot(path='/Users/sahil/reward-seat-tracker/final_screenshot.png')
        
        print("Browser will stay open for 60 seconds for manual verification...")
        await page.wait_for_timeout(60000)
        
        await browser.close()
        
        return result

if __name__ == "__main__":
    result = asyncio.run(extract_upper_class_points())
    print(f"Extracted: {result}")