console.log("Hand Tracking App Loaded.");

// DOM Elements
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const cameraToggleBtn = document.getElementById("camera-toggle-btn");
const statusText = document.getElementById("status-text");
const webcamFeed = document.getElementById("webcam-feed");

let isCameraOn = true;

// Event Listeners
startBtn.addEventListener("click", () => {
    statusText.textContent = "Status: Tracking Active 🟢";
    startBtn.disabled = true;
    stopBtn.disabled = false;
    console.log("Tracking started.");
});

stopBtn.addEventListener("click", () => {
    statusText.textContent = "Status: Tracking Stopped 🔴";
    startBtn.disabled = false;
    stopBtn.disabled = true;
    console.log("Tracking stopped.");
});

cameraToggleBtn.addEventListener("click", () => {
    if (isCameraOn) {
        // Turn camera off
        webcamFeed.src = ""; // Stop the video feed
        cameraToggleBtn.textContent = "Turn Camera On";
        statusText.textContent = "Status: Camera Off 🔴";
        isCameraOn = false;
        console.log("Camera turned off.");
    } else {
        // Turn camera on
        webcamFeed.src = "{{ url_for('video_feed') }}"; // Restart the video feed
        cameraToggleBtn.textContent = "Turn Camera Off";
        statusText.textContent = "Status: Camera On 🟢";
        isCameraOn = true;
        console.log("Camera turned on.");
    }
});

// Future Feature: Mouse Movement with Finger Gestures
let isMouseControlEnabled = false;

function enableMouseControl() {
    isMouseControlEnabled = true;
    console.log("Mouse control enabled.");
}

function disableMouseControl() {
    isMouseControlEnabled = false;
    console.log("Mouse control disabled.");
}

// Example: Simulate mouse movement (to be integrated with hand tracking data)
function moveMouse(x, y) {
    if (isMouseControlEnabled) {
        console.log(`Moving mouse to (${x}, ${y})`);
        // Implement mouse movement logic here
    }
}

// Example: Simulate mouse click (to be integrated with hand tracking data)
function simulateClick() {
    if (isMouseControlEnabled) {
        console.log("Simulating mouse click.");
        // Implement mouse click logic here
    }
}