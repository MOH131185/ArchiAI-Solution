"""
Style Classifier - AI model for architectural style classification
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from typing import Dict, Any, List
import json
import os

class StyleClassifier(nn.Module):
    def __init__(self, num_classes: int = 5):
        super(StyleClassifier, self).__init__()
        
        # Convolutional layers for feature extraction
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
        
        # Style classes
        self.style_classes = [
            "Traditional", "Modern", "Contemporary", "Mediterranean", "Colonial"
        ]
        
        # Initialize weights
        self._initialize_weights()
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)
    
    async def classify_style(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Classify architectural style from features"""
        # Convert features to tensor
        feature_vector = self._extract_feature_vector(features)
        
        # Make prediction
        with torch.no_grad():
            output = self.forward(feature_vector)
            probabilities = torch.softmax(output, dim=1)
        
        # Convert to dictionary
        style_scores = {}
        for i, style in enumerate(self.style_classes):
            style_scores[style] = probabilities[0][i].item()
        
        return style_scores
    
    def _extract_feature_vector(self, features: Dict[str, Any]) -> torch.Tensor:
        """Extract feature vector from architectural features"""
        # Convert features to numerical values
        feature_values = []
        
        # Roof type
        roof_type = features.get("roof_type", "flat")
        roof_encoding = self._encode_roof_type(roof_type)
        feature_values.extend(roof_encoding)
        
        # Window style
        window_style = features.get("window_style", "modern")
        window_encoding = self._encode_window_style(window_style)
        feature_values.extend(window_encoding)
        
        # Material texture
        material_texture = features.get("material_texture", "concrete")
        material_encoding = self._encode_material_texture(material_texture)
        feature_values.extend(material_encoding)
        
        # Symmetry
        symmetry = features.get("symmetry", "medium")
        symmetry_encoding = self._encode_symmetry(symmetry)
        feature_values.extend(symmetry_encoding)
        
        # Ornamentation
        ornamentation = features.get("ornamentation", "minimal")
        ornamentation_encoding = self._encode_ornamentation(ornamentation)
        feature_values.extend(ornamentation_encoding)
        
        # Proportions
        proportions = features.get("proportions", "modern")
        proportions_encoding = self._encode_proportions(proportions)
        feature_values.extend(proportions_encoding)
        
        # Convert to tensor and add batch dimension
        feature_tensor = torch.tensor(feature_values, dtype=torch.float32).unsqueeze(0)
        
        # Reshape to match expected input size (3, 224, 224)
        # This is a simplified approach - in practice, you'd use actual image data
        feature_tensor = feature_tensor.unsqueeze(0).repeat(1, 3, 224, 224)
        
        return feature_tensor
    
    def _encode_roof_type(self, roof_type: str) -> List[float]:
        """Encode roof type as one-hot vector"""
        roof_types = ["flat", "pitched", "gabled", "domed", "sawtooth"]
        encoding = [0.0] * len(roof_types)
        if roof_type in roof_types:
            encoding[roof_types.index(roof_type)] = 1.0
        return encoding
    
    def _encode_window_style(self, window_style: str) -> List[float]:
        """Encode window style as one-hot vector"""
        window_styles = ["traditional", "modern", "large", "strip", "curtain_wall"]
        encoding = [0.0] * len(window_styles)
        if window_style in window_styles:
            encoding[window_styles.index(window_style)] = 1.0
        return encoding
    
    def _encode_material_texture(self, material_texture: str) -> List[float]:
        """Encode material texture as one-hot vector"""
        materials = ["brick", "concrete", "glass", "steel", "wood", "stucco"]
        encoding = [0.0] * len(materials)
        if material_texture in materials:
            encoding[materials.index(material_texture)] = 1.0
        return encoding
    
    def _encode_symmetry(self, symmetry: str) -> List[float]:
        """Encode symmetry level"""
        symmetry_levels = {"low": 0.0, "medium": 0.5, "high": 1.0}
        return [symmetry_levels.get(symmetry, 0.5)]
    
    def _encode_ornamentation(self, ornamentation: str) -> List[float]:
        """Encode ornamentation level"""
        ornamentation_levels = {"minimal": 0.0, "moderate": 0.5, "high": 1.0}
        return [ornamentation_levels.get(ornamentation, 0.5)]
    
    def _encode_proportions(self, proportions: str) -> List[float]:
        """Encode proportion style"""
        proportion_styles = ["classical", "modern", "contemporary"]
        encoding = [0.0] * len(proportion_styles)
        if proportions in proportion_styles:
            encoding[proportion_styles.index(proportions)] = 1.0
        return encoding

