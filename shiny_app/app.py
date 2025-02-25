from shiny import App, ui, render, reactive
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load Groq API Key
load_dotenv()
groq_api_key = os.environ.get('GROQ_API_KEY')

# Initialize Groq LLM
llm = ChatGroq(groq_api_key=groq_api_key, model="Llama3-70b-8192")

# Define Questions (Grouped 4 per Page)
questions = [
    [
        {"label": "Time using TV (in hours):", "key": "tv", "type": "numeric"},
        {"label": "Time using Washing Machine (in hours):", "key": "washing_machine", "type": "numeric"},
        {"label": "Time charging Mobile (in hours):", "key": "mobile", "type": "numeric"},
        {"label": "Time using Kitchen Chimney (in hours):", "key": "chimney", "type": "numeric"},
    ],
    [
        {"label": "LPG Gas usage (in hours):", "key": "lpg", "type": "numeric"},
        {"label": "Time using Fan (in hours):", "key": "fan", "type": "numeric"},
        {"label": "Time using Air Conditioner (in hours):", "key": "ac", "type": "numeric"},
        {"label": "Time using Water Heater (in hours):", "key": "water_heater", "type": "numeric"},
    ],
    [
        {"label": "Time using Wifi Router (in hours):", "key": "wifi_router", "type": "numeric"},
        {"label": "Time using Water Pump (in hours):", "key": "water_pump", "type": "numeric"},
        {"label": "Number of Lights:", "key": "num_lights", "type": "numeric"},
        {"label": "Time Lights are On (in hours):", "key": "lights_on", "type": "numeric"},
    ],
    [
        {
            "label": "Transportation Mode:",
            "key": "transportation",
            "type": "select",
            "options": ["Car", "Bike", "Public Transport", "Walk"],
        },
        {"label": "Waste Generated (in kg):", "key": "waste", "type": "numeric"},
        {
            "label": "Diet Type:",
            "key": "diet",
            "type": "select",
            "options": ["Vegetarian", "Non-Vegetarian", "Vegan"],
        },
    ],
]

# Reactive Variables to Store Recommendations
recommendation_text = reactive.Value("")
carbon_footprint_text = reactive.Value("")

# Define UI
app_ui = ui.page_fluid(
    ui.panel_title("🌍 Carbon Footprint Calculator"),

    ui.page_sidebar(
        sidebar=ui.sidebar(
            ui.input_numeric("step", "Step", 1, min=1, max=len(questions), step=1, width="100px"),
            ui.input_action_button("prev", "Previous"),
            ui.input_action_button("next", "Next"),
            ui.hr(),
            ui.input_action_button("submit", "Submit"),
        ),
    ),

    ui.layout_columns(
        ui.card(
            ui.output_ui("questionnaire"),
            ui.output_ui("recommendations")
        )
    )
)

# Define Server Logic
def server(input, output, session):
    responses = {}

    @output
    @render.ui
    def questionnaire():
        step = int(input.step())
        question_group = questions[step - 1]

        inputs = []
        for q in question_group:
            if q["type"] == "numeric":
                inputs.append(ui.input_numeric(q["key"], q["label"], 0, min=0, step=1))
            else:
                inputs.append(ui.input_select(q["key"], q["label"], q["options"]))

        return ui.div(*inputs)

    # ✅ Fix: Use reactive effect instead of `on_input_change()`
    @reactive.effect
    def handle_navigation():
        if input.next() > 0:
            step_val = min(input.step() + 1, len(questions))
            session.send_input_message("step", step_val)

        if input.prev() > 0:
            step_val = max(input.step() - 1, 1)
            session.send_input_message("step", step_val)

    @reactive.effect
    def generate_recommendations():
        if input.submit() > 0:  # ✅ Use reactive effect for submit button
            user_data = {q["key"]: input.get(q["key"], 0) for group in questions for q in group}

            prompt_text = f"""
            Based on the following user's daily activities, provide **well-structured** recommendations to reduce carbon footprint.

            **🌱 Recommendations:**
            1️⃣ **Tip 1**  
            Explanation of how to optimize.

            2️⃣ **Tip 2**  
            Explanation of how to optimize.

            At the end, show **Total Estimated Carbon Footprint** in kg CO₂.

            User Data:
            {user_data}
            """

            response = llm.invoke(prompt_text)
            total_footprint = sum(val for val in user_data.values() if isinstance(val, (int, float)))

            # ✅ Store in reactive variables
            recommendation_text.set(response)
            carbon_footprint_text.set(f"💨 Estimated Carbon Footprint: {total_footprint} kg CO₂")

    @output
    @render.ui
    def recommendations():
        return ui.div(
            ui.h2("🌿 Optimization Recommendations", class_="text-success"),
            ui.p(recommendation_text(), class_="lead"),  # ✅ Use reactive variable
            ui.h3(carbon_footprint_text(), class_="text-primary"),  # ✅ Use reactive variable
        )

# Create the app
app = App(app_ui, server)
