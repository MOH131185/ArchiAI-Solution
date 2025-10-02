"""
3D Surroundings Generator - Creates 3D visualization of surrounding area
"""

import json
import math
from typing import Dict, Any, List, Tuple
import numpy as np

class Surroundings3DGenerator:
    def __init__(self):
        self.building_templates = self._load_building_templates()
        self.terrain_generator = TerrainGenerator()
        
    def _load_building_templates(self) -> Dict[str, Any]:
        """Load 3D building templates for different building types"""
        return {
            "residential": {
                "height_range": (3, 15),
                "width_range": (8, 20),
                "depth_range": (8, 20),
                "roof_types": ["pitched", "flat", "gabled"],
                "window_patterns": ["traditional", "modern", "large"],
                "materials": ["brick", "wood", "stucco", "concrete"]
            },
            "commercial": {
                "height_range": (10, 50),
                "width_range": (15, 40),
                "depth_range": (15, 40),
                "roof_types": ["flat", "modern"],
                "window_patterns": ["large", "curtain_wall", "strip"],
                "materials": ["glass", "steel", "concrete", "aluminum"]
            },
            "industrial": {
                "height_range": (8, 25),
                "width_range": (20, 60),
                "depth_range": (20, 60),
                "roof_types": ["flat", "sawtooth"],
                "window_patterns": ["minimal", "strip"],
                "materials": ["steel", "concrete", "metal"]
            },
            "institutional": {
                "height_range": (5, 30),
                "width_range": (20, 50),
                "depth_range": (20, 50),
                "roof_types": ["flat", "pitched", "domed"],
                "window_patterns": ["traditional", "large", "strip"],
                "materials": ["concrete", "brick", "stone", "glass"]
            }
        }
    
    async def generate_3d_surroundings(
        self, 
        coordinates: Tuple[float, float], 
        building_data: List[Dict[str, Any]], 
        terrain_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 3D model of surrounding area"""
        
        # Generate terrain mesh
        terrain_mesh = await self.terrain_generator.generate_terrain_mesh(
            coordinates, terrain_data
        )
        
        # Generate building models
        building_models = await self._generate_building_models(building_data)
        
        # Generate street network
        street_network = await self._generate_street_network(coordinates, building_data)
        
        # Generate vegetation
        vegetation = await self._generate_vegetation(coordinates, building_data)
        
        # Combine all elements
        surroundings_3d = {
            "terrain": terrain_mesh,
            "buildings": building_models,
            "streets": street_network,
            "vegetation": vegetation,
            "lighting": await self._generate_lighting_setup(coordinates),
            "camera_positions": await self._calculate_camera_positions(coordinates),
            "bounding_box": await self._calculate_bounding_box(coordinates, building_data)
        }
        
        return surroundings_3d
    
    async def _generate_building_models(self, building_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate 3D models for buildings"""
        building_models = []
        
        for building in building_data:
            model = await self._create_building_model(building)
            building_models.append(model)
        
        return building_models
    
    async def _create_building_model(self, building: Dict[str, Any]) -> Dict[str, Any]:
        """Create 3D model for a single building"""
        building_type = building.get("type", "residential")
        template = self.building_templates.get(building_type, self.building_templates["residential"])
        
        # Generate building dimensions
        height = np.random.uniform(*template["height_range"])
        width = np.random.uniform(*template["width_range"])
        depth = np.random.uniform(*template["depth_range"])
        
        # Generate building geometry
        geometry = await self._generate_building_geometry(
            width, depth, height, template
        )
        
        # Generate materials and textures
        materials = await self._generate_building_materials(template)
        
        # Generate windows and doors
        openings = await self._generate_building_openings(width, depth, height, template)
        
        return {
            "id": building.get("id", "unknown"),
            "type": building_type,
            "coordinates": building.get("coordinates", {}),
            "dimensions": {"width": width, "depth": depth, "height": height},
            "geometry": geometry,
            "materials": materials,
            "openings": openings,
            "style": building.get("style", "modern")
        }
    
    async def _generate_building_geometry(
        self, width: float, depth: float, height: float, template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate 3D geometry for building"""
        
        # Generate base shape
        base_vertices = [
            [0, 0, 0],
            [width, 0, 0],
            [width, depth, 0],
            [0, depth, 0]
        ]
        
        # Generate roof
        roof_type = np.random.choice(template["roof_types"])
        roof_geometry = await self._generate_roof_geometry(width, depth, height, roof_type)
        
        # Generate walls
        wall_geometry = await self._generate_wall_geometry(width, depth, height)
        
        return {
            "base": base_vertices,
            "roof": roof_geometry,
            "walls": wall_geometry,
            "roof_type": roof_type
        }
    
    async def _generate_roof_geometry(
        self, width: float, depth: float, height: float, roof_type: str
    ) -> Dict[str, Any]:
        """Generate roof geometry based on type"""
        
        if roof_type == "flat":
            return {
                "type": "flat",
                "vertices": [
                    [0, 0, height],
                    [width, 0, height],
                    [width, depth, height],
                    [0, depth, height]
                ]
            }
        elif roof_type == "pitched":
            # Gabled roof
            ridge_height = height + depth * 0.3
            return {
                "type": "pitched",
                "vertices": [
                    [0, 0, height],
                    [width, 0, height],
                    [width/2, depth/2, ridge_height],
                    [0, depth, height]
                ]
            }
        elif roof_type == "gabled":
            # Cross-gabled roof
            return {
                "type": "gabled",
                "vertices": [
                    [0, 0, height],
                    [width, 0, height],
                    [width, depth, height],
                    [0, depth, height],
                    [width/2, depth/2, height + depth * 0.2]
                ]
            }
        else:
            return await self._generate_roof_geometry(width, depth, height, "flat")
    
    async def _generate_wall_geometry(
        self, width: float, depth: float, height: float
    ) -> List[Dict[str, Any]]:
        """Generate wall geometry"""
        walls = []
        
        # Front wall
        walls.append({
            "face": "front",
            "vertices": [
                [0, 0, 0], [width, 0, 0], [width, 0, height], [0, 0, height]
            ]
        })
        
        # Back wall
        walls.append({
            "face": "back",
            "vertices": [
                [0, depth, 0], [width, depth, 0], [width, depth, height], [0, depth, height]
            ]
        })
        
        # Left wall
        walls.append({
            "face": "left",
            "vertices": [
                [0, 0, 0], [0, depth, 0], [0, depth, height], [0, 0, height]
            ]
        })
        
        # Right wall
        walls.append({
            "face": "right",
            "vertices": [
                [width, 0, 0], [width, depth, 0], [width, depth, height], [width, 0, height]
            ]
        })
        
        return walls
    
    async def _generate_building_materials(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Generate materials for building"""
        materials = template.get("materials", ["concrete"])
        selected_materials = np.random.choice(materials, size=min(3, len(materials)), replace=False)
        
        return {
            "primary": selected_materials[0],
            "secondary": selected_materials[1] if len(selected_materials) > 1 else selected_materials[0],
            "accent": selected_materials[2] if len(selected_materials) > 2 else selected_materials[0],
            "textures": await self._generate_material_textures(selected_materials)
        }
    
    async def _generate_material_textures(self, materials: List[str]) -> Dict[str, Any]:
        """Generate texture information for materials"""
        texture_map = {
            "brick": {"roughness": 0.8, "reflectivity": 0.1, "color": [0.7, 0.4, 0.3]},
            "concrete": {"roughness": 0.6, "reflectivity": 0.2, "color": [0.8, 0.8, 0.8]},
            "glass": {"roughness": 0.1, "reflectivity": 0.9, "color": [0.9, 0.9, 1.0]},
            "steel": {"roughness": 0.3, "reflectivity": 0.7, "color": [0.6, 0.6, 0.6]},
            "wood": {"roughness": 0.7, "reflectivity": 0.1, "color": [0.6, 0.4, 0.2]},
            "stucco": {"roughness": 0.5, "reflectivity": 0.3, "color": [0.9, 0.9, 0.8]}
        }
        
        return {material: texture_map.get(material, texture_map["concrete"]) for material in materials}
    
    async def _generate_building_openings(
        self, width: float, depth: float, height: float, template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate windows and doors for building"""
        window_pattern = np.random.choice(template["window_patterns"])
        
        # Generate windows
        windows = await self._generate_windows(width, depth, height, window_pattern)
        
        # Generate doors
        doors = await self._generate_doors(width, depth, height)
        
        return {
            "windows": windows,
            "doors": doors,
            "pattern": window_pattern
        }
    
    async def _generate_windows(
        self, width: float, depth: float, height: float, pattern: str
    ) -> List[Dict[str, Any]]:
        """Generate window openings"""
        windows = []
        
        if pattern == "traditional":
            # Traditional windows
            window_width = width * 0.15
            window_height = height * 0.3
            spacing = width * 0.1
            
            for i in range(int(width / (window_width + spacing))):
                windows.append({
                    "type": "window",
                    "position": [i * (window_width + spacing), 0, height * 0.3],
                    "size": [window_width, window_height],
                    "style": "traditional"
                })
        
        elif pattern == "modern":
            # Modern large windows
            window_width = width * 0.4
            window_height = height * 0.6
            
            windows.append({
                "type": "window",
                "position": [width * 0.3, 0, height * 0.2],
                "size": [window_width, window_height],
                "style": "modern"
            })
        
        elif pattern == "large":
            # Large windows
            window_width = width * 0.8
            window_height = height * 0.8
            
            windows.append({
                "type": "window",
                "position": [width * 0.1, 0, height * 0.1],
                "size": [window_width, window_height],
                "style": "large"
            })
        
        return windows
    
    async def _generate_doors(self, width: float, depth: float, height: float) -> List[Dict[str, Any]]:
        """Generate door openings"""
        door_width = width * 0.2
        door_height = height * 0.8
        
        return [{
            "type": "door",
            "position": [width * 0.4, 0, 0],
            "size": [door_width, door_height],
            "style": "standard"
        }]
    
    async def _generate_street_network(
        self, coordinates: Tuple[float, float], building_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate street network"""
        lat, lon = coordinates
        
        # Generate main streets
        main_streets = [
            {
                "type": "main",
                "start": [lat - 0.001, lon - 0.001],
                "end": [lat + 0.001, lon + 0.001],
                "width": 12
            },
            {
                "type": "main",
                "start": [lat - 0.001, lon + 0.001],
                "end": [lat + 0.001, lon - 0.001],
                "width": 12
            }
        ]
        
        # Generate side streets
        side_streets = []
        for i in range(4):
            side_streets.append({
                "type": "side",
                "start": [lat - 0.0005, lon - 0.001 + i * 0.0005],
                "end": [lat + 0.0005, lon - 0.001 + i * 0.0005],
                "width": 8
            })
        
        return {
            "main_streets": main_streets,
            "side_streets": side_streets,
            "intersections": await self._generate_intersections(main_streets, side_streets)
        }
    
    async def _generate_intersections(
        self, main_streets: List[Dict[str, Any]], side_streets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate street intersections"""
        intersections = []
        
        # Main intersection
        intersections.append({
            "type": "main",
            "position": [0, 0],
            "size": 20,
            "traffic_light": True
        })
        
        # Side intersections
        for i in range(2):
            intersections.append({
                "type": "side",
                "position": [0, 0],
                "size": 15,
                "traffic_light": False
            })
        
        return intersections
    
    async def _generate_vegetation(
        self, coordinates: Tuple[float, float], building_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate vegetation elements"""
        lat, lon = coordinates
        
        # Generate trees
        trees = []
        for i in range(20):
            trees.append({
                "type": "tree",
                "position": [
                    lat + (i - 10) * 0.0001,
                    lon + (i - 10) * 0.0001
                ],
                "size": np.random.uniform(2, 8),
                "species": np.random.choice(["oak", "maple", "pine", "birch"])
            })
        
        # Generate grass areas
        grass_areas = [
            {
                "type": "grass",
                "position": [lat, lon],
                "size": [100, 100],
                "density": 0.8
            }
        ]
        
        return {
            "trees": trees,
            "grass_areas": grass_areas,
            "parks": await self._generate_parks(coordinates)
        }
    
    async def _generate_parks(self, coordinates: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Generate park areas"""
        lat, lon = coordinates
        
        return [
            {
                "type": "park",
                "position": [lat + 0.0005, lon + 0.0005],
                "size": [50, 50],
                "features": ["playground", "benches", "trees"]
            }
        ]
    
    async def _generate_lighting_setup(self, coordinates: Tuple[float, float]) -> Dict[str, Any]:
        """Generate lighting setup for 3D scene"""
        return {
            "sun_position": [45, 30],  # Azimuth, elevation
            "ambient_light": 0.3,
            "directional_light": 0.7,
            "street_lights": await self._generate_street_lights(coordinates)
        }
    
    async def _generate_street_lights(self, coordinates: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Generate street lighting"""
        lat, lon = coordinates
        lights = []
        
        for i in range(10):
            lights.append({
                "position": [lat + (i - 5) * 0.0002, lon + (i - 5) * 0.0002],
                "height": 6,
                "intensity": 1000,
                "color": [1.0, 0.9, 0.8]
            })
        
        return lights
    
    async def _calculate_camera_positions(self, coordinates: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Calculate optimal camera positions for 3D viewing"""
        lat, lon = coordinates
        
        return [
            {
                "name": "Street View",
                "position": [lat, lon, 1.8],
                "target": [lat + 0.0001, lon + 0.0001, 1.8],
                "fov": 75
            },
            {
                "name": "Aerial View",
                "position": [lat, lon, 100],
                "target": [lat, lon, 0],
                "fov": 60
            },
            {
                "name": "Corner View",
                "position": [lat + 0.0005, lon + 0.0005, 10],
                "target": [lat, lon, 0],
                "fov": 70
            }
        ]
    
    async def _calculate_bounding_box(
        self, coordinates: Tuple[float, float], building_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate bounding box for 3D scene"""
        lat, lon = coordinates
        
        # Calculate bounds based on buildings
        min_lat = min([b.get("coordinates", {}).get("lat", lat) for b in building_data] + [lat])
        max_lat = max([b.get("coordinates", {}).get("lat", lat) for b in building_data] + [lat])
        min_lon = min([b.get("coordinates", {}).get("lon", lon) for b in building_data] + [lon])
        max_lon = max([b.get("coordinates", {}).get("lon", lon) for b in building_data] + [lon])
        
        return {
            "min": [min_lat, min_lon, 0],
            "max": [max_lat, max_lon, 100],
            "center": [lat, lon, 50],
            "size": [max_lat - min_lat, max_lon - min_lon, 100]
        }

class TerrainGenerator:
    def __init__(self):
        pass
    
    async def generate_terrain_mesh(
        self, coordinates: Tuple[float, float], terrain_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate terrain mesh"""
        lat, lon = coordinates
        elevation = terrain_data.get("elevation", 100)
        slope = terrain_data.get("slope", 0.05)
        
        # Generate terrain vertices
        vertices = []
        for i in range(20):
            for j in range(20):
                x = (i - 10) * 0.0001
                z = (j - 10) * 0.0001
                y = elevation + x * slope * 1000 + z * slope * 1000
                vertices.append([x, y, z])
        
        # Generate faces
        faces = []
        for i in range(19):
            for j in range(19):
                v1 = i * 20 + j
                v2 = v1 + 1
                v3 = v1 + 20
                v4 = v3 + 1
                
                faces.append([v1, v2, v3])
                faces.append([v2, v4, v3])
        
        return {
            "vertices": vertices,
            "faces": faces,
            "materials": {
                "type": "terrain",
                "texture": "grass",
                "color": [0.3, 0.6, 0.3]
            }
        }