class DesignGenerator:
    def __init__(self):
        self.style_classifier = StyleClassifier()
        self.design_templates = self._load_design_templates()
        
    def _load_design_templates(self) -> Dict[str, Any]:
        """Load design templates for different project types"""
        return {
            "residential": {
                "house": {
                    "rooms": ["living_room", "kitchen", "bedroom", "bathroom"],
                    "layout": "open_plan",
                    "features": ["garage", "garden", "balcony"]
                },
                "apartment": {
                    "rooms": ["living_room", "kitchen", "bedroom", "bathroom"],
                    "layout": "compact",
                    "features": ["balcony", "storage"]
                }
            },
            "commercial": {
                "office": {
                    "rooms": ["reception", "office", "meeting_room", "break_room"],
                    "layout": "open_plan",
                    "features": ["elevator", "parking", "lobby"]
                },
                "retail": {
                    "rooms": ["showroom", "storage", "office", "restroom"],
                    "layout": "open_plan",
                    "features": ["display_windows", "storage", "parking"]
                }
            },
            "institutional": {
                "hospital": {
                    "rooms": ["reception", "patient_room", "surgery", "lab"],
                    "layout": "functional",
                    "features": ["elevator", "parking", "emergency_access"]
                },
                "school": {
                    "rooms": ["classroom", "office", "library", "gym"],
                    "layout": "corridor",
                    "features": ["playground", "parking", "auditorium"]
                }
            }
        }
    
    async def generate_2d_design(
        self, 
        project_requirements: Dict[str, Any],
        climate_data: Dict[str, Any],
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 2D architectural design"""
        
        # Determine project type and requirements
        project_type = project_requirements.get("type", "residential")
        surface_area = project_requirements.get("surface_area", 100)
        
        # Get design template
        template = self.design_templates.get(project_type, {})
        
        # Generate floor plan
        floor_plan = await self._generate_floor_plan(
            template, surface_area, climate_data, architectural_style
        )
        
        # Generate elevations
        elevations = await self._generate_elevations(
            floor_plan, architectural_style, climate_data
        )
        
        # Generate sections
        sections = await self._generate_sections(floor_plan, architectural_style)
        
        return {
            "floor_plan": floor_plan,
            "elevations": elevations,
            "sections": sections,
            "design_parameters": {
                "project_type": project_type,
                "surface_area": surface_area,
                "style": architectural_style.get("primary_style", "Modern"),
                "climate_considerations": climate_data.get("architectural_recommendations", {})
            }
        }
    
    async def generate_3d_design(
        self, 
        project_requirements: Dict[str, Any],
        climate_data: Dict[str, Any],
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 3D architectural design"""
        
        # Generate 3D model
        model_3d = await self._generate_3d_model(
            project_requirements, climate_data, architectural_style
        )
        
        # Generate materials and textures
        materials = await self._generate_materials(architectural_style, climate_data)
        
        # Generate lighting
        lighting = await self._generate_lighting(climate_data, architectural_style)
        
        # Generate landscaping
        landscaping = await self._generate_landscaping(climate_data, architectural_style)
        
        return {
            "model_3d": model_3d,
            "materials": materials,
            "lighting": lighting,
            "landscaping": landscaping,
            "viewpoints": await self._generate_viewpoints(project_requirements)
        }
    
    async def _generate_floor_plan(
        self, 
        template: Dict[str, Any], 
        surface_area: float, 
        climate_data: Dict[str, Any],
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate floor plan"""
        
        # Calculate room sizes based on surface area
        room_sizes = self._calculate_room_sizes(template, surface_area)
        
        # Generate room layout
        layout = await self._generate_room_layout(room_sizes, architectural_style)
        
        # Add climate considerations
        climate_layout = await self._apply_climate_considerations(layout, climate_data)
        
        # Add style elements
        styled_layout = await self._apply_style_elements(climate_layout, architectural_style)
        
        return {
            "rooms": styled_layout,
            "dimensions": room_sizes,
            "circulation": await self._generate_circulation(styled_layout),
            "openings": await self._generate_openings(styled_layout, climate_data)
        }
    
    def _calculate_room_sizes(self, template: Dict[str, Any], surface_area: float) -> Dict[str, float]:
        """Calculate room sizes based on template and surface area"""
        rooms = template.get("rooms", [])
        total_rooms = len(rooms)
        
        if total_rooms == 0:
            return {}
        
        # Allocate surface area to rooms
        base_area = surface_area / total_rooms
        
        room_sizes = {}
        for room in rooms:
            # Adjust size based on room type
            if room in ["living_room", "kitchen"]:
                room_sizes[room] = base_area * 1.5
            elif room in ["bedroom", "office"]:
                room_sizes[room] = base_area * 1.2
            elif room in ["bathroom", "storage"]:
                room_sizes[room] = base_area * 0.5
            else:
                room_sizes[room] = base_area
        
        return room_sizes
    
    async def _generate_room_layout(
        self, 
        room_sizes: Dict[str, float], 
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate room layout"""
        
        layout = {}
        current_x = 0
        current_y = 0
        
        for room, size in room_sizes.items():
            # Calculate room dimensions
            width = np.sqrt(size * 1.2)  # Assume 1.2 aspect ratio
            height = size / width
            
            layout[room] = {
                "position": [current_x, current_y],
                "dimensions": [width, height],
                "area": size
            }
            
            # Move to next position
            current_x += width + 1  # 1m gap between rooms
            
            # Start new row if needed
            if current_x > 20:  # Max width
                current_x = 0
                current_y += height + 1
        
        return layout
    
    async def _apply_climate_considerations(
        self, 
        layout: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply climate considerations to layout"""
        
        recommendations = climate_data.get("architectural_recommendations", {})
        
        # Apply thermal comfort recommendations
        if "thermal_comfort" in recommendations:
            for room in layout:
                layout[room]["insulation"] = "high" if "High-performance insulation" in recommendations["thermal_comfort"] else "standard"
        
        # Apply ventilation recommendations
        if "ventilation" in recommendations:
            for room in layout:
                layout[room]["ventilation"] = "enhanced" if "Enhanced ventilation" in recommendations["ventilation"] else "standard"
        
        # Apply orientation recommendations
        if "orientation" in recommendations:
            layout["orientation"] = "south" if "south" in str(recommendations["orientation"]).lower() else "north"
        
        return layout
    
    async def _apply_style_elements(
        self, 
        layout: Dict[str, Any], 
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply architectural style elements to layout"""
        
        primary_style = architectural_style.get("primary_style", "Modern")
        style_elements = architectural_style.get("characteristic_elements", [])
        
        # Apply style-specific modifications
        if primary_style == "Traditional":
            layout["style_features"] = {
                "symmetry": "high",
                "proportions": "classical",
                "ornamentation": "moderate"
            }
        elif primary_style == "Modern":
            layout["style_features"] = {
                "symmetry": "low",
                "proportions": "contemporary",
                "ornamentation": "minimal"
            }
        elif primary_style == "Contemporary":
            layout["style_features"] = {
                "symmetry": "medium",
                "proportions": "dynamic",
                "ornamentation": "minimal"
            }
        
        return layout
    
    async def _generate_circulation(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Generate circulation paths"""
        return {
            "corridors": [
                {"start": [0, 0], "end": [20, 0], "width": 1.2},
                {"start": [0, 0], "end": [0, 20], "width": 1.2}
            ],
            "doors": [
                {"room": "living_room", "position": [5, 0], "width": 0.9},
                {"room": "kitchen", "position": [10, 0], "width": 0.9}
            ]
        }
    
    async def _generate_openings(
        self, 
        layout: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate windows and doors"""
        
        openings = {
            "windows": [],
            "doors": []
        }
        
        # Generate windows based on climate
        solar_orientation = climate_data.get("architectural_recommendations", {}).get("orientation", [])
        
        for room, room_data in layout.items():
            if room != "style_features":
                # Add windows
                openings["windows"].append({
                    "room": room,
                    "position": [room_data["position"][0], room_data["position"][1] + room_data["dimensions"][1]],
                    "size": [2, 1.5],
                    "orientation": "south" if "south" in str(solar_orientation).lower() else "north"
                })
        
        return openings
    
    async def _generate_elevations(
        self, 
        floor_plan: Dict[str, Any], 
        architectural_style: Dict[str, Any],
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate building elevations"""
        
        elevations = {}
        primary_style = architectural_style.get("primary_style", "Modern")
        
        # Generate front elevation
        elevations["front"] = {
            "height": 3.5,
            "style": primary_style,
            "materials": self._get_style_materials(primary_style),
            "openings": await self._generate_elevation_openings(floor_plan, "front")
        }
        
        # Generate side elevations
        elevations["side"] = {
            "height": 3.5,
            "style": primary_style,
            "materials": self._get_style_materials(primary_style),
            "openings": await self._generate_elevation_openings(floor_plan, "side")
        }
        
        return elevations
    
    def _get_style_materials(self, style: str) -> List[str]:
        """Get materials for architectural style"""
        material_map = {
            "Traditional": ["brick", "stone", "wood"],
            "Modern": ["concrete", "glass", "steel"],
            "Contemporary": ["recycled_materials", "smart_materials"],
            "Mediterranean": ["stucco", "tile", "stone"],
            "Colonial": ["brick", "wood", "stone"]
        }
        return material_map.get(style, ["concrete", "glass"])
    
    async def _generate_elevation_openings(
        self, 
        floor_plan: Dict[str, Any], 
        elevation_type: str
    ) -> List[Dict[str, Any]]:
        """Generate openings for elevation"""
        openings = []
        
        for room, room_data in floor_plan.items():
            if room != "style_features":
                openings.append({
                    "type": "window",
                    "position": [room_data["position"][0], 1.5],
                    "size": [1.5, 1.2],
                    "style": "modern"
                })
        
        return openings
    
    async def _generate_sections(
        self, 
        floor_plan: Dict[str, Any], 
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate building sections"""
        
        return {
            "longitudinal": {
                "height": 3.5,
                "structure": "concrete_frame",
                "insulation": "high_performance",
                "roof": "flat" if architectural_style.get("primary_style") == "Modern" else "pitched"
            },
            "transverse": {
                "height": 3.5,
                "structure": "concrete_frame",
                "insulation": "high_performance",
                "roof": "flat" if architectural_style.get("primary_style") == "Modern" else "pitched"
            }
        }
    
    async def _generate_3d_model(
        self, 
        project_requirements: Dict[str, Any],
        climate_data: Dict[str, Any],
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 3D model"""
        
        # Generate building geometry
        geometry = await self._generate_building_geometry(project_requirements, architectural_style)
        
        # Generate materials
        materials = await self._generate_materials(architectural_style, climate_data)
        
        # Generate lighting
        lighting = await self._generate_lighting(climate_data, architectural_style)
        
        return {
            "geometry": geometry,
            "materials": materials,
            "lighting": lighting,
            "textures": await self._generate_textures(architectural_style)
        }
    
    async def _generate_building_geometry(
        self, 
        project_requirements: Dict[str, Any],
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 3D building geometry"""
        
        surface_area = project_requirements.get("surface_area", 100)
        project_type = project_requirements.get("type", "residential")
        
        # Calculate building dimensions
        width = np.sqrt(surface_area * 1.2)
        depth = surface_area / width
        height = 3.5 if project_type == "residential" else 4.5
        
        # Generate vertices
        vertices = [
            [0, 0, 0], [width, 0, 0], [width, depth, 0], [0, depth, 0],  # Base
            [0, 0, height], [width, 0, height], [width, depth, height], [0, depth, height]  # Top
        ]
        
        # Generate faces
        faces = [
            [0, 1, 2, 3],  # Bottom
            [4, 5, 6, 7],  # Top
            [0, 1, 5, 4],  # Front
            [2, 3, 7, 6],  # Back
            [0, 3, 7, 4],  # Left
            [1, 2, 6, 5]   # Right
        ]
        
        return {
            "vertices": vertices,
            "faces": faces,
            "dimensions": [width, depth, height]
        }
    
    async def _generate_materials(
        self, 
        architectural_style: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate materials for 3D model"""
        
        primary_style = architectural_style.get("primary_style", "Modern")
        style_materials = self._get_style_materials(primary_style)
        
        # Apply climate considerations
        climate_materials = climate_data.get("architectural_recommendations", {}).get("materials", [])
        
        # Combine style and climate materials
        combined_materials = list(set(style_materials + climate_materials))
        
        return {
            "primary": combined_materials[0] if combined_materials else "concrete",
            "secondary": combined_materials[1] if len(combined_materials) > 1 else combined_materials[0],
            "accent": combined_materials[2] if len(combined_materials) > 2 else combined_materials[0],
            "properties": await self._get_material_properties(combined_materials)
        }
    
    async def _get_material_properties(self, materials: List[str]) -> Dict[str, Any]:
        """Get material properties"""
        properties = {}
        
        for material in materials:
            if material == "concrete":
                properties[material] = {"roughness": 0.6, "reflectivity": 0.2, "color": [0.8, 0.8, 0.8]}
            elif material == "glass":
                properties[material] = {"roughness": 0.1, "reflectivity": 0.9, "color": [0.9, 0.9, 1.0]}
            elif material == "brick":
                properties[material] = {"roughness": 0.8, "reflectivity": 0.1, "color": [0.7, 0.4, 0.3]}
            elif material == "wood":
                properties[material] = {"roughness": 0.7, "reflectivity": 0.1, "color": [0.6, 0.4, 0.2]}
            else:
                properties[material] = {"roughness": 0.5, "reflectivity": 0.3, "color": [0.8, 0.8, 0.8]}
        
        return properties
    
    async def _generate_lighting(
        self, 
        climate_data: Dict[str, Any], 
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate lighting setup"""
        
        # Get solar data from climate
        solar_data = climate_data.get("solar_irradiance", [])
        avg_solar = sum([month["solar_irradiance"] for month in solar_data]) / 12 if solar_data else 1000
        
        return {
            "natural_lighting": {
                "solar_gain": avg_solar,
                "window_area": "large" if avg_solar > 1000 else "standard",
                "orientation": "south" if avg_solar > 800 else "north"
            },
            "artificial_lighting": {
                "ambient": 300,  # lux
                "task": 500,     # lux
                "accent": 200    # lux
            },
            "lighting_control": "smart" if architectural_style.get("primary_style") == "Contemporary" else "standard"
        }
    
    async def _generate_landscaping(
        self, 
        climate_data: Dict[str, Any], 
        architectural_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate landscaping elements"""
        
        # Get climate recommendations
        recommendations = climate_data.get("architectural_recommendations", {})
        
        return {
            "vegetation": {
                "trees": "native" if "native" in str(recommendations) else "ornamental",
                "shrubs": "drought_tolerant" if "drought" in str(recommendations) else "standard",
                "grass": "native" if "native" in str(recommendations) else "turf"
            },
            "hardscaping": {
                "patio": "permeable" if "permeable" in str(recommendations) else "concrete",
                "walkways": "natural" if "natural" in str(recommendations) else "paved"
            },
            "water_features": "rainwater_harvesting" if "rainwater" in str(recommendations) else "none"
        }
    
    async def _generate_textures(self, architectural_style: Dict[str, Any]) -> Dict[str, Any]:
        """Generate textures for 3D model"""
        
        primary_style = architectural_style.get("primary_style", "Modern")
        
        texture_map = {
            "Traditional": {"roughness": 0.8, "bump": 0.3, "detail": "high"},
            "Modern": {"roughness": 0.3, "bump": 0.1, "detail": "low"},
            "Contemporary": {"roughness": 0.5, "bump": 0.2, "detail": "medium"}
        }
        
        return texture_map.get(primary_style, texture_map["Modern"])
    
    async def _generate_viewpoints(self, project_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate viewpoints for 3D visualization"""
        
        return [
            {
                "name": "Front View",
                "position": [0, -10, 2],
                "target": [0, 0, 2],
                "fov": 60
            },
            {
                "name": "Side View",
                "position": [-10, 0, 2],
                "target": [0, 0, 2],
                "fov": 60
            },
            {
                "name": "Aerial View",
                "position": [0, 0, 20],
                "target": [0, 0, 0],
                "fov": 45
            },
            {
                "name": "Interior View",
                "position": [5, 5, 1.5],
                "target": [10, 10, 1.5],
                "fov": 75
            }
        ]
