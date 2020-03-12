(function FeedbackModule(){
  document.querySelectorAll('.leave-feedback').forEach(function(feedbackEl){
    feedbackEl.onclick = function(){
      var idFragment = feedbackEl.getAttribute('id').split('feedback-toggle-')[1]
      var formContainer = document.getElementById('feedback-form-container-' + idFragment)
      if (getComputedStyle(formContainer).getPropertyValue('display') == 'none'){
        formContainer.style = 'display: block'
        textarea = formContainer.querySelector('textarea')
        textarea.focus()
      } else {
        formContainer.style = 'display: none'
      }
    }
  });
})();