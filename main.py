#!/usr/bin/env python3
"""
Reward Seat Flights Tracker
Main application entry point
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Reward Seat Tracker", version="1.0.0")

class FlightSearch(BaseModel):
    origin: str
    destination: str
    month: int
    year: int
    airline: str = "virgin_atlantic"

class FlightResult(BaseModel):
    date: str
    availability: bool
    price: str
    booking_class: str
    timestamp: datetime

class RewardSeatTracker:
    def __init__(self):
        self.browser = None
        self.page = None
        
    async def start_browser(self):
        """Initialize Playwright browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        
    async def close_browser(self):
        """Close browser and cleanup"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
            
    async def search_virgin_atlantic(self, search: FlightSearch) -> List[FlightResult]:
        """Search Virgin Atlantic for reward seats"""
        url = f"https://www.virginatlantic.com/reward-flight-finder/results/month?origin={search.origin}&destination={search.destination}&month={search.month}&year={search.year}"
        
        try:
            await self.page.goto(url, wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Wait for results to load
            await self.page.wait_for_selector(".flight-result", timeout=10000)
            
            # Extract flight data
            flights = await self.page.query_selector_all(".flight-result")
            results = []
            
            for flight in flights:
                date_elem = await flight.query_selector(".date")
                price_elem = await flight.query_selector(".price")
                availability_elem = await flight.query_selector(".availability")
                
                if date_elem and price_elem:
                    date = await date_elem.inner_text()
                    price = await price_elem.inner_text()
                    availability = availability_elem is not None
                    
                    results.append(FlightResult(
                        date=date.strip(),
                        availability=availability,
                        price=price.strip(),
                        booking_class="economy",
                        timestamp=datetime.now()
                    ))
                    
            return results
            
        except Exception as e:
            logger.error(f"Error searching Virgin Atlantic: {e}")
            return []

# Global tracker instance
tracker = RewardSeatTracker()

@app.on_event("startup")
async def startup_event():
    """Initialize browser on startup"""
    await tracker.start_browser()
    
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await tracker.close_browser()

@app.post("/search", response_model=List[FlightResult])
async def search_flights(search: FlightSearch):
    """Search for reward seats"""
    if search.airline == "virgin_atlantic":
        return await tracker.search_virgin_atlantic(search)
    else:
        return []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Reward Seat Tracker API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)