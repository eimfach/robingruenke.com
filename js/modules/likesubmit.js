;(function LikeSubmitModule () {
  var featureContainer = document.getElementById('feature-like-journal')

  if (featureContainer) {
    var likeForm = featureContainer.querySelector('#like-form')
    var submitIcon = likeForm.querySelector('.submit')

    submitIcon.onclick = function () {
      // HTMLFormElement.prototype.requestSubmit helps with applying a form submit event emitter on any element besides button and input
      // It does trigger a submit event (HTMLFormElement.prototype.submit does not)
      likeForm.requestSubmit()
    }

    if (typeof window.fetch === 'function') {
      likeForm.onsubmit = function (e) {
        e.preventDefault()

        submitIcon.onclick = null
        submitIcon.classList.remove('icon-bubble-love-streamline-talk')
        submitIcon.classList.remove('font-big')
        submitIcon.textContent = 'Thanks :)'

        var formData = {
          method: likeForm.method,
          headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
          },
          body: new URLSearchParams(new FormData(likeForm)).toString()
        }
        // send the form
        fetch('/', formData).catch(function () {
          var retries = 0
          var interval = setInterval(function () {
            if (retries === 10) {
              clearInterval(interval)
            } else {
              retries = retries + 1
              fetch('/', formData).then(function () {
                clearInterval(interval)
              })
            }
          }, 20000)
        })
      }
    }
  }
})()
