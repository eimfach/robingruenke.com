(function LikeSubmitModule(){
  var featureContainer = document.getElementById('feature-like-journal')

  if (featureContainer) {
    if (typeof window.fetch === 'function') {
      var likeform = featureContainer.querySelector('#like-form')
      var submitIcon = likeform.querySelector('.submit')
  
      likeform.onsubmit = function(e){
        e.preventDefault()

        submitIcon.onclick = null
        submitIcon.classList.remove('icon-bubble-love-streamline-talk')
        submitIcon.classList.remove('font-big')
        submitIcon.textContent = 'Thanks :)'

        formData = {
          method: likeform.method,
          headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
          },
          body: new URLSearchParams(new FormData(likeform)).toString()
        }
        // send the form
        fetch('/', formData)
        
      }
  
      submitIcon.onclick = function(){
        // HTMLFormElement.prototype.requestSubmit helps with applying a form submit event emitter on any element besides button and input
        // It does trigger a submit event (HTMLFormElement.prototype.submit does not)
        likeform.requestSubmit()
      }
    } else {
      // disable like feature if fetch api is not supported by client browser
      featureContainer.style = 'display: none'
    }

  }

})();