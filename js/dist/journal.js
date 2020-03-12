// auto generated, don't modify 

document.addEventListener("DOMContentLoaded", function(event) {

(function StartUpModule(){
  document.body.className = "grayscale"
})();

(function ChapterIndexModule(){
  var chapterIndexToggle = document.getElementById('chapter-index-toggle')
  var chapterIndexList = document.getElementById('chapter-index-list')
  if (chapterIndexToggle && chapterIndexList) {
    chapterIndexToggle.onclick = function(){
      if (getComputedStyle(chapterIndexList).getPropertyValue("display") === "none") {
        chapterIndexToggle.style = 'text-align: left'
        chapterIndexList.style = 'display: block'
      } else {
        chapterIndexList.style = 'display: none'
        chapterIndexToggle.style = 'text-align: center'
      }
       
    }
  }

})();

(function ArticleUpdateHintModule(){
  if(window.localStorage) {
    var pageTitle = document.getElementById('pagetitle').textContent.trim().split(' ').join('-').toLowerCase()
    var key = pageTitle + '-article-count'
    var lastChapterCount = localStorage.getItem(key)

    if(!lastChapterCount) {
      localStorage.setItem(key, countChapters())
    } else {
      var updatedChapterCount = countChapters()

      if (updatedChapterCount > lastChapterCount) {
        // enable blockquote highlight
        var highlightEl = document.getElementById('new-chapter-hint')

        if (highlightEl) {
          
          var firstNewChapterEl = document.querySelectorAll('.chapter')[lastChapterCount]
          var firstNewChapterElId = firstNewChapterEl.getAttribute('id')

          highlightEl.setAttribute('href', '#' + firstNewChapterElId)
          
          highlightEl.style = 'display: block'

          localStorage.setItem(key, updatedChapterCount)
        }
        
      }
    }
  }

  function countChapters() {
    var chapterCount = 0

    document.querySelectorAll('.chapter').forEach(function(el) {
      chapterCount = chapterCount + 1
    });

    return chapterCount
  }
})();

(function GalleryModule(){
  document.querySelectorAll('.gallery-background').forEach(function(topEl){
    var mainImage = topEl.querySelector('.main-image');

      topEl.querySelectorAll('.gallery-picture').forEach(function(img){

        img.onclick = function() {
          var imgSrc = img.getAttribute('src')
          var mainImageSrc = mainImage.getAttribute('src')
          
          img.setAttribute('src', mainImageSrc)
          mainImage.setAttribute('src', imgSrc)
        }
      });

  });
})();

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

(function LikeSubmitModule(){
  var likeform = document.querySelector('.like-form')
  if (likeform) {
    likeform.querySelector('.submit').onclick = function(){
      likeform.submit()
    }
  }
})();




});