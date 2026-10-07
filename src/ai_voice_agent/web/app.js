let microphoneStream = null;

const startButton = document.getElementById("start-mic");
const stopButton = document.getElementById("stop-mic");
const status = document.getElementById("status");


startButton.addEventListener("click", async () => {

    try {

        microphoneStream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        console.log("Microphone stream:", microphoneStream);

        status.textContent = "Microphone ON";

        startButton.disabled = true;
        stopButton.disabled = false;

    } catch (error) {

        console.error("Microphone error:", error);

        status.textContent = `Error: ${error.name}`;
    }
});


stopButton.addEventListener("click", () => {

    if (microphoneStream) {

        microphoneStream.getTracks().forEach(track => {
            track.stop();
        });

        microphoneStream = null;
    }

    status.textContent = "Microphone off";

    startButton.disabled = false;
    stopButton.disabled = true;
});