#!/usr/bin/env python3
"""
Simple script to navigate to Virgin Atlantic reward flights page
"""

import asyncio
from playwright.async_api import async_playwright

async def navigate_to_virgin_atlantic():
    """Navigate to Virgin Atlantic reward flights page"""
    url = "https://www.virginatlantic.com/reward-flight-finder/results/month?origin=LHR&destination=BLR&month=10&year=2025"
    
    async with async_playwright() as p:
        # Launch browser in non-headless mode so you can see it
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print(f"Navigating to: {url}")
        await page.goto(url)
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        
        # Handle cookie consent - look for "Reject All" button
        try:
            print("Checking for cookie consent dialog...")
            # Common selectors for cookie rejection buttons
            reject_selectors = [
                'button:has-text("Reject All")',
                'button:has-text("Reject all")',
                'button:has-text("Decline All")',
                '[data-testid="reject-all"]',
                '.reject-all',
                '#reject-all'
            ]
            
            for selector in reject_selectors:
                try:
                    reject_button = await page.wait_for_selector(selector, timeout=3000)
                    if reject_button:
                        print(f"Found reject button with selector: {selector}")
                        await reject_button.click()
                        print("Clicked 'Reject All' button")
                        await page.wait_for_timeout(2000)  # Wait for dialog to close
                        break
                except:
                    continue
            else:
                print("No cookie consent dialog found or already handled")
                
        except Exception as e:
            print(f"Cookie consent handling: {e}")
        
        print("Page loaded successfully!")
        
        # Extract Upper Class points for specific dates
        try:
            print("Extracting Upper Class points for Oct 19 and Oct 20...")
            
            # Wait for flight results to load
            await page.wait_for_selector('[data-testid="flight-result"], .flight-result, .calendar-day', timeout=10000)
            await page.wait_for_timeout(3000)  # Additional wait for content
            
            # Look for October 19 and 20 specific dates
            target_dates = {
                "19": None,  # Oct 19
                "20": None   # Oct 20
            }
            
            # Try different selectors to find calendar/flight data
            selectors_to_try = [
                '[data-date*="19"], [data-date*="20"]',
                '.calendar-day:has-text("19"), .calendar-day:has-text("20")',
                '.flight-result:has-text("19"), .flight-result:has-text("20")',
                '[data-testid*="19"], [data-testid*="20"]'
            ]
            
            for selector in selectors_to_try:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"Found elements with selector: {selector}")
                        break
                except:
                    continue
            
            # If no specific selectors work, get all text content and search
            page_content = await page.content()
            
            # Look for patterns like "19" or "20" followed by points
            import re
            
            # Pattern to match Upper Class points
            patterns = [
                r'(?:Oct(?:ober)?\s*)?(?:Sun(?:day)?\s*)?19(?:th)?.*?Upper\s*Class.*?(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)',
                r'(?:Oct(?:ober)?\s*)?(?:Mon(?:day)?\s*)?20(?:th)?.*?Upper\s*Class.*?(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)',
                r'Upper\s*Class.*?(?:Oct(?:ober)?\s*)?(?:Sun(?:day)?\s*)?19(?:th)?.*?(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)',
                r'Upper\s*Class.*?(?:Oct(?:ober)?\s*)?(?:Mon(?:day)?\s*)?20(?:th)?.*?(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)'
            ]
            
            oct_19_points = None
            oct_20_points = None
            
            for pattern in patterns:
                matches = re.finditer(pattern, page_content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    points = match.group(1).replace(',', '')
                    if '19' in match.group(0):
                        oct_19_points = points
                    elif '20' in match.group(0):
                        oct_20_points = points
            
            # Alternative: Look for calendar grid or table structure
            if not oct_19_points or not oct_20_points:
                print("Trying alternative extraction method...")
                
                # Look for table cells or calendar days
                day_elements = await page.query_selector_all('.calendar-day, .day, [data-day], .flight-day')
                
                for element in day_elements:
                    text = await element.inner_text()
                    if '19' in text and 'Upper' in text:
                        points_match = re.search(r'(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)', text, re.IGNORECASE)
                        if points_match:
                            oct_19_points = points_match.group(1).replace(',', '')
                    elif '20' in text and 'Upper' in text:
                        points_match = re.search(r'(\d+(?:,\d{3})*)\s*(?:k|K)?\s*(?:pts|points)', text, re.IGNORECASE)
                        if points_match:
                            oct_20_points = points_match.group(1).replace(',', '')
            
            # Format and display results
            oct_19_display = f"{oct_19_points}k pts" if oct_19_points else "Not found"
            oct_20_display = f"{oct_20_points}k pts" if oct_20_points else "Not found"
            
            result = f"Oct 19: {oct_19_display}, Oct 20: {oct_20_display}"
            print(f"\nEXTRACTED RESULTS: {result}")
            
            # Also save to file
            with open('/Users/sahil/reward-seat-tracker/extracted_points.txt', 'w') as f:
                f.write(result)
            
        except Exception as e:
            print(f"Error extracting points: {e}")
            print("Taking screenshot for debugging...")
            await page.screenshot(path='/Users/sahil/reward-seat-tracker/debug_screenshot.png')
        
        print("Browser will stay open for 30 seconds for manual inspection...")
        await page.wait_for_timeout(30000)  # 30 seconds
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(navigate_to_virgin_atlantic())