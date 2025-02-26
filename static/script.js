document.getElementById("chat-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let userInput = document.getElementById("user-input").value;
    let data = userInput.split(",").map(x => parseFloat(x.trim()));

    let requestBody = {
        "tv": data[0],
        "washing_machine": data[1],
        "mobile": data[2],
        "chimney": data[3],
        "lpg": data[4],
        "fan": data[5],
        "ac": data[6],
        "water_heater": data[7],
        "wifi_router": data[8],
        "water_pump": data[9],
        "num_lights": data[10],
        "lights_on": data[11],
        "transportation": "Car",
        "waste": data[12],
        "diet": "Vegetarian"
    };

    let response = await fetch("/calculate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
    });

    let result = await response.json();
    document.getElementById("response").innerHTML = `
        <h2>Estimated Carbon Footprint: ${result.footprint}</h2>
        <p>${result.recommendations}</p>
    `;
});
