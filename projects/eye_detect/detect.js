// import vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3";
//
// const { FaceLandmarker, FilesetResolver, DrawingUtils } = vision;
//
// // Before we can use HandLandmarker class we must wait for it to finish
// // loading. Machine Learning models can be large and take a moment to
// // get everything needed to run.
// const faceLandmarker = await FaceLandmarker.createFromOptions(
//     vision,
//     {
//       baseOptions: {
//         modelAssetPath: "path/to/model"
//       },
//       // runningMode: "IMAGE"
//     });
// console.log("face landmarker loaded");


// async function createFaceLandmarker() {
//
//   const filesetResolver = await FilesetResolver.forVisionTasks(
//     "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
//   );
//   faceLandmarker = await FaceLandmarker.createFromOptions(filesetResolver, {
//     baseOptions: {
//       modelAssetPath: `face_landmarker.task`,
//       delegate: "GPU"
//     },
//     outputFaceBlendshapes: true,
//     runningMode: "image",
//     numFaces: 1
//   });
//   // demosSection.classList.remove("invisible");
// }
// createFaceLandmarker();
//
const image = document.getElementById("image");
// console.log(image)
// const faceLandmarkerResult = faceLandmarker.detect(image);
//
// console.log(vision)
// console.log(faceLandmarkerResult);

 // end of code
// })();
