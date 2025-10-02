"""
Location Service - Handles architectural style detection and 3D surroundings
"""

import requests
import asyncio
from typing import Dict, Any, List, Optional, Tuple
import json
import os
from dotenv import load_dotenv
from ..utils.geocoding import get_coordinates

# Load environment variables
load_dotenv()
from ..utils.architectural_style_detector import ArchitecturalStyleDetector
from ..utils.surroundings_3d import Surroundings3DGenerator

class LocationService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.mapbox_api_key = os.getenv("MAPBOX_API_KEY")
        self.style_detector = ArchitecturalStyleDetector()
        self.surroundings_3d = Surroundings3DGenerator()
        
    async def detect_architectural_style(
        self, address: str, postal_code: str = None
    ) -> Dict[str, Any]:
        """Detect architectural style of the location"""
        try:
            # Get coordinates
            coordinates = await get_coordinates(address)
            if not coordinates:
                raise ValueError("Could not geocode address")
            
            lat, lon = coordinates
            
            # Get street view images for analysis
            street_view_images = await self._get_street_view_images(lat, lon)
            
            # Get nearby buildings data
            nearby_buildings = await self._get_nearby_buildings(lat, lon)
            
            # Analyze architectural style
            style_analysis = await self.style_detector.analyze_architectural_style(
                street_view_images, nearby_buildings, coordinates
            )
            
            # Get historical context
            historical_context = await self._get_historical_context(address, postal_code)
            
            return {
                "primary_style": style_analysis["primary_style"],
                "secondary_styles": style_analysis["secondary_styles"],
                "style_confidence": style_analysis["confidence"],
                "characteristic_elements": style_analysis["characteristic_elements"],
                "historical_context": historical_context,
                "recommended_integration": self._generate_integration_recommendations(style_analysis)
            }
            
        except Exception as e:
            raise Exception(f"Error detecting architectural style: {str(e)}")
    
    async def get_3d_surroundings(
        self, address: str, postal_code: str = None
    ) -> Dict[str, Any]:
        """Get 3D visualization of surrounding area"""
        try:
            # Get coordinates
            coordinates = await get_coordinates(address)
            if not coordinates:
                raise ValueError("Could not geocode address")
            
            lat, lon = coordinates
            
            # Get building data for 3D visualization
            building_data = await self._get_building_data(lat, lon)
            
            # Get terrain data
            terrain_data = await self._get_terrain_data(lat, lon)
            
            # Generate 3D surroundings
            surroundings_3d = await self.surroundings_3d.generate_3d_surroundings(
                coordinates, building_data, terrain_data
            )
            
            return {
                "coordinates": {"lat": lat, "lon": lon},
                "buildings": building_data,
                "terrain": terrain_data,
                "3d_model": surroundings_3d,
                "view_angles": self._calculate_view_angles(lat, lon),
                "context_analysis": await self._analyze_surrounding_context(lat, lon)
            }
            
        except Exception as e:
            raise Exception(f"Error getting 3D surroundings: {str(e)}")
    
    async def _get_street_view_images(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Get street view images from multiple angles"""
        if not self.google_api_key:
            return []
        
        images = []
        headings = [0, 90, 180, 270]  # North, East, South, West
        
        for heading in headings:
            url = "https://maps.googleapis.com/maps/api/streetview"
            params = {
                "location": f"{lat},{lon}",
                "size": "640x640",
                "heading": heading,
                "pitch": 0,
                "key": self.google_api_key
            }
            
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    images.append({
                        "heading": heading,
                        "direction": self._get_direction_name(heading),
                        "image_url": response.url,
                        "image_data": response.content
                    })
            except Exception as e:
                print(f"Error getting street view for heading {heading}: {str(e)}")
        
        return images
    
    async def _get_nearby_buildings(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Get nearby buildings data"""
        if not self.google_api_key:
            return []
        
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lon}",
            "radius": 500,  # 500 meters
            "type": "establishment",
            "key": self.google_api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            buildings = []
            
            for place in data.get("results", []):
                buildings.append({
                    "name": place.get("name", ""),
                    "types": place.get("types", []),
                    "rating": place.get("rating", 0),
                    "vicinity": place.get("vicinity", ""),
                    "geometry": place.get("geometry", {}),
                    "photos": place.get("photos", [])
                })
            
            return buildings
            
        except Exception as e:
            print(f"Error getting nearby buildings: {str(e)}")
            return []
    
    async def _get_historical_context(self, address: str, postal_code: str = None) -> Dict[str, Any]:
        """Get historical context for the location"""
        # This would typically involve querying historical databases
        # For now, we'll return a simulated response
        return {
            "historical_period": "Modern (1950-present)",
            "development_era": "Post-war expansion",
            "architectural_movements": ["Modernism", "Postmodernism"],
            "notable_buildings": [],
            "cultural_significance": "Residential/commercial area"
        }
    
    async def _get_building_data(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Get building data for 3D visualization"""
        # This would typically involve querying building databases or APIs
        # For now, we'll return simulated building data
        buildings = []
        
        # Simulate nearby buildings
        for i in range(10):
            buildings.append({
                "id": f"building_{i}",
                "coordinates": {
                    "lat": lat + (i - 5) * 0.001,
                    "lon": lon + (i - 5) * 0.001
                },
                "height": 10 + (i * 3),
                "type": "residential" if i % 2 == 0 else "commercial",
                "style": "modern" if i % 3 == 0 else "traditional",
                "materials": ["concrete", "glass", "steel"],
                "roof_type": "flat" if i % 2 == 0 else "pitched"
            })
        
        return buildings
    
    async def _get_terrain_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get terrain data for 3D visualization"""
        # This would typically involve querying elevation APIs
        # For now, we'll return simulated terrain data
        return {
            "elevation": 100 + (lat * 10),  # Simulated elevation
            "terrain_type": "urban",
            "slope": 0.05,  # 5% slope
            "drainage": "good",
            "soil_type": "clay",
            "water_features": []
        }
    
    def _calculate_view_angles(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Calculate optimal view angles for 3D visualization"""
        return [
            {"angle": 0, "direction": "North", "description": "Street view"},
            {"angle": 45, "direction": "Northeast", "description": "Corner view"},
            {"angle": 90, "direction": "East", "description": "Side view"},
            {"angle": 135, "direction": "Southeast", "description": "Diagonal view"},
            {"angle": 180, "direction": "South", "description": "Rear view"},
            {"angle": 225, "direction": "Southwest", "description": "Corner view"},
            {"angle": 270, "direction": "West", "description": "Side view"},
            {"angle": 315, "direction": "Northwest", "description": "Diagonal view"}
        ]
    
    async def _analyze_surrounding_context(self, lat: float, lon: float) -> Dict[str, Any]:
        """Analyze surrounding context for design considerations"""
        return {
            "urban_density": "medium",
            "building_heights": "mixed",
            "street_pattern": "grid",
            "green_spaces": "limited",
            "traffic_level": "moderate",
            "noise_level": "medium",
            "accessibility": "good",
            "public_transport": "available"
        }
    
    def _get_direction_name(self, heading: float) -> str:
        """Convert heading to direction name"""
        directions = ["North", "Northeast", "East", "Southeast", 
                     "South", "Southwest", "West", "Northwest"]
        index = int((heading + 22.5) / 45) % 8
        return directions[index]
    
    def _generate_integration_recommendations(self, style_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations for integrating with local architectural style"""
        primary_style = style_analysis.get("primary_style", "Modern")
        confidence = style_analysis.get("confidence", 0.5)
        
        recommendations = {
            "style_integration": "high" if confidence > 0.7 else "medium",
            "suggested_elements": [],
            "material_recommendations": [],
            "color_palette": [],
            "proportion_guidelines": []
        }
        
        if primary_style == "Traditional":
            recommendations["suggested_elements"] = [
                "Pitched roofs", "Traditional windows", "Classical proportions"
            ]
            recommendations["material_recommendations"] = [
                "Brick", "Stone", "Wood", "Traditional masonry"
            ]
            recommendations["color_palette"] = [
                "Earth tones", "Natural materials", "Traditional colors"
            ]
        elif primary_style == "Modern":
            recommendations["suggested_elements"] = [
                "Clean lines", "Large windows", "Open spaces"
            ]
            recommendations["material_recommendations"] = [
                "Concrete", "Glass", "Steel", "Modern composites"
            ]
            recommendations["color_palette"] = [
                "Neutral colors", "White", "Gray", "Accent colors"
            ]
        elif primary_style == "Contemporary":
            recommendations["suggested_elements"] = [
                "Innovative forms", "Sustainable materials", "Technology integration"
            ]
            recommendations["material_recommendations"] = [
                "Recycled materials", "Smart materials", "Sustainable options"
            ]
            recommendations["color_palette"] = [
                "Bold colors", "Natural materials", "High contrast"
            ]
        
        return recommendations
