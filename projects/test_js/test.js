// Helper Functions
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
      if (audio && audio.playing && visible){
      } else if (audio && visible) {
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
