"""
ArchiAI Solution - Main FastAPI Application
AI-powered architectural design system
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import ai_models
backend_dir = Path(__file__).resolve().parent
parent_dir = backend_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from datetime import datetime

from services.climate_service import ClimateService
from services.location_service import LocationService
from services.design_service import DesignService
from services.export_service import ExportService
from services.cost_service import CostService
from models.database import init_db
from models.schemas import *

app = FastAPI(
    title="ArchiAI Solution",
    description="AI-powered architectural design system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
climate_service = ClimateService()
location_service = LocationService()
design_service = DesignService()
export_service = ExportService()
cost_service = CostService()

# Initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "ArchiAI Solution API", "version": "1.0.0"}

# Climate and Location Analysis
@app.post("/api/analyze-location")
async def analyze_location(location: LocationRequest):
    """Analyze location for climate, architectural style, and surroundings"""
    try:
        # Get climate data
        climate_data = await climate_service.get_climate_data(location.address)
        
        # Get architectural style
        architectural_style = await location_service.detect_architectural_style(
            location.address, location.postal_code
        )
        
        # Get 3D surroundings
        surroundings_3d = await location_service.get_3d_surroundings(
            location.address, location.postal_code
        )
        
        return {
            "climate": climate_data,
            "architectural_style": architectural_style,
            "surroundings_3d": surroundings_3d,
            "location": {
                "address": location.address,
                "postal_code": location.postal_code,
                "coordinates": climate_data.get("coordinates")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Project Creation
@app.post("/api/create-project")
async def create_project(
    project_data: ProjectRequest,
    portfolio_files: List[UploadFile] = File(None)
):
    """Create a new architectural project"""
    try:
        # Process uploaded portfolio files
        portfolio_data = None
        if portfolio_files:
            portfolio_data = await design_service.process_portfolio(portfolio_files)
        
        # Create project
        project = await design_service.create_project(
            project_data, portfolio_data
        )
        
        return {"project_id": project.id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Design Generation
@app.post("/api/generate-design")
async def generate_design(design_request: DesignRequest):
    """Generate AI-powered architectural design"""
    try:
        # Generate 2D design
        design_2d = await design_service.generate_2d_design(design_request)
        
        # Generate 3D design
        design_3d = await design_service.generate_3d_design(design_request)
        
        # Generate structural design
        structural_design = await design_service.generate_structural_design(design_request)
        
        # Generate MEP design
        mep_design = await design_service.generate_mep_design(design_request)
        
        return {
            "design_2d": design_2d,
            "design_3d": design_3d,
            "structural": structural_design,
            "mep": mep_design,
            "project_id": design_request.project_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Text-based Modification
@app.post("/api/modify-design")
async def modify_design(modification_request: ModificationRequest):
    """Modify design using natural language commands"""
    try:
        modified_design = await design_service.modify_design(
            modification_request.project_id,
            modification_request.text_command,
            modification_request.modification_type
        )
        
        return {
            "modified_design": modified_design,
            "project_id": modification_request.project_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export to Architecture Software
@app.post("/api/export-design")
async def export_design(export_request: ExportRequest):
    """Export design to various architecture software formats"""
    try:
        export_result = await export_service.export_design(
            export_request.project_id,
            export_request.export_format,
            export_request.software_type
        )
        
        return {
            "export_url": export_result["url"],
            "format": export_request.export_format,
            "software": export_request.software_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cost Estimation
@app.post("/api/estimate-cost")
async def estimate_cost(cost_request: CostRequest):
    """Generate cost estimation for the project"""
    try:
        cost_estimate = await cost_service.generate_cost_estimate(
            cost_request.project_id,
            cost_request.region,
            cost_request.currency
        )
        
        return {
            "cost_estimate": cost_estimate,
            "excel_url": cost_estimate.get("excel_url"),
            "project_id": cost_request.project_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Project Status
@app.get("/api/project/{project_id}")
async def get_project(project_id: str):
    """Get project details and status"""
    try:
        project = await design_service.get_project(project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=404, detail="Project not found")

# Health Check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
