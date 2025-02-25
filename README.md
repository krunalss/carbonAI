# Carbon Footprint Calculator

This project is a Shiny web application designed to help individuals calculate their estimated daily carbon footprint and receive personalized recommendations for reducing it.  It leverages the power of Large Language Models (LLMs), specifically the Llama3-70b-8192 model via the Groq API, to provide insightful and actionable advice.

## Features

* **Interactive Questionnaire:** Users answer a series of questions about their daily habits related to energy consumption, transportation, waste, and diet.  The questions are grouped into manageable pages for a smoother user experience.
* **Personalized Recommendations:** Based on the user's input, the application uses the Llama3-70b-8192 LLM to generate tailored recommendations for reducing their carbon footprint. These recommendations are structured and easy to understand.
* **Estimated Carbon Footprint:** The application provides an estimated daily carbon footprint in kg CO₂ based on the user's responses (note: this is a simplified estimate and should not be taken as a precise scientific measurement).
* **Intuitive User Interface:** The Shiny framework provides a user-friendly web interface with clear navigation and input fields.

## Technologies Used

* **Shiny (R):** For building the interactive web application.
* **LangChain Groq:** For interfacing with the Groq API and the Llama3-70b-8192 LLM.
* **Llama3-70b-8192 (LLM):**  To generate personalized recommendations.
* **dotenv:** For managing environment variables (API keys).

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/krunalss/carbonAI.git](https://www.google.com/search?q=https://github.com/krunalss/carbonAI.git)  # Replace with your repo URL
   cd carbonAI

2. **Install required R packages:**
    ```bash
    install.packages(c("shiny", "langchain", "dotenv")) # Add other packages if needed

3. **Set up environment variables:**
- Create a .env file in the project directory.
- Add your Groq API key to the .env file:
    ```bash
    GROQ_API_KEY=YOUR_ACTUAL_GROQ_API_KEY

##  **Contributing**

Contributions are welcome! Please open an issue or submit a pull request.

##  **License**

MIT

## **Disclaimer**

The carbon footprint calculation provided by this application is an estimate based on the user's input and is not a substitute for professional assessment.  The recommendations generated by the LLM are intended for informational purposes and should be considered suggestions for reducing environmental impact.  Actual results may vary.   