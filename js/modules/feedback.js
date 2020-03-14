(function FeedbackModule(){
  document.querySelectorAll('.feedback-container').forEach(function(feedbackEl){
    var feedbackElId = feedbackEl.getAttribute('id')
    var idfragment = feedbackElId.split('feedback-container-')[1]
    var feedbackToggle = feedbackEl.querySelector('#feedback-toggle-' + idfragment)
    var formContainer = document.getElementById('feedback-form-container-' + idfragment)

    if (window.localStorage) {
      var textarea = formContainer.querySelector('textarea')
      var key = 'feedback-' + idfragment
      var maxCharsCount = formContainer.querySelector('.max-1000-characters')
      var maxCharsHint = formContainer.querySelector('.max-char-hint')

      previousText = window.localStorage.getItem(key)
      textarea.value = previousText || ''
      maxCharsCount.textContent = previousText && previousText.length || 0

      textarea.oninput = function(e) {
        var feedbackText = e.target.value

        if (feedbackText.length >= 1500) {
          textarea.value = feedbackText.slice(0, 1500)
          maxCharsHint.classList.add('red')
        } else {
          maxCharsHint.classList.remove('red')
        }

        maxCharsCount.textContent = textarea.value.length

        window.setTimeout(function() {
          window.localStorage.setItem('feedback-' + idfragment, textarea.value)
        }, 0)
      }

    }


    feedbackToggle.onclick = function() {
      if (getComputedStyle(formContainer).getPropertyValue('display') == 'none'){
        formContainer.style = 'display: block'

        if (window.location) {
          var clearedUrl = window.location.href.replace(/#.+/, '')
          window.location.href = clearedUrl + '#' + feedbackElId
        }
      } else {
        formContainer.style = 'display: none'
      }
    }

  });
})();