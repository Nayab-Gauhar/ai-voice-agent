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

        websocket.onmessage = (event) => {
            const message = JSON.parse(event.data)

            if(message.type === "transcript"){

                if (message.speech_final){
                    console.log("User utterance",message.text)
                }
                else if(message.is_final){
                    console.log("Stable Transcript:",message.text)
                }
                else{
                    console.log("Interim :",message.text)
                }
            return;
        }
            if(message.type === "ai_response"){
                console.log("AI : ",message.text)
                return;
            }

            // console.log("Server:", event.data);
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