from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize Groq LLM API
llm = ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")

# Power Ratings in kW (average values)
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
    "lights": 0.05  # per light
}

# Emission Factors
electricity_factor = 0.82  # kg CO2 per kWh
lpg_factor = 2.983  # kg CO2 per kg of LPG
waste_factor = 0.15  # kg CO2 per kg of waste

# Transportation Emission Factors (kg CO2 per trip)
transport_factors = {
    "car": 2.5,  # Estimated per trip
    "bike": 1.0,
    "public": 1.5,
    "walk": 0  # No emissions for walking
}

# Diet Carbon Emissions (kg CO2 per day)
diet_factors = {
    "vegan": 2.0,
    "vegetarian": 3.5,
    "omnivore": 5.0,
    "meat-heavy": 7.0
}

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("greengauge.html", {"request": request})

@app.post("/calculate_greengauge")
async def calculate_greengauge(
    request: Request,
    tv: float = Form(...),
    washing_machine: float = Form(...),
    mobile_charging: float = Form(...),
    kitchen_chimney: float = Form(...),
    lpg_gas: float = Form(...),
    fan: float = Form(...),
    ac: float = Form(...),
    water_heater: float = Form(...),
    wifi_router: float = Form(...),
    water_pump: float = Form(...),
    lights: int = Form(...),
    lights_time: float = Form(...),
    transportation: str = Form(...),
    waste: float = Form(...),
    diet: str = Form(...)
):
    # Calculate electricity consumption (kWh)
    electricity_kwh = (
        tv * power_ratings["tv"] +
        washing_machine * power_ratings["washing_machine"] +
        mobile_charging * power_ratings["mobile_charging"] +
        kitchen_chimney * power_ratings["kitchen_chimney"] +
        fan * power_ratings["fan"] +
        ac * power_ratings["ac"] +
        water_heater * power_ratings["water_heater"] +
        wifi_router * power_ratings["wifi_router"] +
        water_pump * power_ratings["water_pump"] +
        lights * lights_time * power_ratings["lights"]
    )

    # Convert electricity consumption to emissions
    electricity_emissions = electricity_kwh * electricity_factor

    # Calculate emissions from LPG
    lpg_emissions = lpg_gas * lpg_factor

    # Calculate waste emissions
    waste_emissions = waste * waste_factor

    # Calculate transportation emissions
    transport_emissions = transport_factors.get(transportation.lower(), 0)

    # Calculate diet emissions
    diet_emissions = diet_factors.get(diet.lower(), 3.5)  # Default to vegetarian if unknown

    # Calculate total carbon footprint
    total_footprint = (
        electricity_emissions + lpg_emissions + waste_emissions + transport_emissions + diet_emissions
    )

    # Prepare prompt for LLM
    prompt_text = f"""
    User's daily activity data:
    - TV: {tv} hrs, Washing Machine: {washing_machine} hrs, Mobile Charging: {mobile_charging} hrs
    - Kitchen Chimney: {kitchen_chimney} hrs, LPG: {lpg_gas} kg, Fan: {fan} hrs, AC: {ac} hrs
    - Water Heater: {water_heater} hrs, Wifi Router: {wifi_router} hrs, Water Pump: {water_pump} hrs
    - Lights: {lights} x {lights_time} hrs, Waste: {waste} kg, Transportation: {transportation}
    - Diet: {diet}

    **Carbon Footprint Breakdown:**
    - Electricity: {electricity_emissions:.2f} kg CO₂
    - LPG: {lpg_emissions:.2f} kg CO₂
    - Waste: {waste_emissions:.2f} kg CO₂
    - Transport: {transport_emissions:.2f} kg CO₂
    - Diet: {diet_emissions:.2f} kg CO₂
    - **Total: {total_footprint:.2f} kg CO₂**

    Classify this footprint as "low" (0 - 10 kg), "medium" (10 - 30 kg), or "high" (30+ kg).
    Provide clear and structured recommendations to reduce emissions in a sustainable way.
    """

    # Get recommendations from LLM
    response = llm.invoke(prompt_text)

    # Format LLM response
    formatted_recommendations = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response.content.replace("\n", "<br>"))

    # Define emission ranges
    emission_ranges = {
        "low": "0 - 10 kg CO₂",
        "medium": "10 - 30 kg CO₂",
        "high": "30+ kg CO₂"
    }

    return templates.TemplateResponse("greengauge_result.html", {
        "request": request,
        "carbon_emission": f"{total_footprint:.2f}",
        "emission_ranges": emission_ranges,
        "recommendations": formatted_recommendations
    })
