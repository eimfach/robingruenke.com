(function FeedbackModule(){
  document.querySelectorAll('.feedback-container').forEach(function(feedbackEl){
    var feedbackElId = feedbackEl.getAttribute('id')
    var idfragment = feedbackElId.split('feedback-container-')[1]
    var feedbackToggle = feedbackEl.querySelector('#feedback-toggle-' + idfragment)
    var formContainer = document.getElementById('feedback-form-container-' + idfragment)

    feedbackToggle.onclick = function() {
      if (getComputedStyle(formContainer).getPropertyValue('display') == 'none'){
        formContainer.style = 'display: block'

        if (window.location) {
          clearedUrl = window.location.href.replace(/#.+/, '')
          window.location.href = clearedUrl + '#' + feedbackElId
        }
      } else {
        formContainer.style = 'display: none'
      }
    }

  });
})();