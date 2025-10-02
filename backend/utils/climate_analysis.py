"""
Climate analysis utilities for architectural recommendations
"""

from typing import Dict, Any, List
import math

def analyze_climate_patterns(
    current_weather: Dict[str, Any],
    historical_data: Dict[str, Any],
    seasonal_patterns: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze climate patterns and generate architectural insights"""
    
    analysis = {
        "climate_zone": determine_climate_zone(current_weather, historical_data),
        "thermal_comfort": analyze_thermal_comfort(current_weather, historical_data),
        "energy_efficiency": analyze_energy_efficiency(current_weather, historical_data),
        "ventilation_needs": analyze_ventilation_needs(current_weather, historical_data),
        "solar_potential": analyze_solar_potential(current_weather, historical_data),
        "precipitation_impact": analyze_precipitation_impact(historical_data),
        "wind_patterns": analyze_wind_patterns(current_weather, historical_data)
    }
    
    return analysis

def determine_climate_zone(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> str:
    """Determine climate zone based on temperature and precipitation patterns"""
    avg_temp = current_weather.get("temperature", 20)
    precipitation = historical_data.get("precipitation_data", [])
    
    # Calculate average annual precipitation
    avg_precipitation = sum([month["precipitation"] for month in precipitation]) / 12 if precipitation else 0
    
    # Köppen climate classification
    if avg_temp > 18:
        if avg_precipitation > 1000:
            return "Tropical Rainforest"
        elif avg_precipitation > 500:
            return "Tropical Monsoon"
        else:
            return "Tropical Savanna"
    elif avg_temp > 10:
        if avg_precipitation > 1000:
            return "Temperate Oceanic"
        elif avg_precipitation > 500:
            return "Temperate Continental"
        else:
            return "Temperate Steppe"
    else:
        if avg_precipitation > 500:
            return "Subarctic"
        else:
            return "Tundra"

def analyze_thermal_comfort(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze thermal comfort requirements"""
    temp = current_weather.get("temperature", 20)
    humidity = current_weather.get("humidity", 50)
    
    # Calculate comfort zone (18-26°C, 30-70% humidity)
    temp_comfort = 18 <= temp <= 26
    humidity_comfort = 30 <= humidity <= 70
    
    # Calculate heating/cooling degree days
    heating_degree_days = max(0, 18 - temp)
    cooling_degree_days = max(0, temp - 26)
    
    return {
        "temperature_comfort": temp_comfort,
        "humidity_comfort": humidity_comfort,
        "heating_degree_days": heating_degree_days,
        "cooling_degree_days": cooling_degree_days,
        "thermal_strategy": get_thermal_strategy(temp, humidity)
    }

def get_thermal_strategy(temperature: float, humidity: float) -> str:
    """Determine thermal strategy based on temperature and humidity"""
    if temperature > 26:
        if humidity > 70:
            return "Passive cooling with dehumidification"
        else:
            return "Passive cooling with ventilation"
    elif temperature < 18:
        if humidity > 70:
            return "Passive heating with humidity control"
        else:
            return "Passive heating with thermal mass"
    else:
        return "Natural ventilation and thermal mass"

def analyze_energy_efficiency(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze energy efficiency opportunities"""
    temp = current_weather.get("temperature", 20)
    solar_irradiance = historical_data.get("solar_irradiance", [])
    
    # Calculate average solar irradiance
    avg_solar = sum([month["solar_irradiance"] for month in solar_irradiance]) / 12 if solar_irradiance else 0
    
    return {
        "solar_potential": avg_solar,
        "insulation_priority": "High" if abs(temp - 20) > 10 else "Medium",
        "renewable_energy": "Solar" if avg_solar > 800 else "Wind",
        "energy_storage": avg_solar > 1000
    }

def analyze_ventilation_needs(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze ventilation requirements"""
    humidity = current_weather.get("humidity", 50)
    wind_speed = current_weather.get("wind_speed", 5)
    
    return {
        "natural_ventilation": wind_speed > 3,
        "mechanical_ventilation": humidity > 70 or wind_speed < 2,
        "cross_ventilation": wind_speed > 5,
        "ventilation_rate": calculate_ventilation_rate(humidity, wind_speed)
    }

def calculate_ventilation_rate(humidity: float, wind_speed: float) -> str:
    """Calculate required ventilation rate"""
    if humidity > 70:
        return "High (6-12 ACH)"
    elif wind_speed > 5:
        return "Natural (2-4 ACH)"
    else:
        return "Standard (3-6 ACH)"

def analyze_solar_potential(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze solar energy potential"""
    solar_data = historical_data.get("solar_irradiance", [])
    
    if not solar_data:
        return {"potential": "Unknown", "orientation": "South", "tilt": 30}
    
    avg_solar = sum([month["solar_irradiance"] for month in solar_data]) / 12
    
    return {
        "potential": "High" if avg_solar > 1000 else "Medium" if avg_solar > 500 else "Low",
        "orientation": "South",
        "tilt": calculate_optimal_tilt(solar_data),
        "shading_considerations": avg_solar < 800
    }

def calculate_optimal_tilt(solar_data: List[Dict[str, Any]]) -> int:
    """Calculate optimal solar panel tilt angle"""
    # Simplified calculation based on seasonal variation
    summer_irradiance = sum([month["solar_irradiance"] for month in solar_data[5:8]]) / 3
    winter_irradiance = sum([month["solar_irradiance"] for month in solar_data[11:2]]) / 3
    
    if summer_irradiance > winter_irradiance * 1.5:
        return 20  # Favor summer generation
    elif winter_irradiance > summer_irradiance * 1.2:
        return 45  # Favor winter generation
    else:
        return 30  # Balanced

def analyze_precipitation_impact(historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze precipitation impact on design"""
    precipitation_data = historical_data.get("precipitation_data", [])
    
    if not precipitation_data:
        return {"roof_design": "Standard", "drainage": "Basic", "water_management": "None"}
    
    avg_precipitation = sum([month["precipitation"] for month in precipitation_data]) / 12
    max_precipitation = max([month["precipitation"] for month in precipitation_data])
    
    return {
        "roof_design": "Steep" if max_precipitation > 100 else "Standard",
        "drainage": "Enhanced" if avg_precipitation > 80 else "Basic",
        "water_management": "Rainwater harvesting" if avg_precipitation > 60 else "None",
        "flood_risk": "High" if max_precipitation > 150 else "Low"
    }

def analyze_wind_patterns(current_weather: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze wind patterns for design considerations"""
    wind_speed = current_weather.get("wind_speed", 5)
    wind_direction = current_weather.get("wind_direction", 0)
    
    wind_data = historical_data.get("wind_data", [])
    avg_wind_speed = sum([month["wind_speed"] for month in wind_data]) / 12 if wind_data else wind_speed
    
    return {
        "prevailing_wind": get_wind_direction_name(wind_direction),
        "wind_speed_category": get_wind_speed_category(avg_wind_speed),
        "wind_breaks_needed": avg_wind_speed > 10,
        "natural_ventilation": avg_wind_speed > 3,
        "structural_considerations": avg_wind_speed > 15
    }

def get_wind_direction_name(degrees: float) -> str:
    """Convert wind direction degrees to compass direction"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]

def get_wind_speed_category(speed: float) -> str:
    """Categorize wind speed"""
    if speed < 2:
        return "Light"
    elif speed < 5:
        return "Gentle"
    elif speed < 10:
        return "Moderate"
    elif speed < 15:
        return "Fresh"
    else:
        return "Strong"
