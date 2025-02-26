# 🌍 GreenGauge - Carbon Footprint Calculator & Recommendation System  

**GreenGauge** is a **FastAPI-based web application** that calculates a user's **carbon footprint** based on daily activities and provides **AI-generated recommendations** to reduce it. The application is powered by **Groq LLM API(llama-3.1-8b-instant)** for intelligent insights and deployed on **Hugging Face Spaces** using **Docker**.

---

## 🚀 Features  

✅ **Carbon Footprint Calculation**  
- Estimates emissions from **electricity usage, LPG, waste, transportation, and diet**.  
- Uses **scientific emission factors** for accurate calculations.  

✅ **AI-Powered Recommendations**  
- Provides **personalized suggestions** to reduce emissions.  
- Classifies footprint as **low, medium, or high** and adapts advice accordingly.  

✅ **Interactive Web Interface**  
- Users input their daily activities in an **intuitive form**.  
- Results are displayed in a **structured and user-friendly format**.  

✅ **FastAPI Backend & Hugging Face Deployment**  
- Built using **FastAPI** for high performance.  
- Deployed on **Hugging Face Spaces** using **Docker**.  

---

## 🛠️ Tech Stack  

- **Backend:** FastAPI  
- **Frontend:** Jinja2 + Bootstrap  
- **AI Model:** Groq LLM API (llama-3.1-8b-instant)  
- **Deployment:** Hugging Face Spaces (Docker)  
- **Python Version:** `3.12.7-slim`  

---

## 🔧 Installation & Local Setup  


### **1️⃣ Clone the Repository**  
```bash
git clone https://huggingface.co/spaces/your-username/your-space-name
cd your-space-name
```

### **2️⃣ Create a Virtual Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a .env file in the root directory and add your Groq API key:

```bash
GROQ_API_KEY=your_groq_api_key 
```

### **5️⃣ Run the Application Locally**
```bash
uvicorn app:app --host 127.0.0.1 --port 7860 --reload
```
Open your browser and visit: http://127.0.0.1:7860/

## **🌐 Deployment on Hugging Face Spaces**
1️⃣ Create a new Space on Hugging Face: Hugging Face Spaces.

2️⃣ Select Docker as the runtime environment.

3️⃣ Push the Code to the Hugging Face repository:

```bash
git init
git add .
git commit -m "Deploying GreenGauge on Hugging Face"
git remote add origin https://huggingface.co/spaces/your-username/your-space-name
git push origin main
```

4️⃣ Hugging Face will automatically build and deploy your FastAPI app.

### **🐳 Docker Deployment (Local Testing)**
If you want to test using Docker, build and run the container:
```bash
docker build -t greengauge .
docker run -p 7860:7860 greengauge
```

### **🏆 Contributors**
Your Name - Developer & AI Engineer
🙌 Open to collaborations! Feel free to contribute or suggest improvements.

### **📄 License**
This project is licensed under the MIT License.

# **🌱 "The greatest threat to our planet is the belief that someone else will save it." – Robert Swan**

