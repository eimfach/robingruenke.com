// audio module
;(function () {
  var context = createAudioContext()

  if (context === undefined) {
    return
  }

  var gainNode = context.createGain()
  gainNode.gain.value = 0.01
  gainNode.connect(context.destination)

  var request = new XMLHttpRequest()

  request.open('GET', '/audio/tonight-c-3.wav')
  request.responseType = 'arraybuffer'
  request.onload = function () {
    context.decodeAudioData(request.response, onDecoded)
  }

  request.send()

  function onDecoded (audioBuffer) {
    var bufferSource = context.createBufferSource()
    bufferSource.buffer = audioBuffer
    bufferSource.connect(gainNode)
    bufferSource.start()
  }

  function createAudioContext () {
    if (window.AudioContext) {
      return new window.AudioContext()
    } else if (window.webkitAudioContext) {
      return new window.webkitAudioContext()
    }
  }
})()
