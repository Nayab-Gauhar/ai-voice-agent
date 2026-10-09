let websocket = null;
let microphoneStream = null;
let mediaRecorder = null;

const startButton = document.getElementById("start-mic");
const stopButton = document.getElementById("stop-mic");
const status = document.getElementById("status");

startButton.addEventListener("click", async () => {
    try {
        // --------------------------------
        // 1. Get microphone permission
        // --------------------------------
        microphoneStream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        console.log("🎙️ Microphone access granted");

        // --------------------------------
        // 2. Connect WebSocket
        // --------------------------------
        const protocol =
            window.location.protocol === "https:"
                ? "wss"
                : "ws";

        const websocketUrl =
            `${protocol}://${window.location.host}/ws`;
            
        websocket = new WebSocket(websocketUrl);

        websocket.onopen = () => {
            console.log("WebSocket connected");

            // --------------------------------
            // 3. Choose supported audio format
            // --------------------------------
            let mimeType = "";

            if (
                MediaRecorder.isTypeSupported(
                    "audio/webm;codecs=opus"
                )
            ) {
                mimeType = "audio/webm;codecs=opus";
            } else if (
                MediaRecorder.isTypeSupported(
                    "audio/ogg;codecs=opus"
                )
            ) {
                mimeType = "audio/ogg;codecs=opus";
            } else {
                mimeType = "";
            }

            console.log("MIME type:", mimeType || "browser default");

            // --------------------------------
            // 4. Create recorder
            // --------------------------------
            mediaRecorder = mimeType
                ? new MediaRecorder(
                      microphoneStream,
                      { mimeType }
                  )
                : new MediaRecorder(microphoneStream);

            // --------------------------------
            // 5. Audio chunk produced
            // --------------------------------
            mediaRecorder.ondataavailable = (event) => {
                const audioChunk = event.data;

                if (audioChunk.size === 0) {
                    return;
                }

                console.log(
                    "Audio chunk:",
                    audioChunk.size,
                    "bytes",
                    audioChunk.type
                );

                // --------------------------------
                // 6. Send audio to FastAPI
                // --------------------------------
                if (
                    websocket &&
                    websocket.readyState === WebSocket.OPEN
                ) {
                    websocket.send(audioChunk);
                }
            };

            // --------------------------------
            // 7. Start recording
            // --------------------------------
            mediaRecorder.start(500);

            console.log("Recording started");

            status.textContent = "Listening...";

            startButton.disabled = true;
            stopButton.disabled = false;
        };

        websocket.onmessage = async (event) => {

            // Binary message = audio from Sarvam
            if (event.data instanceof Blob) {

                console.log("🔊 Audio received:", event.data.size, "bytes");

                // Pause microphone recording while the agent speaks
                if (mediaRecorder?.state === "recording") {
                    mediaRecorder.pause();
                }

                const audioBlob = new Blob(
                    [event.data],
                    { type: "audio/wav" }
                );

                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);

                const finishPlayback = () => {
                    URL.revokeObjectURL(audioUrl);

                    if (mediaRecorder?.state === "paused") {
                        mediaRecorder.resume();
                    }
                };

                audio.addEventListener("ended", finishPlayback, { once: true });
                audio.addEventListener("error", finishPlayback, { once: true });

                try {
                    await audio.play();
                } catch (error) {
                    console.error("Audio playback failed:", error);
                    finishPlayback();
                }

                return;
            }

            // Text message = transcript or AI response
            const message = JSON.parse(event.data);

            if (message.type === "transcript") {
                console.log("👤 Transcript:", message.text);
            }

            if (message.type === "ai_response") {
                console.log("🤖 AI:", message.text);
            }
        };

        websocket.onclose = () => {
            console.log(" WebSocket closed");

            status.textContent = "Disconnected";
        };

        websocket.onerror = (error) => {
            console.error(" WebSocket error:", error);

            status.textContent = "WebSocket error";
        };

    } catch (error) {
        console.error("Error:", error);

        status.textContent =
            `Error: ${error.message}`;
    }
});


stopButton.addEventListener("click", () => {

    // --------------------------------
    // Stop recorder
    // --------------------------------
    if (
        mediaRecorder &&
        mediaRecorder.state !== "inactive"
    ) {
        mediaRecorder.stop();
    }

    // --------------------------------
    // Stop microphone
    // --------------------------------
    if (microphoneStream) {

        microphoneStream
            .getTracks()
            .forEach(track => track.stop());

        microphoneStream = null;
    }

    // --------------------------------
    // Close WebSocket
    // --------------------------------
    if (
        websocket &&
        websocket.readyState === WebSocket.OPEN
    ) {
        websocket.close();
    }

    mediaRecorder = null;
    websocket = null;

    status.textContent = "Microphone off";

    startButton.disabled = false;
    stopButton.disabled = true;
});