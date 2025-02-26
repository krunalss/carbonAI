# calculator.py

def calculate_carbon_footprint(tv, washing_machine, mobile_charging, kitchen_chimney, lpg_gas, fan, ac, water_heater, 
                               wifi_router, water_pump, lights, lights_time, transportation, waste, diet):
    """
    Calculate the daily carbon footprint based on energy usage, LPG consumption, transportation, waste, and diet.
    All calculations are based on India's average emission factors.
    """

    # Electricity Emission Factor for India (kg CO2 per kWh)
    electricity_factor = 0.82  

    # Appliance Power Ratings (in kW)
    power_ratings = {
        "tv": 0.15,
        "washing_machine": 1.0,
        "mobile_charging": 0.01,
        "kitchen_chimney": 0.25,
        "fan": 0.075,
        "ac": 2.5,
        "water_heater": 2.0,
        "wifi_router": 0.01,
        "water_pump": 1.5,
        "lights": 0.05  # Assuming LED bulbs
    }

    # Calculate Electricity Consumption (in kWh)
    electricity_kwh = (
        (tv * power_ratings["tv"]) +
        (washing_machine * power_ratings["washing_machine"]) +
        (mobile_charging * power_ratings["mobile_charging"]) +
        (kitchen_chimney * power_ratings["kitchen_chimney"]) +
        (fan * power_ratings["fan"]) +
        (ac * power_ratings["ac"]) +
        (water_heater * power_ratings["water_heater"]) +
        (wifi_router * power_ratings["wifi_router"]) +
        (water_pump * power_ratings["water_pump"]) +
        (lights * lights_time * power_ratings["lights"])
    )

    # Carbon Emissions from Electricity
    electricity_emissions = electricity_kwh * electricity_factor

    # Carbon Emissions from LPG
    lpg_emissions = lpg_gas * 2.983  # kg CO2 per kg LPG

    # Carbon Emissions from Waste
    waste_emissions = waste * 0.15  # kg CO2 per kg of waste

    # Transportation Emission Factors
    transport_factors = {
        "car_petrol": 0.25,
        "car_diesel": 0.27,
        "bus": 0.1,
        "train": 0.05,
        "bicycle": 0,
        "walking": 0
    }

    # Carbon Emissions from Transport
    transport_emissions = transport_factors.get(transportation.lower(), 0)  # Default to 0 if transport type is unknown

    # Carbon Emissions from Diet
    diet_factors = {
        "vegan": 2.0,
        "vegetarian": 3.5,
        "omnivore": 5.0,
        "meat-heavy": 7.0
    }
    diet_emissions = diet_factors.get(diet.lower(), 3.5)  # Default to vegetarian if unknown

    # Total Daily Carbon Footprint
    total_carbon_footprint = (
        electricity_emissions + lpg_emissions + waste_emissions + transport_emissions + diet_emissions
    )

    return {
        "electricity_emissions": round(electricity_emissions, 2),
        "lpg_emissions": round(lpg_emissions, 2),
        "waste_emissions": round(waste_emissions, 2),
        "transport_emissions": round(transport_emissions, 2),
        "diet_emissions": round(diet_emissions, 2),
        "total_carbon_footprint": round(total_carbon_footprint, 2)
    }
