"""
Pydantic schemas for ArchiAI Solution
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class ProjectType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INSTITUTIONAL = "institutional"
    INDUSTRIAL = "industrial"

class DesignStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MODIFIED = "modified"

class ExportFormat(str, Enum):
    DWG = "dwg"
    DXF = "dxf"
    RVT = "rvt"
    SKP = "skp"
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"

class SoftwareType(str, Enum):
    AUTOCAD = "autocad"
    REVIT = "revit"
    SKETCHUP = "sketchup"
    ARCHICAD = "archicad"
    VECTORWORKS = "vectorworks"

class ModificationType(str, Enum):
    DESIGN_2D = "2d"
    DESIGN_3D = "3d"
    STRUCTURAL = "structural"
    MEP = "mep"

# Location and Climate Schemas
class LocationRequest(BaseModel):
    address: str = Field(..., description="Project address")
    postal_code: Optional[str] = Field(None, description="Postal code")
    country: Optional[str] = Field(None, description="Country")

class ClimateData(BaseModel):
    coordinates: Dict[str, float] = Field(..., description="Latitude and longitude")
    current_weather: Dict[str, Any] = Field(..., description="Current weather data")
    historical_data: Dict[str, Any] = Field(..., description="Historical climate data")
    seasonal_patterns: Dict[str, Any] = Field(..., description="Seasonal climate patterns")
    climate_analysis: Dict[str, Any] = Field(..., description="Climate analysis results")
    architectural_recommendations: Dict[str, Any] = Field(..., description="Architectural recommendations")

class ArchitecturalStyle(BaseModel):
    primary_style: str = Field(..., description="Primary architectural style")
    secondary_styles: List[str] = Field(..., description="Secondary architectural styles")
    style_confidence: float = Field(..., description="Style confidence score")
    characteristic_elements: List[str] = Field(..., description="Characteristic architectural elements")
    historical_context: Dict[str, Any] = Field(..., description="Historical context")
    recommended_integration: Dict[str, Any] = Field(..., description="Integration recommendations")

class Surroundings3D(BaseModel):
    coordinates: Dict[str, float] = Field(..., description="Location coordinates")
    buildings: List[Dict[str, Any]] = Field(..., description="Surrounding buildings")
    terrain: Dict[str, Any] = Field(..., description="Terrain data")
    model_3d: Dict[str, Any] = Field(..., description="3D model data")
    view_angles: List[Dict[str, Any]] = Field(..., description="View angles")
    context_analysis: Dict[str, Any] = Field(..., description="Context analysis")

# Project Schemas
class ProjectRequest(BaseModel):
    name: str = Field(..., description="Project name")
    type: ProjectType = Field(..., description="Project type")
    surface_area: float = Field(..., description="Surface area in square meters")
    location: LocationRequest = Field(..., description="Project location")
    requirements: Dict[str, Any] = Field(..., description="Project requirements")

class ProjectResponse(BaseModel):
    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    type: ProjectType = Field(..., description="Project type")
    surface_area: float = Field(..., description="Surface area")
    location: LocationRequest = Field(..., description="Project location")
    requirements: Dict[str, Any] = Field(..., description="Project requirements")
    status: DesignStatus = Field(..., description="Project status")
    created_at: datetime = Field(..., description="Creation timestamp")
    designs: Dict[str, Any] = Field(..., description="Design data")

# Design Schemas
class DesignRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    climate_data: ClimateData = Field(..., description="Climate data")
    architectural_style: ArchitecturalStyle = Field(..., description="Architectural style")
    surroundings_3d: Optional[Surroundings3D] = Field(None, description="3D surroundings")

class Design2D(BaseModel):
    floor_plan: Dict[str, Any] = Field(..., description="Floor plan data")
    elevations: Dict[str, Any] = Field(..., description="Building elevations")
    sections: Dict[str, Any] = Field(..., description="Building sections")
    design_parameters: Dict[str, Any] = Field(..., description="Design parameters")

class Design3D(BaseModel):
    model_3d: Dict[str, Any] = Field(..., description="3D model data")
    materials: Dict[str, Any] = Field(..., description="Materials data")
    lighting: Dict[str, Any] = Field(..., description="Lighting data")
    landscaping: Dict[str, Any] = Field(..., description="Landscaping data")
    viewpoints: List[Dict[str, Any]] = Field(..., description="Viewpoints")

class StructuralDesign(BaseModel):
    analysis: Dict[str, Any] = Field(..., description="Structural analysis")
    foundation: Dict[str, Any] = Field(..., description="Foundation design")
    frame: Dict[str, Any] = Field(..., description="Structural frame")
    roof: Dict[str, Any] = Field(..., description="Roof structure")
    connections: Dict[str, Any] = Field(..., description="Structural connections")
    drawings: Dict[str, Any] = Field(..., description="Structural drawings")
    specifications: Dict[str, Any] = Field(..., description="Structural specifications")

class MEPDesign(BaseModel):
    electrical: Dict[str, Any] = Field(..., description="Electrical design")
    plumbing: Dict[str, Any] = Field(..., description="Plumbing design")
    hvac: Dict[str, Any] = Field(..., description="HVAC design")
    fire_protection: Dict[str, Any] = Field(..., description="Fire protection design")
    drawings: Dict[str, Any] = Field(..., description="MEP drawings")
    specifications: Dict[str, Any] = Field(..., description="MEP specifications")

# Modification Schemas
class ModificationRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    text_command: str = Field(..., description="Natural language modification command")
    modification_type: ModificationType = Field(..., description="Type of modification")

class ModificationResponse(BaseModel):
    modified_design: Dict[str, Any] = Field(..., description="Modified design data")
    modification: Dict[str, Any] = Field(..., description="Modification details")
    project_id: str = Field(..., description="Project ID")

# Export Schemas
class ExportRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    export_format: ExportFormat = Field(..., description="Export format")
    software_type: SoftwareType = Field(..., description="Target software")

class ExportResponse(BaseModel):
    export_url: str = Field(..., description="Export file URL")
    format: ExportFormat = Field(..., description="Export format")
    software: SoftwareType = Field(..., description="Target software")

# Cost Estimation Schemas
class CostRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    region: str = Field(..., description="Cost region")
    currency: str = Field(..., description="Currency code")

class CostEstimate(BaseModel):
    total_cost: float = Field(..., description="Total project cost")
    breakdown: Dict[str, Any] = Field(..., description="Cost breakdown")
    materials: Dict[str, Any] = Field(..., description="Material costs")
    labor: Dict[str, Any] = Field(..., description="Labor costs")
    equipment: Dict[str, Any] = Field(..., description="Equipment costs")
    overhead: Dict[str, Any] = Field(..., description="Overhead costs")
    excel_url: str = Field(..., description="Excel file URL")

class CostResponse(BaseModel):
    cost_estimate: CostEstimate = Field(..., description="Cost estimate data")
    excel_url: str = Field(..., description="Excel file URL")
    project_id: str = Field(..., description="Project ID")

# Portfolio Schemas
class PortfolioFile(BaseModel):
    filename: str = Field(..., description="File name")
    content_type: str = Field(..., description="File content type")
    size: int = Field(..., description="File size in bytes")
    processed: bool = Field(..., description="Processing status")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Analysis results")

class PortfolioData(BaseModel):
    files: List[PortfolioFile] = Field(..., description="Portfolio files")
    styles: List[str] = Field(..., description="Detected styles")
    elements: List[str] = Field(..., description="Architectural elements")

# API Response Schemas
class APIResponse(BaseModel):
    success: bool = Field(..., description="Success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message")

class HealthCheck(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")

# Error Schemas
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: str = Field(..., description="Error details")
    status_code: int = Field(..., description="HTTP status code")

# File Upload Schemas
class FileUpload(BaseModel):
    filename: str = Field(..., description="File name")
    content_type: str = Field(..., description="File content type")
    size: int = Field(..., description="File size in bytes")

# Database Schemas
class ProjectDB(BaseModel):
    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    type: ProjectType = Field(..., description="Project type")
    surface_area: float = Field(..., description="Surface area")
    location: Dict[str, Any] = Field(..., description="Project location")
    requirements: Dict[str, Any] = Field(..., description="Project requirements")
    status: DesignStatus = Field(..., description="Project status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    designs: Dict[str, Any] = Field(..., description="Design data")
    portfolio: Optional[Dict[str, Any]] = Field(None, description="Portfolio data")

class DesignDB(BaseModel):
    id: str = Field(..., description="Design ID")
    project_id: str = Field(..., description="Project ID")
    design_type: str = Field(..., description="Design type")
    design_data: Dict[str, Any] = Field(..., description="Design data")
    created_at: datetime = Field(..., description="Creation timestamp")
    modified_at: datetime = Field(..., description="Last modification timestamp")

# Configuration Schemas
class APIConfig(BaseModel):
    openweather_api_key: str = Field(..., description="OpenWeather API key")
    google_maps_api_key: str = Field(..., description="Google Maps API key")
    mapbox_api_key: str = Field(..., description="Mapbox API key")
    climate_api_key: str = Field(..., description="Climate API key")
    database_url: str = Field(..., description="Database URL")
    redis_url: str = Field(..., description="Redis URL")

class DatabaseConfig(BaseModel):
    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    name: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")

# Validation Schemas
class ValidationError(BaseModel):
    field: str = Field(..., description="Field name")
    message: str = Field(..., description="Validation message")
    value: Any = Field(..., description="Invalid value")

class ValidationResponse(BaseModel):
    valid: bool = Field(..., description="Validation status")
    errors: List[ValidationError] = Field(..., description="Validation errors")

# Search and Filter Schemas
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")
    limit: int = Field(10, description="Result limit")
    offset: int = Field(0, description="Result offset")

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Search results")
    total: int = Field(..., description="Total results")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")

# Notification Schemas
class Notification(BaseModel):
    id: str = Field(..., description="Notification ID")
    type: str = Field(..., description="Notification type")
    message: str = Field(..., description="Notification message")
    timestamp: datetime = Field(..., description="Notification timestamp")
    read: bool = Field(False, description="Read status")

class NotificationRequest(BaseModel):
    type: str = Field(..., description="Notification type")
    message: str = Field(..., description="Notification message")
    user_id: str = Field(..., description="User ID")

# Analytics Schemas
class AnalyticsData(BaseModel):
    project_id: str = Field(..., description="Project ID")
    metric: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    timestamp: datetime = Field(..., description="Metric timestamp")

class AnalyticsRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    start_date: datetime = Field(..., description="Start date")
    end_date: datetime = Field(..., description="End date")
    metrics: List[str] = Field(..., description="Metrics to retrieve")

class AnalyticsResponse(BaseModel):
    project_id: str = Field(..., description="Project ID")
    metrics: List[AnalyticsData] = Field(..., description="Analytics data")
    summary: Dict[str, Any] = Field(..., description="Summary statistics")
