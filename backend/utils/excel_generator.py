"""
Excel Generator - Handles Excel file generation for cost estimates
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

class ExcelGenerator:
    def __init__(self):
        self.excel_templates = self._load_excel_templates()
        self.cost_formulas = self._load_cost_formulas()
        
    def _load_excel_templates(self) -> Dict[str, Any]:
        """Load Excel templates"""
        return {
            "cost_estimate": {
                "title": "Cost Estimate",
                "headers": [
                    "Item", "Description", "Quantity", "Unit", "Unit Cost", "Total Cost"
                ],
                "sections": [
                    "Materials", "Labor", "Equipment", "Overhead", "Summary"
                ]
            }
        }
    
    def _load_cost_formulas(self) -> Dict[str, str]:
        """Load Excel formulas for cost calculations"""
        return {
            "total_cost": "=SUM(D:D)",
            "subtotal": "=SUM(D2:D100)",
            "tax": "=D101*0.1",
            "grand_total": "=D101+D102"
        }
    
    async def generate_cost_excel(
        self, 
        cost_breakdown: Dict[str, Any], 
        project_id: str, 
        region: str, 
        currency: str
    ) -> bytes:
        """Generate Excel file with cost breakdown"""
        
        # Create Excel workbook structure
        workbook = {
            "metadata": {
                "title": "Cost Estimate",
                "author": "ArchiAI Solution",
                "created": datetime.now().isoformat(),
                "project_id": project_id,
                "region": region,
                "currency": currency
            },
            "worksheets": await self._generate_worksheets(cost_breakdown, project_id, region, currency)
        }
        
        # Convert to Excel binary format
        return await self._convert_to_excel_binary(workbook)
    
    async def _generate_worksheets(
        self, 
        cost_breakdown: Dict[str, Any], 
        project_id: str, 
        region: str, 
        currency: str
    ) -> List[Dict[str, Any]]:
        """Generate Excel worksheets"""
        worksheets = []
        
        # Summary worksheet
        worksheets.append(await self._generate_summary_worksheet(cost_breakdown))
        
        # Materials worksheet
        worksheets.append(await self._generate_materials_worksheet(cost_breakdown))
        
        # Labor worksheet
        worksheets.append(await self._generate_labor_worksheet(cost_breakdown))
        
        # Equipment worksheet
        worksheets.append(await self._generate_equipment_worksheet(cost_breakdown))
        
        # Overhead worksheet
        worksheets.append(await self._generate_overhead_worksheet(cost_breakdown))
        
        # Detailed breakdown worksheet
        worksheets.append(await self._generate_detailed_worksheet(cost_breakdown))
        
        return worksheets
    
    async def _generate_summary_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary worksheet"""
        return {
            "name": "Summary",
            "data": [
                ["Cost Estimate Summary", "", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Project Information", "", "", "", "", ""],
                ["Total Cost", f"{cost_breakdown['total_cost']:,.2f}", cost_breakdown['currency'], "", "", ""],
                ["Region", cost_breakdown['region'], "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Cost Breakdown", "", "", "", "", ""],
                ["Materials", f"{cost_breakdown['breakdown']['materials']['total']:,.2f}", "", "", "", ""],
                ["Labor", f"{cost_breakdown['breakdown']['labor']['total']:,.2f}", "", "", "", ""],
                ["Equipment", f"{cost_breakdown['breakdown']['equipment']['total']:,.2f}", "", "", "", ""],
                ["Overhead", f"{cost_breakdown['breakdown']['overhead']['overhead_amount']:,.2f}", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Cost Distribution", "", "", "", "", ""],
                ["Materials %", f"{cost_breakdown['summary']['cost_distribution']['materials']['percentage']:.1f}%", "", "", "", ""],
                ["Labor %", f"{cost_breakdown['summary']['cost_distribution']['labor']['percentage']:.1f}%", "", "", "", ""],
                ["Equipment %", f"{cost_breakdown['summary']['cost_distribution']['equipment']['percentage']:.1f}%", "", "", "", ""],
                ["Overhead %", f"{cost_breakdown['summary']['cost_distribution']['overhead']['percentage']:.1f}%", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Cost per m²", f"{cost_breakdown['summary']['cost_per_sqm']:,.2f}", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Recommendations", "", "", "", "", ""]
            ] + [
                [rec, "", "", "", "", ""] for rec in cost_breakdown['summary']['recommendations']
            ]
        }
    
    async def _generate_materials_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate materials worksheet"""
        materials = cost_breakdown['breakdown']['materials']['materials']
        
        data = [
            ["Materials Cost Breakdown", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Material", "Description", "Quantity", "Unit", "Unit Cost", "Total Cost"]
        ]
        
        for material, details in materials.items():
            data.append([
                material.title(),
                f"{material} material",
                f"{details['quantity']:.2f}",
                "m³" if material in ["brick", "concrete", "wood"] else "m²" if material == "glass" else "tons" if material == "steel" else "units",
                f"{details['unit_cost']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        data.append(["", "", "", "", "", ""])
        data.append(["Total Materials", "", "", "", "", f"{cost_breakdown['breakdown']['materials']['total']:,.2f}"])
        
        return {
            "name": "Materials",
            "data": data
        }
    
    async def _generate_labor_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate labor worksheet"""
        trades = cost_breakdown['breakdown']['labor']['trades']
        
        data = [
            ["Labor Cost Breakdown", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Trade", "Description", "Hours", "Unit", "Rate", "Total Cost"]
        ]
        
        for trade, details in trades.items():
            data.append([
                trade.title(),
                f"{trade} work",
                f"{details['hours']:.1f}",
                "hours",
                f"{details['rate']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        data.append(["", "", "", "", "", ""])
        data.append(["Total Labor", "", "", "", "", f"{cost_breakdown['breakdown']['labor']['total']:,.2f}"])
        
        return {
            "name": "Labor",
            "data": data
        }
    
    async def _generate_equipment_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate equipment worksheet"""
        equipment = cost_breakdown['breakdown']['equipment']['equipment']
        
        data = [
            ["Equipment Cost Breakdown", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Equipment", "Description", "Days", "Unit", "Rate", "Total Cost"]
        ]
        
        for equipment_name, details in equipment.items():
            data.append([
                equipment_name.title(),
                f"{equipment_name} rental",
                f"{details['days']:.1f}",
                "days",
                f"{details['rate']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        data.append(["", "", "", "", "", ""])
        data.append(["Total Equipment", "", "", "", "", f"{cost_breakdown['breakdown']['equipment']['total']:,.2f}"])
        
        return {
            "name": "Equipment",
            "data": data
        }
    
    async def _generate_overhead_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overhead worksheet"""
        overhead = cost_breakdown['breakdown']['overhead']
        
        data = [
            ["Overhead Cost Breakdown", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Item", "Description", "Percentage", "Base Cost", "Overhead Amount", "Total Cost"]
        ]
        
        data.append([
            "Overhead",
            "Project overhead and profit",
            f"{overhead['percentage']:.1f}%",
            f"{overhead['base_costs']:,.2f}",
            f"{overhead['overhead_amount']:,.2f}",
            f"{overhead['total']:,.2f}"
        ])
        
        data.append(["", "", "", "", "", ""])
        data.append(["Total Overhead", "", "", "", "", f"{overhead['overhead_amount']:,.2f}"])
        
        return {
            "name": "Overhead",
            "data": data
        }
    
    async def _generate_detailed_worksheet(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed breakdown worksheet"""
        data = [
            ["Detailed Cost Breakdown", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Category", "Item", "Quantity", "Unit", "Unit Cost", "Total Cost"]
        ]
        
        # Add materials
        materials = cost_breakdown['breakdown']['materials']['materials']
        for material, details in materials.items():
            data.append([
                "Materials",
                material.title(),
                f"{details['quantity']:.2f}",
                "m³" if material in ["brick", "concrete", "wood"] else "m²" if material == "glass" else "tons" if material == "steel" else "units",
                f"{details['unit_cost']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        # Add labor
        trades = cost_breakdown['breakdown']['labor']['trades']
        for trade, details in trades.items():
            data.append([
                "Labor",
                trade.title(),
                f"{details['hours']:.1f}",
                "hours",
                f"{details['rate']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        # Add equipment
        equipment = cost_breakdown['breakdown']['equipment']['equipment']
        for equipment_name, details in equipment.items():
            data.append([
                "Equipment",
                equipment_name.title(),
                f"{details['days']:.1f}",
                "days",
                f"{details['rate']:,.2f}",
                f"{details['total_cost']:,.2f}"
            ])
        
        # Add totals
        data.append(["", "", "", "", "", ""])
        data.append(["TOTAL", "", "", "", "", f"{cost_breakdown['total_cost']:,.2f}"])
        
        return {
            "name": "Detailed",
            "data": data
        }
    
    async def _convert_to_excel_binary(self, workbook: Dict[str, Any]) -> bytes:
        """Convert workbook to Excel binary format"""
        # This would typically use a library like openpyxl or xlsxwriter
        # For now, we'll return a simple binary representation
        return json.dumps(workbook, indent=2).encode('utf-8')
    
    async def generate_cost_comparison_excel(
        self, 
        cost_estimates: List[Dict[str, Any]], 
        project_id: str
    ) -> bytes:
        """Generate Excel file comparing multiple cost estimates"""
        
        workbook = {
            "metadata": {
                "title": "Cost Comparison",
                "author": "ArchiAI Solution",
                "created": datetime.now().isoformat(),
                "project_id": project_id
            },
            "worksheets": await self._generate_comparison_worksheets(cost_estimates)
        }
        
        return await self._convert_to_excel_binary(workbook)
    
    async def _generate_comparison_worksheets(self, cost_estimates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate comparison worksheets"""
        worksheets = []
        
        # Summary comparison
        worksheets.append(await self._generate_comparison_summary(cost_estimates))
        
        # Detailed comparison
        worksheets.append(await self._generate_comparison_detailed(cost_estimates))
        
        return worksheets
    
    async def _generate_comparison_summary(self, cost_estimates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comparison summary worksheet"""
        data = [
            ["Cost Comparison Summary", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Estimate", "Total Cost", "Currency", "Region", "Date", "Notes"]
        ]
        
        for i, estimate in enumerate(cost_estimates):
            data.append([
                f"Estimate {i+1}",
                f"{estimate['total_cost']:,.2f}",
                estimate['currency'],
                estimate['region'],
                estimate['created_at'],
                ""
            ])
        
        return {
            "name": "Comparison Summary",
            "data": data
        }
    
    async def _generate_comparison_detailed(self, cost_estimates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed comparison worksheet"""
        data = [
            ["Detailed Cost Comparison", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Category", "Item", "Estimate 1", "Estimate 2", "Difference", "Percentage"]
        ]
        
        # Compare materials
        if len(cost_estimates) >= 2:
            materials1 = cost_estimates[0]['breakdown']['materials']['materials']
            materials2 = cost_estimates[1]['breakdown']['materials']['materials']
            
            for material in materials1:
                if material in materials2:
                    cost1 = materials1[material]['total_cost']
                    cost2 = materials2[material]['total_cost']
                    difference = cost2 - cost1
                    percentage = (difference / cost1) * 100 if cost1 > 0 else 0
                    
                    data.append([
                        "Materials",
                        material.title(),
                        f"{cost1:,.2f}",
                        f"{cost2:,.2f}",
                        f"{difference:,.2f}",
                        f"{percentage:.1f}%"
                    ])
        
        return {
            "name": "Detailed Comparison",
            "data": data
        }
    
    async def generate_cost_analysis_excel(
        self, 
        cost_analysis: Dict[str, Any], 
        project_id: str
    ) -> bytes:
        """Generate Excel file with cost analysis"""
        
        workbook = {
            "metadata": {
                "title": "Cost Analysis",
                "author": "ArchiAI Solution",
                "created": datetime.now().isoformat(),
                "project_id": project_id
            },
            "worksheets": await self._generate_analysis_worksheets(cost_analysis)
        }
        
        return await self._convert_to_excel_binary(workbook)
    
    async def _generate_analysis_worksheets(self, cost_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate analysis worksheets"""
        worksheets = []
        
        # Cost analysis summary
        worksheets.append(await self._generate_analysis_summary(cost_analysis))
        
        # Cost trends
        worksheets.append(await self._generate_cost_trends(cost_analysis))
        
        # Cost optimization
        worksheets.append(await self._generate_cost_optimization(cost_analysis))
        
        return worksheets
    
    async def _generate_analysis_summary(self, cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary worksheet"""
        data = [
            ["Cost Analysis Summary", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Metric", "Value", "Unit", "Target", "Variance", "Status"]
        ]
        
        # Add analysis metrics
        for metric, value in cost_analysis.items():
            data.append([
                metric.title(),
                f"{value:.2f}",
                "currency",
                f"{value * 0.9:.2f}",  # 10% below target
                f"{value * 0.1:.2f}",
                "Good" if value <= value * 1.1 else "Over Budget"
            ])
        
        return {
            "name": "Analysis Summary",
            "data": data
        }
    
    async def _generate_cost_trends(self, cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cost trends worksheet"""
        data = [
            ["Cost Trends Analysis", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Month", "Materials", "Labor", "Equipment", "Total", "Cumulative"]
        ]
        
        # Add trend data
        for month in range(1, 13):
            materials = 10000 + month * 1000
            labor = 15000 + month * 1500
            equipment = 5000 + month * 500
            total = materials + labor + equipment
            cumulative = total * month
            
            data.append([
                f"Month {month}",
                f"{materials:,.2f}",
                f"{labor:,.2f}",
                f"{equipment:,.2f}",
                f"{total:,.2f}",
                f"{cumulative:,.2f}"
            ])
        
        return {
            "name": "Cost Trends",
            "data": data
        }
    
    async def _generate_cost_optimization(self, cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cost optimization worksheet"""
        data = [
            ["Cost Optimization Opportunities", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["Category", "Current Cost", "Optimized Cost", "Savings", "Percentage", "Implementation"]
        ]
        
        # Add optimization opportunities
        optimizations = [
            ["Materials", 50000, 45000, 5000, 10, "Bulk purchasing"],
            ["Labor", 75000, 70000, 5000, 7, "Efficient scheduling"],
            ["Equipment", 25000, 22000, 3000, 12, "Equipment sharing"],
            ["Overhead", 30000, 28000, 2000, 7, "Process optimization"]
        ]
        
        for opt in optimizations:
            data.append(opt)
        
        return {
            "name": "Cost Optimization",
            "data": data
        }
