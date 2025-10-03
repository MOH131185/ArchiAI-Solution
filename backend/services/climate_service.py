"""
Climate Service - Handles climate and weather data analysis
"""

import requests
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import os
from utils.geocoding import get_coordinates
from utils.climate_analysis import analyze_climate_patterns

class ClimateService:
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.climate_api_key = os.getenv("CLIMATE_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    async def get_climate_data(self, address: str) -> Dict[str, Any]:
        """Get comprehensive climate data for a location"""
        try:
            # Get coordinates from address
            coordinates = await get_coordinates(address)
            if not coordinates:
                raise ValueError("Could not geocode address")
            
            lat, lon = coordinates
            
            # Get current weather
            current_weather = await self._get_current_weather(lat, lon)
            
            # Get historical climate data
            historical_data = await self._get_historical_climate(lat, lon)
            
            # Get seasonal patterns
            seasonal_patterns = await self._get_seasonal_patterns(lat, lon)
            
            # Analyze climate for architectural recommendations
            climate_analysis = analyze_climate_patterns(
                current_weather, historical_data, seasonal_patterns
            )
            
            return {
                "coordinates": {"lat": lat, "lon": lon},
                "current_weather": current_weather,
                "historical_data": historical_data,
                "seasonal_patterns": seasonal_patterns,
                "climate_analysis": climate_analysis,
                "architectural_recommendations": self._generate_architectural_recommendations(climate_analysis)
            }
            
        except Exception as e:
            raise Exception(f"Error getting climate data: {str(e)}")
    
    async def _get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get current weather data"""
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.openweather_api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"].get("deg", 0),
            "weather_description": data["weather"][0]["description"],
            "cloudiness": data["clouds"]["all"],
            "visibility": data.get("visibility", 0) / 1000,  # Convert to km
            "uv_index": data.get("uvi", 0)
        }
    
    async def _get_historical_climate(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get historical climate data for the past 5 years"""
        # Get data for the past 5 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 5)
        
        historical_data = {
            "temperature_ranges": [],
            "precipitation_data": [],
            "humidity_data": [],
            "wind_data": [],
            "solar_irradiance": []
        }
        
        # This would typically involve multiple API calls to get historical data
        # For now, we'll simulate with current data patterns
        current_weather = await self._get_current_weather(lat, lon)
        
        # Simulate historical patterns based on current data
        historical_data["temperature_ranges"] = self._simulate_temperature_ranges(current_weather["temperature"])
        historical_data["precipitation_data"] = self._simulate_precipitation_data()
        historical_data["humidity_data"] = self._simulate_humidity_data(current_weather["humidity"])
        historical_data["wind_data"] = self._simulate_wind_data(current_weather["wind_speed"])
        historical_data["solar_irradiance"] = self._simulate_solar_data(lat)
        
        return historical_data
    
    async def _get_seasonal_patterns(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get seasonal climate patterns"""
        # Get 5-day forecast for seasonal analysis
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.openweather_api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        forecast_data = response.json()
        
        # Analyze seasonal patterns
        seasonal_patterns = {
            "spring": self._analyze_season("spring", lat),
            "summer": self._analyze_season("summer", lat),
            "autumn": self._analyze_season("autumn", lat),
            "winter": self._analyze_season("winter", lat)
        }
        
        return seasonal_patterns
    
    def _generate_architectural_recommendations(self, climate_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate architectural recommendations based on climate analysis"""
        recommendations = {
            "thermal_comfort": [],
            "energy_efficiency": [],
            "ventilation": [],
            "insulation": [],
            "orientation": [],
            "materials": []
        }
        
        # Temperature-based recommendations
        avg_temp = climate_analysis.get("average_temperature", 20)
        temp_range = climate_analysis.get("temperature_range", 10)
        
        if avg_temp > 25:
            recommendations["thermal_comfort"].append("Implement passive cooling strategies")
            recommendations["ventilation"].append("Design for cross-ventilation")
            recommendations["materials"].append("Use reflective and light-colored materials")
        elif avg_temp < 10:
            recommendations["thermal_comfort"].append("Implement passive heating strategies")
            recommendations["insulation"].append("High-performance insulation required")
            recommendations["materials"].append("Use thermal mass materials")
        
        # Humidity-based recommendations
        humidity = climate_analysis.get("average_humidity", 50)
        if humidity > 70:
            recommendations["ventilation"].append("Enhanced ventilation for humidity control")
            recommendations["materials"].append("Use moisture-resistant materials")
        
        # Wind-based recommendations
        wind_speed = climate_analysis.get("average_wind_speed", 5)
        if wind_speed > 10:
            recommendations["orientation"].append("Design windbreaks and sheltered areas")
        
        # Solar-based recommendations
        solar_irradiance = climate_analysis.get("solar_irradiance", 1000)
        if solar_irradiance > 1500:
            recommendations["energy_efficiency"].append("Implement solar energy systems")
            recommendations["orientation"].append("Optimize building orientation for solar gain")
        
        return recommendations
    
    def _simulate_temperature_ranges(self, current_temp: float) -> List[Dict[str, Any]]:
        """Simulate temperature ranges based on current temperature"""
        return [
            {"month": "Jan", "min": current_temp - 15, "max": current_temp - 5, "avg": current_temp - 10},
            {"month": "Feb", "min": current_temp - 12, "max": current_temp - 2, "avg": current_temp - 7},
            {"month": "Mar", "min": current_temp - 8, "max": current_temp + 2, "avg": current_temp - 3},
            {"month": "Apr", "min": current_temp - 3, "max": current_temp + 7, "avg": current_temp + 2},
            {"month": "May", "min": current_temp + 2, "max": current_temp + 12, "avg": current_temp + 7},
            {"month": "Jun", "min": current_temp + 5, "max": current_temp + 15, "avg": current_temp + 10},
            {"month": "Jul", "min": current_temp + 7, "max": current_temp + 17, "avg": current_temp + 12},
            {"month": "Aug", "min": current_temp + 6, "max": current_temp + 16, "avg": current_temp + 11},
            {"month": "Sep", "min": current_temp + 3, "max": current_temp + 13, "avg": current_temp + 8},
            {"month": "Oct", "min": current_temp - 1, "max": current_temp + 9, "avg": current_temp + 4},
            {"month": "Nov", "min": current_temp - 6, "max": current_temp + 4, "avg": current_temp - 1},
            {"month": "Dec", "min": current_temp - 12, "max": current_temp - 2, "avg": current_temp - 7}
        ]
    
    def _simulate_precipitation_data(self) -> List[Dict[str, Any]]:
        """Simulate precipitation data"""
        return [
            {"month": "Jan", "precipitation": 50, "rainy_days": 8},
            {"month": "Feb", "precipitation": 45, "rainy_days": 7},
            {"month": "Mar", "precipitation": 60, "rainy_days": 9},
            {"month": "Apr", "precipitation": 70, "rainy_days": 10},
            {"month": "May", "precipitation": 80, "rainy_days": 12},
            {"month": "Jun", "precipitation": 90, "rainy_days": 13},
            {"month": "Jul", "precipitation": 85, "rainy_days": 12},
            {"month": "Aug", "precipitation": 75, "rainy_days": 11},
            {"month": "Sep", "precipitation": 65, "rainy_days": 10},
            {"month": "Oct", "precipitation": 55, "rainy_days": 9},
            {"month": "Nov", "precipitation": 50, "rainy_days": 8},
            {"month": "Dec", "precipitation": 45, "rainy_days": 7}
        ]
    
    def _simulate_humidity_data(self, current_humidity: float) -> List[Dict[str, Any]]:
        """Simulate humidity data"""
        return [
            {"month": "Jan", "humidity": current_humidity + 10},
            {"month": "Feb", "humidity": current_humidity + 8},
            {"month": "Mar", "humidity": current_humidity + 5},
            {"month": "Apr", "humidity": current_humidity + 2},
            {"month": "May", "humidity": current_humidity - 2},
            {"month": "Jun", "humidity": current_humidity - 5},
            {"month": "Jul", "humidity": current_humidity - 8},
            {"month": "Aug", "humidity": current_humidity - 6},
            {"month": "Sep", "humidity": current_humidity - 3},
            {"month": "Oct", "humidity": current_humidity + 1},
            {"month": "Nov", "humidity": current_humidity + 5},
            {"month": "Dec", "humidity": current_humidity + 8}
        ]
    
    def _simulate_wind_data(self, current_wind: float) -> List[Dict[str, Any]]:
        """Simulate wind data"""
        return [
            {"month": "Jan", "wind_speed": current_wind + 2, "wind_direction": "NW"},
            {"month": "Feb", "wind_speed": current_wind + 1, "wind_direction": "N"},
            {"month": "Mar", "wind_speed": current_wind, "wind_direction": "NE"},
            {"month": "Apr", "wind_speed": current_wind - 1, "wind_direction": "E"},
            {"month": "May", "wind_speed": current_wind - 2, "wind_direction": "SE"},
            {"month": "Jun", "wind_speed": current_wind - 1, "wind_direction": "S"},
            {"month": "Jul", "wind_speed": current_wind, "wind_direction": "SW"},
            {"month": "Aug", "wind_speed": current_wind + 1, "wind_direction": "W"},
            {"month": "Sep", "wind_speed": current_wind + 2, "wind_direction": "NW"},
            {"month": "Oct", "wind_speed": current_wind + 1, "wind_direction": "N"},
            {"month": "Nov", "wind_speed": current_wind, "wind_direction": "NE"},
            {"month": "Dec", "wind_speed": current_wind + 1, "wind_direction": "E"}
        ]
    
    def _simulate_solar_data(self, latitude: float) -> List[Dict[str, Any]]:
        """Simulate solar irradiance data based on latitude"""
        # Solar irradiance varies with latitude and season
        base_irradiance = max(0, 1000 - abs(latitude) * 10)
        
        return [
            {"month": "Jan", "solar_irradiance": base_irradiance * 0.6},
            {"month": "Feb", "solar_irradiance": base_irradiance * 0.7},
            {"month": "Mar", "solar_irradiance": base_irradiance * 0.8},
            {"month": "Apr", "solar_irradiance": base_irradiance * 0.9},
            {"month": "May", "solar_irradiance": base_irradiance * 1.0},
            {"month": "Jun", "solar_irradiance": base_irradiance * 1.1},
            {"month": "Jul", "solar_irradiance": base_irradiance * 1.0},
            {"month": "Aug", "solar_irradiance": base_irradiance * 0.9},
            {"month": "Sep", "solar_irradiance": base_irradiance * 0.8},
            {"month": "Oct", "solar_irradiance": base_irradiance * 0.7},
            {"month": "Nov", "solar_irradiance": base_irradiance * 0.6},
            {"month": "Dec", "solar_irradiance": base_irradiance * 0.5}
        ]
    
    def _analyze_season(self, season: str, latitude: float) -> Dict[str, Any]:
        """Analyze climate patterns for a specific season"""
        seasonal_data = {
            "spring": {"temp_range": (5, 20), "humidity": 60, "precipitation": 70},
            "summer": {"temp_range": (15, 30), "humidity": 70, "precipitation": 50},
            "autumn": {"temp_range": (5, 20), "humidity": 65, "precipitation": 80},
            "winter": {"temp_range": (-5, 10), "humidity": 75, "precipitation": 60}
        }
        
        return seasonal_data.get(season, {})
