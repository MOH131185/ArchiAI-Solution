"""
Geocoding utilities for address to coordinates conversion
"""

import requests
import asyncio
from typing import Tuple, Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeocodingService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.nominatim_base_url = "https://nominatim.openstreetmap.org"
    
    async def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get coordinates from address using multiple geocoding services"""
        try:
            # Try Google Maps first
            if self.google_api_key:
                coords = await self._get_google_coordinates(address)
                if coords:
                    return coords
            
            # Fallback to OpenStreetMap Nominatim
            coords = await self._get_nominatim_coordinates(address)
            return coords
            
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return None
    
    async def _get_google_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get coordinates using Google Maps API"""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.google_api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return (location["lat"], location["lng"])
        
        return None
    
    async def _get_nominatim_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get coordinates using OpenStreetMap Nominatim"""
        url = f"{self.nominatim_base_url}/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        
        headers = {
            "User-Agent": "ArchiAI-Solution/1.0"
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            return (float(data[0]["lat"]), float(data[0]["lon"]))
        
        return None

# Global instance
geocoding_service = GeocodingService()

async def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """Get coordinates for an address"""
    return await geocoding_service.get_coordinates(address)
