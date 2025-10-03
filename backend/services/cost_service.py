"""
Cost Service - Handles cost estimation and Excel export
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from utils.cost_calculator import CostCalculator
from utils.excel_generator import ExcelGenerator

class CostService:
    def __init__(self):
        self.cost_calculator = CostCalculator()
        self.excel_generator = ExcelGenerator()
        self.cost_storage = "cost_estimates"  # Directory for cost files
        
    async def generate_cost_estimate(
        self, 
        project_id: str, 
        region: str, 
        currency: str
    ) -> Dict[str, Any]:
        """Generate cost estimate for project"""
        
        # Get project data
        project_data = await self._get_project_data(project_id)
        if not project_data:
            raise ValueError("Project not found")
        
        # Get design data
        design_data = await self._get_design_data(project_id)
        
        # Calculate costs
        cost_breakdown = await self._calculate_cost_breakdown(
            project_data, design_data, region, currency
        )
        
        # Generate Excel file
        excel_url = await self._generate_excel_file(
            cost_breakdown, project_id, region, currency
        )
        
        # Create cost estimate record
        cost_estimate = await self._create_cost_estimate_record(
            project_id, cost_breakdown, excel_url
        )
        
        return {
            "cost_estimate": cost_breakdown,
            "excel_url": excel_url,
            "project_id": project_id,
            "region": region,
            "currency": currency,
            "created_at": datetime.now().isoformat()
        }
    
    async def _get_project_data(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project data from database"""
        # This would typically query the database
        # For now, we'll return simulated data
        return {
            "id": project_id,
            "name": "Sample Project",
            "type": "residential",
            "surface_area": 100,
            "location": {"address": "123 Main St", "postal_code": "12345"},
            "requirements": {"rooms": 3, "bathrooms": 2}
        }
    
    async def _get_design_data(self, project_id: str) -> Dict[str, Any]:
        """Get design data for cost calculation"""
        # This would typically get design data from the database
        # For now, we'll return simulated design data
        return {
            "2d_design": {
                "floor_plan": {
                    "rooms": [
                        {"name": "Living Room", "area": 25, "type": "living"},
                        {"name": "Kitchen", "area": 15, "type": "kitchen"},
                        {"name": "Bedroom", "area": 20, "type": "bedroom"},
                        {"name": "Bathroom", "area": 8, "type": "bathroom"}
                    ]
                }
            },
            "3d_design": {
                "model_3d": {
                    "dimensions": [10, 10, 3.5],
                    "materials": ["brick", "glass", "steel"]
                }
            },
            "structural_design": {
                "foundation": {"type": "shallow", "area": 100},
                "frame": {"type": "steel_frame", "beams": 4, "columns": 8}
            },
            "mep_design": {
                "electrical": {"loads": 5000, "fixtures": 20},
                "plumbing": {"fixtures": 8, "pipes": 50},
                "hvac": {"heating": 2, "cooling": 2}
            }
        }
    
    async def _calculate_cost_breakdown(
        self, 
        project_data: Dict[str, Any], 
        design_data: Dict[str, Any], 
        region: str, 
        currency: str
    ) -> Dict[str, Any]:
        """Calculate detailed cost breakdown"""
        
        # Get regional cost factors
        regional_factors = await self._get_regional_factors(region)
        
        # Calculate material costs
        material_costs = await self._calculate_material_costs(
            design_data, regional_factors, currency
        )
        
        # Calculate labor costs
        labor_costs = await self._calculate_labor_costs(
            design_data, regional_factors, currency
        )
        
        # Calculate equipment costs
        equipment_costs = await self._calculate_equipment_costs(
            design_data, regional_factors, currency
        )
        
        # Calculate overhead costs
        overhead_costs = await self._calculate_overhead_costs(
            material_costs, labor_costs, equipment_costs, regional_factors
        )
        
        # Calculate total costs
        total_cost = (
            material_costs["total"] + 
            labor_costs["total"] + 
            equipment_costs["total"] + 
            overhead_costs["total"]
        )
        
        return {
            "total_cost": total_cost,
            "currency": currency,
            "region": region,
            "breakdown": {
                "materials": material_costs,
                "labor": labor_costs,
                "equipment": equipment_costs,
                "overhead": overhead_costs
            },
            "summary": await self._generate_cost_summary(
                total_cost, material_costs, labor_costs, equipment_costs, overhead_costs
            )
        }
    
    async def _get_regional_factors(self, region: str) -> Dict[str, float]:
        """Get regional cost factors"""
        # This would typically query a cost database
        # For now, we'll return simulated factors
        regional_factors = {
            "north_america": {
                "material_factor": 1.0,
                "labor_factor": 1.0,
                "equipment_factor": 1.0,
                "overhead_factor": 1.2
            },
            "europe": {
                "material_factor": 1.1,
                "labor_factor": 1.2,
                "equipment_factor": 1.1,
                "overhead_factor": 1.3
            },
            "asia": {
                "material_factor": 0.8,
                "labor_factor": 0.6,
                "equipment_factor": 0.9,
                "overhead_factor": 1.1
            }
        }
        
        return regional_factors.get(region, regional_factors["north_america"])
    
    async def _calculate_material_costs(
        self, 
        design_data: Dict[str, Any], 
        regional_factors: Dict[str, float], 
        currency: str
    ) -> Dict[str, Any]:
        """Calculate material costs"""
        
        # Get material quantities
        material_quantities = await self._calculate_material_quantities(design_data)
        
        # Get material unit costs
        material_unit_costs = await self._get_material_unit_costs(currency)
        
        # Calculate costs for each material
        material_costs = {}
        total_material_cost = 0
        
        for material, quantity in material_quantities.items():
            unit_cost = material_unit_costs.get(material, 0)
            regional_cost = unit_cost * regional_factors["material_factor"]
            total_cost = quantity * regional_cost
            
            material_costs[material] = {
                "quantity": quantity,
                "unit_cost": regional_cost,
                "total_cost": total_cost
            }
            
            total_material_cost += total_cost
        
        return {
            "materials": material_costs,
            "total": total_material_cost,
            "currency": currency
        }
    
    async def _calculate_material_quantities(self, design_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate material quantities from design data"""
        quantities = {}
        
        # Calculate wall materials
        if "2d_design" in design_data and "floor_plan" in design_data["2d_design"]:
            floor_plan = design_data["2d_design"]["floor_plan"]
            if "rooms" in floor_plan:
                total_area = sum([room["area"] for room in floor_plan["rooms"]])
                
                # Estimate materials based on area
                quantities["brick"] = total_area * 0.1  # m³
                quantities["concrete"] = total_area * 0.05  # m³
                quantities["steel"] = total_area * 0.02  # tons
                quantities["glass"] = total_area * 0.1  # m²
                quantities["wood"] = total_area * 0.05  # m³
        
        # Calculate MEP materials
        if "mep_design" in design_data:
            mep_design = design_data["mep_design"]
            
            # Electrical materials
            if "electrical" in mep_design:
                electrical = mep_design["electrical"]
                quantities["electrical_wire"] = electrical.get("loads", 0) * 0.1  # meters
                quantities["electrical_fixtures"] = electrical.get("fixtures", 0)
            
            # Plumbing materials
            if "plumbing" in mep_design:
                plumbing = mep_design["plumbing"]
                quantities["plumbing_pipes"] = plumbing.get("pipes", 0)  # meters
                quantities["plumbing_fixtures"] = plumbing.get("fixtures", 0)
        
        return quantities
    
    async def _get_material_unit_costs(self, currency: str) -> Dict[str, float]:
        """Get material unit costs"""
        # This would typically query a cost database
        # For now, we'll return simulated costs
        unit_costs = {
            "brick": 50,  # per m³
            "concrete": 100,  # per m³
            "steel": 800,  # per ton
            "glass": 200,  # per m²
            "wood": 300,  # per m³
            "electrical_wire": 5,  # per meter
            "electrical_fixtures": 50,  # per fixture
            "plumbing_pipes": 10,  # per meter
            "plumbing_fixtures": 200  # per fixture
        }
        
        # Convert currency if needed
        if currency == "EUR":
            for material in unit_costs:
                unit_costs[material] *= 0.85  # USD to EUR conversion
        elif currency == "GBP":
            for material in unit_costs:
                unit_costs[material] *= 0.75  # USD to GBP conversion
        
        return unit_costs
    
    async def _calculate_labor_costs(
        self, 
        design_data: Dict[str, Any], 
        regional_factors: Dict[str, float], 
        currency: str
    ) -> Dict[str, Any]:
        """Calculate labor costs"""
        
        # Get labor hours
        labor_hours = await self._calculate_labor_hours(design_data)
        
        # Get labor rates
        labor_rates = await self._get_labor_rates(currency)
        
        # Calculate costs for each trade
        labor_costs = {}
        total_labor_cost = 0
        
        for trade, hours in labor_hours.items():
            rate = labor_rates.get(trade, 0)
            regional_rate = rate * regional_factors["labor_factor"]
            total_cost = hours * regional_rate
            
            labor_costs[trade] = {
                "hours": hours,
                "rate": regional_rate,
                "total_cost": total_cost
            }
            
            total_labor_cost += total_cost
        
        return {
            "trades": labor_costs,
            "total": total_labor_cost,
            "currency": currency
        }
    
    async def _calculate_labor_hours(self, design_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate labor hours from design data"""
        hours = {}
        
        # Calculate construction hours
        if "2d_design" in design_data and "floor_plan" in design_data["2d_design"]:
            floor_plan = design_data["2d_design"]["floor_plan"]
            if "rooms" in floor_plan:
                total_area = sum([room["area"] for room in floor_plan["rooms"]])
                
                # Estimate hours based on area
                hours["carpenter"] = total_area * 2  # hours per m²
                hours["electrician"] = total_area * 1.5
                hours["plumber"] = total_area * 1
                hours["painter"] = total_area * 1.5
                hours["mason"] = total_area * 3
        
        # Calculate MEP hours
        if "mep_design" in design_data:
            mep_design = design_data["mep_design"]
            
            # Electrical hours
            if "electrical" in mep_design:
                electrical = mep_design["electrical"]
                hours["electrician"] += electrical.get("fixtures", 0) * 2
            
            # Plumbing hours
            if "plumbing" in mep_design:
                plumbing = mep_design["plumbing"]
                hours["plumber"] += plumbing.get("fixtures", 0) * 3
        
        return hours
    
    async def _get_labor_rates(self, currency: str) -> Dict[str, float]:
        """Get labor rates"""
        # This would typically query a cost database
        # For now, we'll return simulated rates
        rates = {
            "carpenter": 50,  # per hour
            "electrician": 60,
            "plumber": 55,
            "painter": 40,
            "mason": 45
        }
        
        # Convert currency if needed
        if currency == "EUR":
            for trade in rates:
                rates[trade] *= 0.85  # USD to EUR conversion
        elif currency == "GBP":
            for trade in rates:
                rates[trade] *= 0.75  # USD to GBP conversion
        
        return rates
    
    async def _calculate_equipment_costs(
        self, 
        design_data: Dict[str, Any], 
        regional_factors: Dict[str, float], 
        currency: str
    ) -> Dict[str, Any]:
        """Calculate equipment costs"""
        
        # Get equipment requirements
        equipment_requirements = await self._calculate_equipment_requirements(design_data)
        
        # Get equipment rates
        equipment_rates = await self._get_equipment_rates(currency)
        
        # Calculate costs for each equipment
        equipment_costs = {}
        total_equipment_cost = 0
        
        for equipment, days in equipment_requirements.items():
            rate = equipment_rates.get(equipment, 0)
            regional_rate = rate * regional_factors["equipment_factor"]
            total_cost = days * regional_rate
            
            equipment_costs[equipment] = {
                "days": days,
                "rate": regional_rate,
                "total_cost": total_cost
            }
            
            total_equipment_cost += total_cost
        
        return {
            "equipment": equipment_costs,
            "total": total_equipment_cost,
            "currency": currency
        }
    
    async def _calculate_equipment_requirements(self, design_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate equipment requirements"""
        requirements = {}
        
        # Calculate construction equipment
        if "2d_design" in design_data and "floor_plan" in design_data["2d_design"]:
            floor_plan = design_data["2d_design"]["floor_plan"]
            if "rooms" in floor_plan:
                total_area = sum([room["area"] for room in floor_plan["rooms"]])
                
                # Estimate equipment days based on area
                requirements["excavator"] = total_area * 0.1  # days per m²
                requirements["crane"] = total_area * 0.05
                requirements["concrete_mixer"] = total_area * 0.2
                requirements["scaffolding"] = total_area * 0.3
        
        return requirements
    
    async def _get_equipment_rates(self, currency: str) -> Dict[str, float]:
        """Get equipment rates"""
        # This would typically query a cost database
        # For now, we'll return simulated rates
        rates = {
            "excavator": 500,  # per day
            "crane": 800,
            "concrete_mixer": 200,
            "scaffolding": 100
        }
        
        # Convert currency if needed
        if currency == "EUR":
            for equipment in rates:
                rates[equipment] *= 0.85  # USD to EUR conversion
        elif currency == "GBP":
            for equipment in rates:
                rates[equipment] *= 0.75  # USD to GBP conversion
        
        return rates
    
    async def _calculate_overhead_costs(
        self, 
        material_costs: Dict[str, Any], 
        labor_costs: Dict[str, Any], 
        equipment_costs: Dict[str, Any], 
        regional_factors: Dict[str, float]
    ) -> Dict[str, Any]:
        """Calculate overhead costs"""
        
        # Calculate base costs
        base_costs = (
            material_costs["total"] + 
            labor_costs["total"] + 
            equipment_costs["total"]
        )
        
        # Calculate overhead percentage
        overhead_percentage = 15  # 15% overhead
        regional_overhead = overhead_percentage * regional_factors["overhead_factor"]
        
        # Calculate overhead costs
        overhead_costs = {
            "percentage": regional_overhead,
            "base_costs": base_costs,
            "overhead_amount": base_costs * (regional_overhead / 100),
            "total": base_costs * (1 + regional_overhead / 100)
        }
        
        return overhead_costs
    
    async def _generate_cost_summary(
        self, 
        total_cost: float, 
        material_costs: Dict[str, Any], 
        labor_costs: Dict[str, Any], 
        equipment_costs: Dict[str, Any], 
        overhead_costs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate cost summary"""
        
        return {
            "total_cost": total_cost,
            "cost_distribution": {
                "materials": {
                    "amount": material_costs["total"],
                    "percentage": (material_costs["total"] / total_cost) * 100
                },
                "labor": {
                    "amount": labor_costs["total"],
                    "percentage": (labor_costs["total"] / total_cost) * 100
                },
                "equipment": {
                    "amount": equipment_costs["total"],
                    "percentage": (equipment_costs["total"] / total_cost) * 100
                },
                "overhead": {
                    "amount": overhead_costs["overhead_amount"],
                    "percentage": (overhead_costs["overhead_amount"] / total_cost) * 100
                }
            },
            "cost_per_sqm": total_cost / 100,  # Assuming 100 m²
            "recommendations": await self._generate_cost_recommendations(
                material_costs, labor_costs, equipment_costs
            )
        }
    
    async def _generate_cost_recommendations(
        self, 
        material_costs: Dict[str, Any], 
        labor_costs: Dict[str, Any], 
        equipment_costs: Dict[str, Any]
    ) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        # Material recommendations
        if material_costs["total"] > labor_costs["total"]:
            recommendations.append("Consider using more cost-effective materials")
        
        # Labor recommendations
        if labor_costs["total"] > material_costs["total"]:
            recommendations.append("Consider prefabricated components to reduce labor costs")
        
        # Equipment recommendations
        if equipment_costs["total"] > material_costs["total"] * 0.5:
            recommendations.append("Consider renting equipment instead of purchasing")
        
        return recommendations
    
    async def _generate_excel_file(
        self, 
        cost_breakdown: Dict[str, Any], 
        project_id: str, 
        region: str, 
        currency: str
    ) -> str:
        """Generate Excel file with cost breakdown"""
        
        # Create cost directory if it doesn't exist
        cost_dir = os.path.join(self.cost_storage, project_id)
        os.makedirs(cost_dir, exist_ok=True)
        
        # Generate Excel content
        excel_content = await self.excel_generator.generate_cost_excel(
            cost_breakdown, project_id, region, currency
        )
        
        # Save Excel file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cost_estimate_{timestamp}.xlsx"
        file_path = os.path.join(cost_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(excel_content)
        
        # Return file URL
        return f"/cost_estimates/{project_id}/{filename}"
    
    async def _create_cost_estimate_record(
        self, 
        project_id: str, 
        cost_breakdown: Dict[str, Any], 
        excel_url: str
    ) -> Dict[str, Any]:
        """Create cost estimate record in database"""
        
        # This would typically save to database
        # For now, we'll return a simulated record
        return {
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "cost_data": cost_breakdown,
            "excel_url": excel_url,
            "created_at": datetime.now().isoformat()
        }
    
    async def get_cost_history(self, project_id: str) -> List[Dict[str, Any]]:
        """Get cost estimation history for a project"""
        
        # This would typically query the database
        # For now, we'll return simulated data
        return [
            {
                "id": str(uuid.uuid4()),
                "project_id": project_id,
                "total_cost": 150000,
                "currency": "USD",
                "region": "north_america",
                "excel_url": f"/cost_estimates/{project_id}/cost_estimate_20240101_120000.xlsx",
                "created_at": "2024-01-01T12:00:00Z"
            }
        ]
    
    async def update_cost_estimate(
        self, 
        cost_estimate_id: str, 
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update cost estimate"""
        
        # This would typically update the database
        # For now, we'll return a simulated response
        return {
            "id": cost_estimate_id,
            "updated": True,
            "updated_at": datetime.now().isoformat()
        }
    
    async def delete_cost_estimate(self, cost_estimate_id: str) -> bool:
        """Delete cost estimate"""
        
        # This would typically delete from database and file system
        # For now, we'll return True
        return True
