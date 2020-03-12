(function LikeSubmitModule(){
  var likeform = document.querySelector('.like-form')
  if (likeform) {
    likeform.querySelector('.submit').onclick = function(){
      likeform.submit()
    }
  }
})();