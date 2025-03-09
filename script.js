// Show/hide input fields based on selected input type
document.getElementById("input-type").addEventListener("change", function () {
    const inputType = this.value;
    document.getElementById("text-input").style.display = inputType === "text" ? "block" : "none";
    document.getElementById("audio-input").style.display = inputType === "audio" ? "block" : "none";
    document.getElementById("image-input").style.display = inputType === "image" ? "block" : "none";
});

// Handle form submission
document.getElementById("translator-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Get input values
    const inputType = document.getElementById("input-type").value;
    const targetLanguage = document.getElementById("target-language").value;
    console.log("Selected Language:", targetLanguage);

    // Initialize FormData
    const formData = new FormData();
    formData.append("input_type", inputType);
    formData.append("target_language", targetLanguage);

    // Append data based on input type
    if (inputType === "text") {
        const text = document.getElementById("text").value;
        if (!text) {
            alert("Please enter some text.");
            return;
        }
        formData.append("text", text);
        console.log("Text Input:", text);
    } else if (inputType === "audio") {
        const audioFile = document.getElementById("audio").files[0];
        if (audioFile) {
            formData.append("audio_file", audioFile);
            console.log("Audio File:", audioFile.name);
        } else {
            alert("Please upload an audio file.");
            return;
        }
    } else if (inputType === "image") {
        const imageFile = document.getElementById("image").files[0];
        if (imageFile) {
            formData.append("image_file", imageFile);
            console.log("Image File:", imageFile.name);
        } else {
            alert("Please upload an image file.");
            return;
        }
    }

    // Send data to the backend
    try {
        const response = await fetch("/translate", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Translation Result:", result);

        // Display the result
        document.getElementById("original-text").textContent = result.original_text || "N/A";
        document.getElementById("translated-text").textContent = result.translated_text || "N/A";
    } catch (error) {
        console.error("Error during translation:", error);
        alert("An error occurred during translation. Please try again.");
    }
});