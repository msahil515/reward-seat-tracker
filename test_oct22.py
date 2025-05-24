import asyncio
import re
from playwright.async_api import async_playwright

async def extract_oct22_points():
    """Test extraction for Oct 22 specifically"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://www.virginatlantic.com/reward-flight-finder/results/month?origin=LHR&destination=BLR&month=10&year=2025"
        print(f"Navigating to: {url}")
        
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        
        # Handle cookie consent
        try:
            reject_button = await page.wait_for_selector('button:has-text("Reject All")', timeout=5000)
            if reject_button:
                await reject_button.click()
                print("Clicked 'Reject All' button")
                await page.wait_for_timeout(2000)
        except:
            print("No cookie consent found or already handled")
        
        await page.wait_for_timeout(3000)
        
        print("Extracting Oct 22 Upper Class points...")
        
        # Get page text
        page_text = await page.inner_text('body')
        
        # Specific patterns for Oct 22
        patterns = [
            r'(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+22\s+.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
            r'22\s+Economy.*?Upper\s+Class\s+(\d+(?:,\d{3})*)\s*pts',
        ]
        
        oct_22_points = None
        
        for i, pattern in enumerate(patterns):
            matches = re.finditer(pattern, page_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                points = match.group(1).replace(',', '')
                full_match = match.group(0)
                
                print(f"Pattern {i+1} found: {full_match.strip()}")
                
                if '22' in full_match and not oct_22_points:
                    oct_22_points = points
                    print(f"Set Oct 22 points: {points}")
        
        # Format result
        if oct_22_points:
            oct_22_k = int(oct_22_points) // 1000
            result = f"Oct 22: {oct_22_k}k pts"
        else:
            result = "Oct 22: Not found"
        
        print(f"\n{'='*50}")
        print(f"FINAL RESULT: {result}")
        print(f"{'='*50}")
        
        # Save result
        with open('/Users/sahil/reward-seat-tracker/test_oct22_result.txt', 'w') as f:
            f.write(result)
        
        print("Browser will stay open for 30 seconds for verification...")
        await page.wait_for_timeout(30000)
        
        await browser.close()
        return result

if __name__ == "__main__":
    result = asyncio.run(extract_oct22_points())
    print(f"Extracted: {result}")