"""
Architectural Style Detector - AI-powered style analysis
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
import json
import os
from ai_models.style_classifier import StyleClassifier

class ArchitecturalStyleDetector:
    def __init__(self):
        self.style_classifier = StyleClassifier()
        self.style_database = self._load_style_database()
        
    def _load_style_database(self) -> Dict[str, Any]:
        """Load architectural style database"""
        return {
            "Traditional": {
                "characteristics": [
                    "Pitched roofs", "Symmetrical facades", "Classical proportions",
                    "Traditional materials", "Decorative elements"
                ],
                "materials": ["Brick", "Stone", "Wood", "Traditional masonry"],
                "colors": ["Earth tones", "Natural materials", "Traditional colors"],
                "regions": ["Europe", "North America", "Traditional areas"]
            },
            "Modern": {
                "characteristics": [
                    "Clean lines", "Minimal ornamentation", "Large windows",
                    "Open floor plans", "Flat roofs"
                ],
                "materials": ["Concrete", "Glass", "Steel", "Modern composites"],
                "colors": ["White", "Gray", "Black", "Neutral colors"],
                "regions": ["Urban areas", "Contemporary developments"]
            },
            "Contemporary": {
                "characteristics": [
                    "Innovative forms", "Sustainable design", "Technology integration",
                    "Mixed materials", "Dynamic shapes"
                ],
                "materials": ["Recycled materials", "Smart materials", "Sustainable options"],
                "colors": ["Bold colors", "Natural materials", "High contrast"],
                "regions": ["Modern cities", "Innovation districts"]
            },
            "Mediterranean": {
                "characteristics": [
                    "Stucco walls", "Tile roofs", "Arched openings",
                    "Outdoor living", "Warm colors"
                ],
                "materials": ["Stucco", "Tile", "Stone", "Wood"],
                "colors": ["Warm earth tones", "Terracotta", "Cream"],
                "regions": ["Mediterranean", "California", "Similar climates"]
            },
            "Colonial": {
                "characteristics": [
                    "Symmetrical design", "Central entrance", "Classical columns",
                    "Traditional windows", "Formal proportions"
                ],
                "materials": ["Brick", "Wood", "Stone", "Traditional masonry"],
                "colors": ["White", "Traditional colors", "Classical palette"],
                "regions": ["Historical areas", "Traditional neighborhoods"]
            }
        }
    
    async def analyze_architectural_style(
        self, 
        street_view_images: List[Dict[str, Any]], 
        nearby_buildings: List[Dict[str, Any]], 
        coordinates: Tuple[float, float]
    ) -> Dict[str, Any]:
        """Analyze architectural style from images and building data"""
        
        # Analyze street view images
        image_analysis = await self._analyze_street_view_images(street_view_images)
        
        # Analyze nearby buildings
        building_analysis = await self._analyze_nearby_buildings(nearby_buildings)
        
        # Get regional context
        regional_context = await self._get_regional_context(coordinates)
        
        # Combine analyses
        combined_analysis = self._combine_analyses(
            image_analysis, building_analysis, regional_context
        )
        
        return combined_analysis
    
    async def _analyze_street_view_images(self, images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze architectural style from street view images"""
        if not images:
            return {"primary_style": "Unknown", "confidence": 0.0}
        
        style_scores = {}
        total_confidence = 0
        
        for image_data in images:
            # Extract features from image
            features = await self._extract_architectural_features(image_data)
            
            # Classify style
            style_prediction = await self.style_classifier.classify_style(features)
            
            # Accumulate scores
            for style, confidence in style_prediction.items():
                if style not in style_scores:
                    style_scores[style] = 0
                style_scores[style] += confidence
                total_confidence += confidence
        
        # Normalize scores
        if total_confidence > 0:
            for style in style_scores:
                style_scores[style] /= total_confidence
        
        # Find primary style
        primary_style = max(style_scores.items(), key=lambda x: x[1])
        
        return {
            "primary_style": primary_style[0],
            "style_scores": style_scores,
            "confidence": primary_style[1],
            "characteristic_elements": self._identify_characteristic_elements(style_scores)
        }
    
    async def _analyze_nearby_buildings(self, buildings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze architectural style from nearby buildings data"""
        if not buildings:
            return {"primary_style": "Unknown", "confidence": 0.0}
        
        style_counts = {}
        total_buildings = len(buildings)
        
        for building in buildings:
            # Analyze building type and characteristics
            building_style = await self._classify_building_style(building)
            
            if building_style in style_counts:
                style_counts[building_style] += 1
            else:
                style_counts[building_style] = 1
        
        # Calculate style percentages
        style_percentages = {
            style: count / total_buildings 
            for style, count in style_counts.items()
        }
        
        # Find dominant style
        dominant_style = max(style_percentages.items(), key=lambda x: x[1])
        
        return {
            "primary_style": dominant_style[0],
            "style_distribution": style_percentages,
            "confidence": dominant_style[1],
            "building_count": total_buildings
        }
    
    async def _get_regional_context(self, coordinates: Tuple[float, float]) -> Dict[str, Any]:
        """Get regional architectural context"""
        lat, lon = coordinates
        
        # Determine region based on coordinates
        if 25 <= lat <= 50 and -125 <= lon <= -65:  # North America
            region = "North America"
            common_styles = ["Traditional", "Modern", "Colonial"]
        elif 35 <= lat <= 70 and -10 <= lon <= 40:  # Europe
            region = "Europe"
            common_styles = ["Traditional", "Mediterranean", "Modern"]
        elif -35 <= lat <= 35 and 100 <= lon <= 180:  # Asia-Pacific
            region = "Asia-Pacific"
            common_styles = ["Traditional", "Modern", "Contemporary"]
        else:
            region = "Other"
            common_styles = ["Modern", "Contemporary", "Traditional"]
        
        return {
            "region": region,
            "common_styles": common_styles,
            "cultural_influences": self._get_cultural_influences(region)
        }
    
    def _combine_analyses(
        self, 
        image_analysis: Dict[str, Any], 
        building_analysis: Dict[str, Any], 
        regional_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine different analyses to determine final architectural style"""
        
        # Weight different analyses
        image_weight = 0.4
        building_weight = 0.4
        regional_weight = 0.2
        
        # Combine style scores
        combined_scores = {}
        
        # Add image analysis scores
        if "style_scores" in image_analysis:
            for style, score in image_analysis["style_scores"].items():
                combined_scores[style] = score * image_weight
        
        # Add building analysis scores
        if "style_distribution" in building_analysis:
            for style, score in building_analysis["style_distribution"].items():
                if style in combined_scores:
                    combined_scores[style] += score * building_weight
                else:
                    combined_scores[style] = score * building_weight
        
        # Add regional context
        for style in regional_context["common_styles"]:
            if style in combined_scores:
                combined_scores[style] += 0.1 * regional_weight
            else:
                combined_scores[style] = 0.1 * regional_weight
        
        # Find primary and secondary styles
        sorted_styles = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_style = sorted_styles[0][0] if sorted_styles else "Unknown"
        secondary_styles = [style for style, _ in sorted_styles[1:3]]
        
        # Calculate confidence
        total_score = sum(combined_scores.values())
        confidence = combined_scores.get(primary_style, 0) / total_score if total_score > 0 else 0
        
        return {
            "primary_style": primary_style,
            "secondary_styles": secondary_styles,
            "confidence": confidence,
            "style_scores": combined_scores,
            "characteristic_elements": self._get_characteristic_elements(primary_style),
            "regional_context": regional_context
        }
    
    async def _extract_architectural_features(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract architectural features from image"""
        # This would typically involve computer vision analysis
        # For now, we'll return simulated features
        return {
            "roof_type": "pitched",
            "window_style": "traditional",
            "material_texture": "brick",
            "symmetry": "high",
            "ornamentation": "moderate",
            "proportions": "classical"
        }
    
    async def _classify_building_style(self, building: Dict[str, Any]) -> str:
        """Classify building style based on building data"""
        # This would typically involve analyzing building characteristics
        # For now, we'll return a simulated classification
        building_types = building.get("types", [])
        
        if "church" in building_types or "place_of_worship" in building_types:
            return "Traditional"
        elif "shopping_mall" in building_types or "store" in building_types:
            return "Modern"
        elif "hospital" in building_types or "school" in building_types:
            return "Contemporary"
        else:
            return "Modern"  # Default
    
    def _identify_characteristic_elements(self, style_scores: Dict[str, float]) -> List[str]:
        """Identify characteristic elements based on style scores"""
        elements = []
        
        for style, score in style_scores.items():
            if score > 0.3:  # Threshold for significant presence
                style_info = self.style_database.get(style, {})
                elements.extend(style_info.get("characteristics", []))
        
        return list(set(elements))  # Remove duplicates
    
    def _get_characteristic_elements(self, primary_style: str) -> List[str]:
        """Get characteristic elements for a specific style"""
        style_info = self.style_database.get(primary_style, {})
        return style_info.get("characteristics", [])
    
    def _get_cultural_influences(self, region: str) -> List[str]:
        """Get cultural influences for a region"""
        cultural_map = {
            "North America": ["European", "Indigenous", "Modern American"],
            "Europe": ["Classical", "Medieval", "Renaissance", "Modern"],
            "Asia-Pacific": ["Traditional Asian", "Colonial", "Modern"],
            "Other": ["Global", "Modern", "Contemporary"]
        }
        
        return cultural_map.get(region, ["Global", "Modern"])
