"""
Design Service - Handles AI-powered architectural design generation
"""

import asyncio
import uuid
from typing import Dict, Any, List, Optional
import json
import os
from ..ai_models.style_classifier import DesignGenerator
from ..services.structural_service import StructuralService
from ..services.mep_service import MEPService
from ..models.schemas import *

class DesignService:
    def __init__(self):
        self.design_generator = DesignGenerator()
        self.structural_service = StructuralService()
        self.mep_service = MEPService()
        self.projects = {}  # In-memory storage for demo
        
    async def process_portfolio(self, portfolio_files: List[UploadFile]) -> Dict[str, Any]:
        """Process uploaded portfolio files"""
        portfolio_data = {
            "files": [],
            "styles": [],
            "elements": []
        }
        
        for file in portfolio_files:
            # Process each file
            file_data = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
                "processed": False
            }
            
            # Analyze file for architectural elements
            if file.content_type.startswith("image/"):
                analysis = await self._analyze_image_file(file)
                file_data["analysis"] = analysis
                portfolio_data["styles"].extend(analysis.get("styles", []))
                portfolio_data["elements"].extend(analysis.get("elements", []))
            
            portfolio_data["files"].append(file_data)
        
        return portfolio_data
    
    async def _analyze_image_file(self, file: UploadFile) -> Dict[str, Any]:
        """Analyze image file for architectural elements"""
        # This would typically involve computer vision analysis
        # For now, we'll return simulated analysis
        return {
            "styles": ["Modern", "Contemporary"],
            "elements": ["large_windows", "clean_lines", "open_spaces"],
            "materials": ["glass", "concrete", "steel"],
            "confidence": 0.8
        }
    
    async def create_project(self, project_data: ProjectRequest, portfolio_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new architectural project"""
        project_id = str(uuid.uuid4())
        
        project = {
            "id": project_id,
            "name": project_data.name,
            "type": project_data.type,
            "surface_area": project_data.surface_area,
            "location": project_data.location,
            "requirements": project_data.requirements,
            "portfolio": portfolio_data,
            "status": "created",
            "created_at": "2024-01-01T00:00:00Z",
            "designs": {
                "2d": None,
                "3d": None,
                "structural": None,
                "mep": None
            }
        }
        
        self.projects[project_id] = project
        return project
    
    async def generate_2d_design(self, design_request: DesignRequest) -> Dict[str, Any]:
        """Generate 2D architectural design"""
        project = self.projects.get(design_request.project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Get project data
        project_requirements = {
            "type": project["type"],
            "surface_area": project["surface_area"],
            "requirements": project["requirements"]
        }
        
        # Get climate and style data from design request
        climate_data = design_request.climate_data
        architectural_style = design_request.architectural_style
        
        # Generate 2D design
        design_2d = await self.design_generator.generate_2d_design(
            project_requirements, climate_data, architectural_style
        )
        
        # Store design
        project["designs"]["2d"] = design_2d
        project["status"] = "2d_design_complete"
        
        return design_2d
    
    async def generate_3d_design(self, design_request: DesignRequest) -> Dict[str, Any]:
        """Generate 3D architectural design"""
        project = self.projects.get(design_request.project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Get project data
        project_requirements = {
            "type": project["type"],
            "surface_area": project["surface_area"],
            "requirements": project["requirements"]
        }
        
        # Get climate and style data from design request
        climate_data = design_request.climate_data
        architectural_style = design_request.architectural_style
        
        # Generate 3D design
        design_3d = await self.design_generator.generate_3d_design(
            project_requirements, climate_data, architectural_style
        )
        
        # Store design
        project["designs"]["3d"] = design_3d
        project["status"] = "3d_design_complete"
        
        return design_3d
    
    async def generate_structural_design(self, design_request: DesignRequest) -> Dict[str, Any]:
        """Generate structural design"""
        project = self.projects.get(design_request.project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Get 2D design for structural analysis
        design_2d = project["designs"]["2d"]
        if not design_2d:
            raise ValueError("2D design not found")
        
        # Generate structural design
        structural_design = await self.structural_service.generate_structural_design(
            design_2d, design_request.climate_data
        )
        
        # Store design
        project["designs"]["structural"] = structural_design
        project["status"] = "structural_design_complete"
        
        return structural_design
    
    async def generate_mep_design(self, design_request: DesignRequest) -> Dict[str, Any]:
        """Generate MEP (Mechanical, Electrical, Plumbing) design"""
        project = self.projects.get(design_request.project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Get 2D design for MEP analysis
        design_2d = project["designs"]["2d"]
        if not design_2d:
            raise ValueError("2D design not found")
        
        # Generate MEP design
        mep_design = await self.mep_service.generate_mep_design(
            design_2d, design_request.climate_data
        )
        
        # Store design
        project["designs"]["mep"] = mep_design
        project["status"] = "mep_design_complete"
        
        return mep_design
    
    async def modify_design(
        self, 
        project_id: str, 
        text_command: str, 
        modification_type: str
    ) -> Dict[str, Any]:
        """Modify design using natural language commands"""
        project = self.projects.get(project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Parse text command
        modification = await self._parse_text_command(text_command, modification_type)
        
        # Apply modification to appropriate design
        if modification_type == "2d":
            modified_design = await self._modify_2d_design(project["designs"]["2d"], modification)
            project["designs"]["2d"] = modified_design
        elif modification_type == "3d":
            modified_design = await self._modify_3d_design(project["designs"]["3d"], modification)
            project["designs"]["3d"] = modified_design
        elif modification_type == "structural":
            modified_design = await self._modify_structural_design(project["designs"]["structural"], modification)
            project["designs"]["structural"] = modified_design
        elif modification_type == "mep":
            modified_design = await self._modify_mep_design(project["designs"]["mep"], modification)
            project["designs"]["mep"] = modified_design
        
        project["status"] = f"{modification_type}_modified"
        
        return {
            "modified_design": modified_design,
            "modification": modification,
            "project_id": project_id
        }
    
    async def _parse_text_command(self, text_command: str, modification_type: str) -> Dict[str, Any]:
        """Parse natural language command into structured modification"""
        # This would typically involve NLP processing
        # For now, we'll return a simplified parsing
        
        modification = {
            "type": modification_type,
            "command": text_command,
            "parameters": {}
        }
        
        # Simple keyword matching
        if "increase" in text_command.lower():
            modification["action"] = "increase"
        elif "decrease" in text_command.lower():
            modification["action"] = "decrease"
        elif "add" in text_command.lower():
            modification["action"] = "add"
        elif "remove" in text_command.lower():
            modification["action"] = "remove"
        elif "change" in text_command.lower():
            modification["action"] = "change"
        else:
            modification["action"] = "modify"
        
        # Extract parameters
        if "room" in text_command.lower():
            modification["parameters"]["element"] = "room"
        elif "window" in text_command.lower():
            modification["parameters"]["element"] = "window"
        elif "door" in text_command.lower():
            modification["parameters"]["element"] = "door"
        elif "wall" in text_command.lower():
            modification["parameters"]["element"] = "wall"
        
        # Extract dimensions
        import re
        dimension_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', text_command)
        if dimension_match:
            modification["parameters"]["dimensions"] = [
                float(dimension_match.group(1)),
                float(dimension_match.group(2))
            ]
        
        return modification
    
    async def _modify_2d_design(self, design_2d: Dict[str, Any], modification: Dict[str, Any]) -> Dict[str, Any]:
        """Modify 2D design based on modification parameters"""
        if not design_2d:
            return design_2d
        
        # Apply modification to floor plan
        if "rooms" in design_2d:
            modified_rooms = await self._apply_room_modification(
                design_2d["rooms"], modification
            )
            design_2d["rooms"] = modified_rooms
        
        # Apply modification to openings
        if "openings" in design_2d:
            modified_openings = await self._apply_opening_modification(
                design_2d["openings"], modification
            )
            design_2d["openings"] = modified_openings
        
        return design_2d
    
    async def _modify_3d_design(self, design_3d: Dict[str, Any], modification: Dict[str, Any]) -> Dict[str, Any]:
        """Modify 3D design based on modification parameters"""
        if not design_3d:
            return design_3d
        
        # Apply modification to 3D model
        if "model_3d" in design_3d:
            modified_model = await self._apply_3d_modification(
                design_3d["model_3d"], modification
            )
            design_3d["model_3d"] = modified_model
        
        return design_3d
    
    async def _modify_structural_design(self, structural_design: Dict[str, Any], modification: Dict[str, Any]) -> Dict[str, Any]:
        """Modify structural design based on modification parameters"""
        if not structural_design:
            return structural_design
        
        # Apply structural modifications
        if "beams" in structural_design:
            modified_beams = await self._apply_beam_modification(
                structural_design["beams"], modification
            )
            structural_design["beams"] = modified_beams
        
        return structural_design
    
    async def _modify_mep_design(self, mep_design: Dict[str, Any], modification: Dict[str, Any]) -> Dict[str, Any]:
        """Modify MEP design based on modification parameters"""
        if not mep_design:
            return mep_design
        
        # Apply MEP modifications
        if "electrical" in mep_design:
            modified_electrical = await self._apply_electrical_modification(
                mep_design["electrical"], modification
            )
            mep_design["electrical"] = modified_electrical
        
        return mep_design
    
    async def _apply_room_modification(
        self, 
        rooms: Dict[str, Any], 
        modification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply room modification"""
        action = modification.get("action", "modify")
        element = modification.get("parameters", {}).get("element", "room")
        
        if action == "add" and element == "room":
            # Add new room
            new_room = {
                "position": [0, 0],
                "dimensions": [4, 4],
                "area": 16
            }
            rooms[f"new_room_{len(rooms)}"] = new_room
        
        elif action == "remove" and element == "room":
            # Remove room (simplified - remove first room)
            if rooms:
                first_room = list(rooms.keys())[0]
                del rooms[first_room]
        
        elif action == "increase" and element == "room":
            # Increase room size
            for room_name, room_data in rooms.items():
                if "dimensions" in room_data:
                    room_data["dimensions"][0] *= 1.1
                    room_data["dimensions"][1] *= 1.1
                    room_data["area"] = room_data["dimensions"][0] * room_data["dimensions"][1]
        
        return rooms
    
    async def _apply_opening_modification(
        self, 
        openings: Dict[str, Any], 
        modification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply opening modification"""
        action = modification.get("action", "modify")
        element = modification.get("parameters", {}).get("element", "window")
        
        if action == "add" and element == "window":
            # Add new window
            new_window = {
                "type": "window",
                "position": [2, 2],
                "size": [1.5, 1.2],
                "style": "modern"
            }
            openings["windows"].append(new_window)
        
        elif action == "remove" and element == "window":
            # Remove window (simplified - remove first window)
            if openings.get("windows"):
                openings["windows"].pop(0)
        
        return openings
    
    async def _apply_3d_modification(
        self, 
        model_3d: Dict[str, Any], 
        modification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply 3D model modification"""
        action = modification.get("action", "modify")
        
        if action == "increase" and "geometry" in model_3d:
            # Increase building size
            geometry = model_3d["geometry"]
            if "dimensions" in geometry:
                geometry["dimensions"][0] *= 1.1
                geometry["dimensions"][1] *= 1.1
                geometry["dimensions"][2] *= 1.1
        
        return model_3d
    
    async def _apply_beam_modification(
        self, 
        beams: List[Dict[str, Any]], 
        modification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply beam modification"""
        action = modification.get("action", "modify")
        
        if action == "increase":
            # Increase beam size
            for beam in beams:
                if "size" in beam:
                    beam["size"] *= 1.1
        
        return beams
    
    async def _apply_electrical_modification(
        self, 
        electrical: Dict[str, Any], 
        modification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply electrical modification"""
        action = modification.get("action", "modify")
        
        if action == "add":
            # Add electrical component
            if "outlets" not in electrical:
                electrical["outlets"] = []
            
            new_outlet = {
                "type": "standard",
                "position": [2, 2],
                "rating": "15A"
            }
            electrical["outlets"].append(new_outlet)
        
        return electrical
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details"""
        project = self.projects.get(project_id)
        if not project:
            raise ValueError("Project not found")
        
        return project
