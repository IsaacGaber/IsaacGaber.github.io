// Helper Functions
var blinking = false;
var blinkCount = 0;
const blinkWait = 8; // wait some frames before switching blinking to true
const blinkThres = .5;
const fadeOut = .05;
const fadeIn = .05;
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
var blink = false;
function update_visible(el){
  // changes colors of all visible to red
  for (let i = 0; i < el.length; i++) {
    const selected = el[i];
    const visible = elementInViewport2(selected);

    // console.log(selected)
    if (selected.children.length > 0){
      const audio = selected.querySelector("audio");
      // console.log(audio.volume)
      console.log(audio.playing)
      if (audio && !audio.playing && visible && blinking){
        // audio.volume *= 1.1
        console.log("audio started")
        audio.play();
        // audio.addEventListener("ended", function () {finishedAudio = true})
        audio.volume = 1;
        currentAudio = audio;
      // } else if (!blinking && !audio.playing) {
      //   finishedAudio = false
      } else {
        if (audio.volume <= .1){
          audio.pause();
          audio.volume = 0;
        } else {
          audio.volume -= fadeOut;
        }
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
// const output = document.getElementById("output");
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
  enableWebcamButton.remove()
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
  // console.log()
  // if (results.faceBlendshapes[0].categories) {
  if (results.faceLandmarks.length > 0) {
    const blinkAverage = (results.faceBlendshapes[0].categories[9].score
    + results.faceBlendshapes[0].categories[10].score)/2;
    // console.log(blinkAverage);
    // console.log(blinking)
    if (blinkAverage > blinkThres) {
      blinkCount += 1;
      blinkCount = Math.min(blinkCount, blinkWait+2);
      if (blinkCount > blinkWait){
        // output.innerText = "blinking";
        blinking = true;
      }
    }else {
        blinkCount -= 1;
        blinkCount = Math.max(blinkCount, 0);
        // console.log(blinkCount)
        // output.innerText = "eyes open";
        if (blinkCount < blinkWait) {
          blinking = false;
        }
    }
  } else {
    blinkCount = blinkCount;
    blinking = blinking;
    // output.innerText = "face not detected";
  }

  // Refresh music and currently visible els
  update_visible(element);
  // }
    // Call this function again to keep predicting when the browser is ready.
  if (webcamRunning === true) {
    window.requestAnimationFrame(predictWebcam);
  }
}
