"""
MEP Service - Handles Mechanical, Electrical, and Plumbing design
"""

import numpy as np
from typing import Dict, Any, List, Tuple
import math

class MEPService:
    def __init__(self):
        self.electrical_codes = self._load_electrical_codes()
        self.plumbing_codes = self._load_plumbing_codes()
        self.hvac_codes = self._load_hvac_codes()
        
    def _load_electrical_codes(self) -> Dict[str, Any]:
        """Load electrical design codes"""
        return {
            "load_calculations": {
                "residential": 3.0,  # VA/ft²
                "office": 5.0,       # VA/ft²
                "retail": 8.0,       # VA/ft²
                "hospital": 10.0,    # VA/ft²
                "school": 6.0        # VA/ft²
            },
            "circuit_ratings": {
                "lighting": 15,      # A
                "receptacles": 20,   # A
                "appliances": 30,    # A
                "hvac": 40           # A
            },
            "voltage_levels": {
                "lighting": 120,     # V
                "receptacles": 120,  # V
                "appliances": 240,   # V
                "hvac": 240          # V
            }
        }
    
    def _load_plumbing_codes(self) -> Dict[str, Any]:
        """Load plumbing design codes"""
        return {
            "fixture_units": {
                "toilet": 3,
                "lavatory": 1,
                "shower": 2,
                "bathtub": 2,
                "kitchen_sink": 2,
                "dishwasher": 1,
                "washing_machine": 2
            },
            "pipe_sizes": {
                "main": 4,           # inches
                "branch": 2,         # inches
                "fixture": 0.5       # inches
            },
            "water_pressure": {
                "minimum": 20,       # psi
                "maximum": 80,       # psi
                "recommended": 40    # psi
            }
        }
    
    def _load_hvac_codes(self) -> Dict[str, Any]:
        """Load HVAC design codes"""
        return {
            "cooling_loads": {
                "residential": 1.0,  # ton/1000 ft²
                "office": 1.5,       # ton/1000 ft²
                "retail": 2.0,       # ton/1000 ft²
                "hospital": 2.5,     # ton/1000 ft²
                "school": 1.8        # ton/1000 ft²
            },
            "heating_loads": {
                "residential": 0.8,  # ton/1000 ft²
                "office": 1.2,       # ton/1000 ft²
                "retail": 1.5,       # ton/1000 ft²
                "hospital": 2.0,     # ton/1000 ft²
                "school": 1.3        # ton/1000 ft²
            },
            "ventilation_rates": {
                "residential": 0.35, # cfm/ft²
                "office": 0.5,       # cfm/ft²
                "retail": 0.3,       # cfm/ft²
                "hospital": 0.6,     # cfm/ft²
                "school": 0.4       # cfm/ft²
            }
        }
    
    async def generate_mep_design(
        self, 
        design_2d: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate MEP design based on 2D design and climate data"""
        
        # Generate electrical design
        electrical_design = await self._generate_electrical_design(design_2d, climate_data)
        
        # Generate plumbing design
        plumbing_design = await self._generate_plumbing_design(design_2d, climate_data)
        
        # Generate HVAC design
        hvac_design = await self._generate_hvac_design(design_2d, climate_data)
        
        # Generate fire protection design
        fire_protection = await self._generate_fire_protection_design(design_2d, climate_data)
        
        # Generate MEP drawings
        mep_drawings = await self._generate_mep_drawings(
            electrical_design, plumbing_design, hvac_design, fire_protection
        )
        
        return {
            "electrical": electrical_design,
            "plumbing": plumbing_design,
            "hvac": hvac_design,
            "fire_protection": fire_protection,
            "drawings": mep_drawings,
            "specifications": await self._generate_mep_specifications(design_2d, climate_data)
        }
    
    async def _generate_electrical_design(
        self, 
        design_2d: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate electrical design"""
        
        # Calculate electrical loads
        electrical_loads = await self._calculate_electrical_loads(design_2d, climate_data)
        
        # Design electrical distribution
        distribution = await self._design_electrical_distribution(electrical_loads)
        
        # Design lighting
        lighting = await self._design_lighting(design_2d, climate_data)
        
        # Design power systems
        power_systems = await self._design_power_systems(electrical_loads)
        
        # Design emergency systems
        emergency_systems = await self._design_emergency_systems(electrical_loads)
        
        return {
            "loads": electrical_loads,
            "distribution": distribution,
            "lighting": lighting,
            "power_systems": power_systems,
            "emergency_systems": emergency_systems,
            "specifications": await self._generate_electrical_specifications(electrical_loads)
        }
    
    async def _calculate_electrical_loads(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate electrical loads"""
        rooms = design_2d.get("rooms", {})
        total_area = sum([room.get("area", 0) for room in rooms.values()])
        
        # Determine occupancy type
        occupancy_type = "residential"  # Default
        if "office" in str(design_2d).lower():
            occupancy_type = "office"
        elif "retail" in str(design_2d).lower():
            occupancy_type = "retail"
        elif "hospital" in str(design_2d).lower():
            occupancy_type = "hospital"
        elif "school" in str(design_2d).lower():
            occupancy_type = "school"
        
        # Calculate base electrical load
        base_load = self.electrical_codes["load_calculations"][occupancy_type]
        total_electrical_load = base_load * total_area  # VA
        
        # Calculate room-specific loads
        room_loads = {}
        for room_name, room_data in rooms.items():
            room_area = room_data.get("area", 0)
            room_load = base_load * room_area
            room_loads[room_name] = {
                "area": room_area,
                "load": room_load,
                "circuits": await self._calculate_room_circuits(room_load)
            }
        
        # Calculate HVAC loads
        hvac_load = await self._calculate_hvac_electrical_load(design_2d, climate_data)
        
        # Calculate total load
        total_load = total_electrical_load + hvac_load
        
        return {
            "total_load": total_load,
            "base_load": total_electrical_load,
            "hvac_load": hvac_load,
            "room_loads": room_loads,
            "occupancy_type": occupancy_type
        }
    
    async def _calculate_room_circuits(self, room_load: float) -> List[Dict[str, Any]]:
        """Calculate electrical circuits for a room"""
        circuits = []
        
        # Lighting circuit
        lighting_load = room_load * 0.3  # 30% for lighting
        circuits.append({
            "type": "lighting",
            "load": lighting_load,
            "rating": 15,  # A
            "voltage": 120  # V
        })
        
        # Receptacle circuit
        receptacle_load = room_load * 0.7  # 70% for receptacles
        circuits.append({
            "type": "receptacles",
            "load": receptacle_load,
            "rating": 20,  # A
            "voltage": 120  # V
        })
        
        return circuits
    
    async def _calculate_hvac_electrical_load(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> float:
        """Calculate HVAC electrical load"""
        rooms = design_2d.get("rooms", {})
        total_area = sum([room.get("area", 0) for room in rooms.values()])
        
        # Get climate data
        current_weather = climate_data.get("current_weather", {})
        temperature = current_weather.get("temperature", 20)
        
        # Calculate HVAC load based on temperature
        if temperature > 25:
            hvac_load_factor = 2.0  # Cooling required
        elif temperature < 10:
            hvac_load_factor = 1.5  # Heating required
        else:
            hvac_load_factor = 1.0  # Minimal HVAC
        
        # Calculate HVAC electrical load
        hvac_electrical_load = total_area * hvac_load_factor * 0.5  # VA/ft²
        
        return hvac_electrical_load
    
    async def _design_electrical_distribution(self, electrical_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Design electrical distribution system"""
        total_load = electrical_loads.get("total_load", 0)
        
        # Calculate main panel size
        main_panel_size = math.ceil(total_load / 1000)  # kVA
        
        # Design main distribution
        main_distribution = {
            "main_panel": {
                "size": main_panel_size,
                "voltage": 240,
                "phases": 3
            },
            "sub_panels": await self._design_sub_panels(electrical_loads),
            "feeders": await self._design_feeders(total_load)
        }
        
        return main_distribution
    
    async def _design_sub_panels(self, electrical_loads: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design sub-panels"""
        sub_panels = []
        
        # Design lighting panel
        sub_panels.append({
            "type": "lighting",
            "size": 20,  # A
            "voltage": 120,
            "circuits": 12
        })
        
        # Design receptacle panel
        sub_panels.append({
            "type": "receptacles",
            "size": 30,  # A
            "voltage": 120,
            "circuits": 16
        })
        
        # Design HVAC panel
        sub_panels.append({
            "type": "hvac",
            "size": 40,  # A
            "voltage": 240,
            "circuits": 8
        })
        
        return sub_panels
    
    async def _design_feeders(self, total_load: float) -> List[Dict[str, Any]]:
        """Design electrical feeders"""
        feeders = []
        
        # Main feeder
        feeders.append({
            "type": "main",
            "size": 4,  # AWG
            "voltage": 240,
            "current": math.ceil(total_load / 240)
        })
        
        # Branch feeders
        feeders.append({
            "type": "branch",
            "size": 12,  # AWG
            "voltage": 120,
            "current": 20
        })
        
        return feeders
    
    async def _design_lighting(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design lighting system"""
        rooms = design_2d.get("rooms", {})
        
        # Get solar data
        solar_data = climate_data.get("solar_irradiance", [])
        avg_solar = sum([month["solar_irradiance"] for month in solar_data]) / 12 if solar_data else 1000
        
        # Design lighting for each room
        room_lighting = {}
        for room_name, room_data in rooms.items():
            room_area = room_data.get("area", 0)
            
            # Calculate lighting requirements
            if avg_solar > 1000:
                # High solar gain - reduce artificial lighting
                lighting_density = 0.5  # W/ft²
            else:
                # Low solar gain - increase artificial lighting
                lighting_density = 1.0  # W/ft²
            
            room_lighting[room_name] = {
                "area": room_area,
                "lighting_density": lighting_density,
                "total_watts": room_area * lighting_density,
                "fixtures": await self._design_lighting_fixtures(room_area, lighting_density)
            }
        
        return {
            "room_lighting": room_lighting,
            "emergency_lighting": await self._design_emergency_lighting(rooms),
            "exterior_lighting": await self._design_exterior_lighting()
        }
    
    async def _design_lighting_fixtures(self, room_area: float, lighting_density: float) -> List[Dict[str, Any]]:
        """Design lighting fixtures for a room"""
        fixtures = []
        
        # Calculate number of fixtures needed
        total_watts = room_area * lighting_density
        fixture_watts = 32  # Standard LED fixture
        num_fixtures = math.ceil(total_watts / fixture_watts)
        
        for i in range(num_fixtures):
            fixtures.append({
                "type": "LED_fixture",
                "watts": fixture_watts,
                "position": [i * 4, 0],  # Simplified positioning
                "height": 9  # ft
            })
        
        return fixtures
    
    async def _design_emergency_lighting(self, rooms: Dict[str, Any]) -> Dict[str, Any]:
        """Design emergency lighting system"""
        return {
            "exit_lighting": {
                "type": "LED_exit_sign",
                "watts": 5,
                "battery_backup": "90_minutes"
            },
            "emergency_fixtures": {
                "type": "LED_emergency",
                "watts": 10,
                "battery_backup": "90_minutes"
            }
        }
    
    async def _design_exterior_lighting(self) -> Dict[str, Any]:
        """Design exterior lighting"""
        return {
            "security_lighting": {
                "type": "LED_security",
                "watts": 50,
                "motion_sensor": True
            },
            "landscape_lighting": {
                "type": "LED_landscape",
                "watts": 20,
                "solar_powered": True
            }
        }
    
    async def _design_power_systems(self, electrical_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Design power systems"""
        return {
            "main_service": {
                "size": 200,  # A
                "voltage": 240,
                "phases": 3
            },
            "generator": {
                "size": 50,  # kW
                "fuel": "natural_gas",
                "automatic_transfer": True
            },
            "ups": {
                "size": 10,  # kVA
                "battery_backup": "30_minutes"
            }
        }
    
    async def _design_emergency_systems(self, electrical_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Design emergency systems"""
        return {
            "fire_alarm": {
                "type": "addressable",
                "zones": 4,
                "battery_backup": "24_hours"
            },
            "emergency_power": {
                "type": "generator",
                "size": 25,  # kW
                "fuel": "natural_gas"
            },
            "exit_lighting": {
                "type": "LED",
                "battery_backup": "90_minutes"
            }
        }
    
    async def _generate_plumbing_design(
        self, 
        design_2d: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate plumbing design"""
        
        # Calculate plumbing loads
        plumbing_loads = await self._calculate_plumbing_loads(design_2d, climate_data)
        
        # Design water supply
        water_supply = await self._design_water_supply(plumbing_loads)
        
        # Design drainage
        drainage = await self._design_drainage(plumbing_loads)
        
        # Design fixtures
        fixtures = await self._design_plumbing_fixtures(design_2d, climate_data)
        
        # Design water heating
        water_heating = await self._design_water_heating(plumbing_loads, climate_data)
        
        return {
            "loads": plumbing_loads,
            "water_supply": water_supply,
            "drainage": drainage,
            "fixtures": fixtures,
            "water_heating": water_heating,
            "specifications": await self._generate_plumbing_specifications(plumbing_loads)
        }
    
    async def _calculate_plumbing_loads(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate plumbing loads"""
        rooms = design_2d.get("rooms", {})
        
        # Count fixtures
        fixture_count = 0
        fixture_units = 0
        
        for room_name, room_data in rooms.items():
            if "bathroom" in room_name.lower():
                fixture_count += 3  # Toilet, lavatory, shower
                fixture_units += 6  # 3 + 1 + 2
            elif "kitchen" in room_name.lower():
                fixture_count += 2  # Sink, dishwasher
                fixture_units += 3  # 2 + 1
        
        # Calculate water demand
        water_demand = fixture_units * 10  # gpm per fixture unit
        
        return {
            "fixture_count": fixture_count,
            "fixture_units": fixture_units,
            "water_demand": water_demand,
            "peak_demand": water_demand * 1.5
        }
    
    async def _design_water_supply(self, plumbing_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Design water supply system"""
        water_demand = plumbing_loads.get("water_demand", 0)
        
        # Design main water line
        main_line_size = 4 if water_demand > 50 else 2  # inches
        
        # Design branch lines
        branch_line_size = 2 if water_demand > 25 else 1  # inches
        
        return {
            "main_line": {
                "size": main_line_size,
                "material": "copper",
                "pressure": 40  # psi
            },
            "branch_lines": {
                "size": branch_line_size,
                "material": "copper",
                "pressure": 40  # psi
            },
            "valves": {
                "main_shutoff": "ball_valve",
                "fixture_shutoffs": "angle_valve"
            }
        }
    
    async def _design_drainage(self, plumbing_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Design drainage system"""
        fixture_units = plumbing_loads.get("fixture_units", 0)
        
        # Design main drain
        main_drain_size = 4 if fixture_units > 20 else 3  # inches
        
        # Design branch drains
        branch_drain_size = 2 if fixture_units > 10 else 1.5  # inches
        
        return {
            "main_drain": {
                "size": main_drain_size,
                "material": "cast_iron",
                "slope": 0.02  # 2% slope
            },
            "branch_drains": {
                "size": branch_drain_size,
                "material": "PVC",
                "slope": 0.02  # 2% slope
            },
            "vents": {
                "main_vent": "4_inch",
                "branch_vents": "2_inch"
            }
        }
    
    async def _design_plumbing_fixtures(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design plumbing fixtures"""
        rooms = design_2d.get("rooms", {})
        
        fixtures = {
            "bathroom": [],
            "kitchen": [],
            "laundry": []
        }
        
        for room_name, room_data in rooms.items():
            if "bathroom" in room_name.lower():
                fixtures["bathroom"].extend([
                    {"type": "toilet", "model": "standard", "water_sense": True},
                    {"type": "lavatory", "model": "wall_mount", "water_sense": True},
                    {"type": "shower", "model": "standard", "water_sense": True}
                ])
            elif "kitchen" in room_name.lower():
                fixtures["kitchen"].extend([
                    {"type": "sink", "model": "double_bowl", "water_sense": True},
                    {"type": "dishwasher", "model": "energy_star", "water_sense": True}
                ])
            elif "laundry" in room_name.lower():
                fixtures["laundry"].extend([
                    {"type": "washing_machine", "model": "high_efficiency", "water_sense": True},
                    {"type": "dryer", "model": "energy_star", "gas": True}
                ])
        
        return fixtures
    
    async def _design_water_heating(self, plumbing_loads: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design water heating system"""
        water_demand = plumbing_loads.get("water_demand", 0)
        
        # Calculate water heater size
        if water_demand > 50:
            heater_size = 80  # gallons
            heater_type = "tank"
        else:
            heater_size = 50  # gallons
            heater_type = "tank"
        
        # Determine fuel type based on climate
        current_weather = climate_data.get("current_weather", {})
        temperature = current_weather.get("temperature", 20)
        
        if temperature < 0:
            fuel_type = "electric"  # Electric for cold climates
        else:
            fuel_type = "natural_gas"  # Gas for moderate climates
        
        return {
            "type": heater_type,
            "size": heater_size,
            "fuel": fuel_type,
            "efficiency": "high",
            "location": "basement"
        }
    
    async def _generate_hvac_design(
        self, 
        design_2d: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate HVAC design"""
        
        # Calculate HVAC loads
        hvac_loads = await self._calculate_hvac_loads(design_2d, climate_data)
        
        # Design heating system
        heating_system = await self._design_heating_system(hvac_loads, climate_data)
        
        # Design cooling system
        cooling_system = await self._design_cooling_system(hvac_loads, climate_data)
        
        # Design ventilation
        ventilation = await self._design_ventilation(design_2d, climate_data)
        
        # Design controls
        controls = await self._design_hvac_controls(hvac_loads, climate_data)
        
        return {
            "loads": hvac_loads,
            "heating": heating_system,
            "cooling": cooling_system,
            "ventilation": ventilation,
            "controls": controls,
            "specifications": await self._generate_hvac_specifications(hvac_loads, climate_data)
        }
    
    async def _calculate_hvac_loads(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate HVAC loads"""
        rooms = design_2d.get("rooms", {})
        total_area = sum([room.get("area", 0) for room in rooms.values()])
        
        # Get climate data
        current_weather = climate_data.get("current_weather", {})
        temperature = current_weather.get("temperature", 20)
        humidity = current_weather.get("humidity", 50)
        
        # Determine occupancy type
        occupancy_type = "residential"  # Default
        if "office" in str(design_2d).lower():
            occupancy_type = "office"
        elif "retail" in str(design_2d).lower():
            occupancy_type = "retail"
        elif "hospital" in str(design_2d).lower():
            occupancy_type = "hospital"
        elif "school" in str(design_2d).lower():
            occupancy_type = "school"
        
        # Calculate cooling load
        cooling_load_factor = self.hvac_codes["cooling_loads"][occupancy_type]
        cooling_load = total_area * cooling_load_factor  # tons
        
        # Calculate heating load
        heating_load_factor = self.hvac_codes["heating_loads"][occupancy_type]
        heating_load = total_area * heating_load_factor  # tons
        
        # Calculate ventilation load
        ventilation_rate = self.hvac_codes["ventilation_rates"][occupancy_type]
        ventilation_load = total_area * ventilation_rate  # cfm
        
        # Apply climate adjustments
        if temperature > 25:
            cooling_load *= 1.2  # Increase cooling for hot climates
        elif temperature < 10:
            heating_load *= 1.2  # Increase heating for cold climates
        
        if humidity > 70:
            cooling_load *= 1.1  # Increase cooling for humid climates
        
        return {
            "cooling_load": cooling_load,
            "heating_load": heating_load,
            "ventilation_load": ventilation_load,
            "total_load": cooling_load + heating_load,
            "occupancy_type": occupancy_type
        }
    
    async def _design_heating_system(self, hvac_loads: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design heating system"""
        heating_load = hvac_loads.get("heating_load", 0)
        
        # Determine heating system type
        if heating_load > 5:  # tons
            system_type = "boiler"
            fuel_type = "natural_gas"
        else:
            system_type = "heat_pump"
            fuel_type = "electric"
        
        return {
            "type": system_type,
            "size": heating_load,
            "fuel": fuel_type,
            "efficiency": "high",
            "distribution": "forced_air"
        }
    
    async def _design_cooling_system(self, hvac_loads: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design cooling system"""
        cooling_load = hvac_loads.get("cooling_load", 0)
        
        # Determine cooling system type
        if cooling_load > 5:  # tons
            system_type = "chiller"
        else:
            system_type = "split_system"
        
        return {
            "type": system_type,
            "size": cooling_load,
            "efficiency": "high",
            "refrigerant": "R410A",
            "distribution": "forced_air"
        }
    
    async def _design_ventilation(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design ventilation system"""
        rooms = design_2d.get("rooms", {})
        
        # Calculate ventilation requirements
        total_area = sum([room.get("area", 0) for room in rooms.values()])
        ventilation_rate = 0.35  # cfm/ft² for residential
        
        total_ventilation = total_area * ventilation_rate
        
        return {
            "type": "mechanical",
            "rate": total_ventilation,
            "efficiency": "high",
            "filters": "MERV_13",
            "heat_recovery": True
        }
    
    async def _design_hvac_controls(self, hvac_loads: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design HVAC controls"""
        return {
            "type": "smart_thermostat",
            "zones": 4,
            "programming": "7_day",
            "remote_access": True,
            "energy_monitoring": True
        }
    
    async def _generate_fire_protection_design(
        self, 
        design_2d: Dict[str, Any], 
        climate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate fire protection design"""
        rooms = design_2d.get("rooms", {})
        total_area = sum([room.get("area", 0) for room in rooms.values()])
        
        # Design sprinkler system
        sprinkler_system = await self._design_sprinkler_system(total_area)
        
        # Design fire alarm system
        fire_alarm = await self._design_fire_alarm_system(rooms)
        
        # Design fire suppression
        fire_suppression = await self._design_fire_suppression(rooms)
        
        return {
            "sprinkler_system": sprinkler_system,
            "fire_alarm": fire_alarm,
            "fire_suppression": fire_suppression,
            "specifications": await self._generate_fire_protection_specifications(total_area)
        }
    
    async def _design_sprinkler_system(self, total_area: float) -> Dict[str, Any]:
        """Design sprinkler system"""
        # Calculate number of sprinklers needed
        coverage_per_sprinkler = 100  # ft²
        num_sprinklers = math.ceil(total_area / coverage_per_sprinkler)
        
        return {
            "type": "wet_pipe",
            "sprinklers": num_sprinklers,
            "coverage": coverage_per_sprinkler,
            "water_supply": "municipal",
            "pressure": 50  # psi
        }
    
    async def _design_fire_alarm_system(self, rooms: Dict[str, Any]) -> Dict[str, Any]:
        """Design fire alarm system"""
        num_rooms = len(rooms)
        
        return {
            "type": "addressable",
            "zones": num_rooms,
            "detectors": num_rooms * 2,  # Smoke and heat detectors
            "pull_stations": 2,
            "horns": num_rooms,
            "battery_backup": "24_hours"
        }
    
    async def _design_fire_suppression(self, rooms: Dict[str, Any]) -> Dict[str, Any]:
        """Design fire suppression system"""
        return {
            "type": "sprinkler",
            "coverage": "total",
            "activation": "automatic",
            "monitoring": "central_station"
        }
    
    async def _generate_mep_drawings(
        self, 
        electrical_design: Dict[str, Any], 
        plumbing_design: Dict[str, Any], 
        hvac_design: Dict[str, Any], 
        fire_protection: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate MEP drawings"""
        return {
            "electrical_plan": {
                "type": "plan",
                "scale": "1:100",
                "elements": electrical_design.get("distribution", {})
            },
            "plumbing_plan": {
                "type": "plan",
                "scale": "1:100",
                "elements": plumbing_design.get("water_supply", {})
            },
            "hvac_plan": {
                "type": "plan",
                "scale": "1:100",
                "elements": hvac_design.get("heating", {})
            },
            "fire_protection_plan": {
                "type": "plan",
                "scale": "1:100",
                "elements": fire_protection.get("sprinkler_system", {})
            }
        }
    
    async def _generate_mep_specifications(self, design_2d: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate MEP specifications"""
        return {
            "electrical": {
                "codes": ["NEC", "IBC"],
                "standards": ["IEEE", "UL"],
                "materials": ["copper", "aluminum", "steel"]
            },
            "plumbing": {
                "codes": ["IPC", "IBC"],
                "standards": ["ASTM", "ANSI"],
                "materials": ["copper", "PVC", "cast_iron"]
            },
            "hvac": {
                "codes": ["IMC", "IBC"],
                "standards": ["ASHRAE", "ARI"],
                "materials": ["steel", "aluminum", "copper"]
            },
            "fire_protection": {
                "codes": ["NFPA", "IBC"],
                "standards": ["UL", "FM"],
                "materials": ["steel", "copper", "PVC"]
            }
        }
    
    async def _generate_electrical_specifications(self, electrical_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Generate electrical specifications"""
        return {
            "codes": ["NEC", "IBC"],
            "standards": ["IEEE", "UL"],
            "materials": ["copper", "aluminum", "steel"],
            "loads": electrical_loads
        }
    
    async def _generate_plumbing_specifications(self, plumbing_loads: Dict[str, Any]) -> Dict[str, Any]:
        """Generate plumbing specifications"""
        return {
            "codes": ["IPC", "IBC"],
            "standards": ["ASTM", "ANSI"],
            "materials": ["copper", "PVC", "cast_iron"],
            "loads": plumbing_loads
        }
    
    async def _generate_hvac_specifications(self, hvac_loads: Dict[str, Any], climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate HVAC specifications"""
        return {
            "codes": ["IMC", "IBC"],
            "standards": ["ASHRAE", "ARI"],
            "materials": ["steel", "aluminum", "copper"],
            "loads": hvac_loads,
            "climate": climate_data
        }
    
    async def _generate_fire_protection_specifications(self, total_area: float) -> Dict[str, Any]:
        """Generate fire protection specifications"""
        return {
            "codes": ["NFPA", "IBC"],
            "standards": ["UL", "FM"],
            "materials": ["steel", "copper", "PVC"],
            "area": total_area
        }
