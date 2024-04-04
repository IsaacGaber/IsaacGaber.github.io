// Helper Functions
var blinking = false;
var blinkCount = 0;
const blinkWait = 2; // wait two frames before switching blinking to true
const blinkThres = .3;
// -----------------------------------------------------------------------------
function elementInViewport2(el) {
  var top = el.offsetTop;
  var left = el.offsetLeft;
  var width = el.offsetWidth;
  var height = el.offsetHeight;

  while(el.offsetParent) {
    el = el.offsetParent;
    top += el.offsetTop;
    left += el.offsetLeft;
  }

  return (
    top < (window.pageYOffset + window.innerHeight) &&
    left < (window.pageXOffset + window.innerWidth) &&
    (top + height) > window.pageYOffset &&
    (left + width) > window.pageXOffset
  );
}

var currentAudio;
function update_visible(el){
  // changes colors of all visible to red
  for (let i = 0; i < el.length; i++) {
    const selected = el[i];
    const visible = elementInViewport2(selected);

    // console.log(selected)
    if (selected.children.length > 0){
      const audio = selected.querySelector("audio");
      if (audio && audio.playing && visible && blinking){
      } else if (audio && visible && blinking) {
        audio.play();
        currentAudio = audio;
      } else if (audio){
        audio.pause();
        // audio.currentTime = 0.0;
      }
    }
  }
}
// -----------------------------------------------------------------------------

const element = document.querySelectorAll("p");
//  set event handler
var handler = function () {update_visible(element)};

window.addEventListener('DOMContentLoaded', handler);
window.addEventListener('load', handler);
window.addEventListener('scroll', handler);
window.addEventListener('resize', handler);

// Facial Detecton
import vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3";
const { FaceLandmarker, FilesetResolver, DrawingUtils } = vision;
const videoWidth = 480;


let faceLandmarker;

async function loadVision() {
  const vision = await FilesetResolver.forVisionTasks(
    // path/to/wasm/root
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
  );
  faceLandmarker = await FaceLandmarker.createFromOptions(
      vision,
      {
        baseOptions: {
          modelAssetPath: "face_landmarker.task",
          delegate: "GPU"
        },
        outputFaceBlendshapes: true,
        runningMode: "VIDEO",
        numFaces: 1
      });
}
loadVision();

var webcamRunning = false;
const video = document.getElementById("webcam");
const image = document.getElementById("image");
const output = document.getElementById("output");
// const button = document.getElementById("imageButton");
//
// button.addEventListener("click", function () {
//   console.log(faceLandmarker.detect(image).faceBlendshapes)
// });
// Check if webcam access is supported.
function hasGetUserMedia() {
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

// If webcam supported, add event listener to button for when user
// wants to activate it.

if (hasGetUserMedia()) {
  var enableWebcamButton = document.getElementById(
    "webcamButton"
  );
  enableWebcamButton.addEventListener("click", enableCam);
} else {
  console.warn("getUserMedia() is not supported by your browser");
}

function enableCam(event) {
  if (!faceLandmarker) {
    console.log("Wait! faceLandmarker not loaded yet.");
    return;
  }

  if (webcamRunning === true) {
    webcamRunning = false;
    enableWebcamButton.innerText = "ENABLE VIDEO";
  } else {
    webcamRunning = true;
    enableWebcamButton.innerText = "DISABLE VIDEO";
  }

  // getUsermedia parameters.
  const constraints = {
    video: true
  };

  // Activate the webcam stream.
  navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    video.srcObject = stream;
    video.addEventListener("loadeddata", predictWebcam);
  });
}


let lastVideoTime = -1;
let results = undefined;
async function predictWebcam() {
  const radio = video.videoHeight / video.videoWidth;
  video.style.width = videoWidth + "px";
  video.style.height = videoWidth * radio + "px";

  let startTimeMs = performance.now();
  if (lastVideoTime !== video.currentTime) {
    lastVideoTime = video.currentTime;
    results = faceLandmarker.detectForVideo(video, startTimeMs);
  }
  // if (results.faceBlendshapes[0].categories) {
  const blinkAverage = (results.faceBlendshapes[0].categories[9].score
  + results.faceBlendshapes[0].categories[10].score)/2;
  console.log(blinkAverage);
  if (blinkAverage > blinkThres) {
    blinkCount += 1;
    blinkCount = Math.min(blinkCount, blinkWait+2);
    if (blinkCount > blinkWait);
      output.innerText = "blinking";
      blinking = true;
      update_visible(element);
  } else {
    blink -= 1;
    output.innerText = "eyes open";
    if (blinkCount < blinkWait) {
      blinking = false;
    }
  }
  // }
    // Call this function again to keep predicting when the browser is ready.
  if (webcamRunning === true) {
    window.requestAnimationFrame(predictWebcam);
  }
}
