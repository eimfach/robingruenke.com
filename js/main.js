document.addEventListener("DOMContentLoaded", function(event) {

  (function StartUpModule(){
    document.body.className = "grayscale"
  })();

  (function ArticleUpdateHintModule(){
    if(window.localStorage) {
      var pageTitle = document.getElementById('pagetitle').textContent.trim().split(' ').join('-').toLowerCase()
      var key = pageTitle + '-article-count'
      lastChapterCount = localStorage.getItem(key)

      if(!lastChapterCount) {
        localStorage.setItem(key, countChapters())
      } else {
        updatedChapterCount = countChapters()

        if (updatedChapterCount > lastChapterCount) {
          // enable blockquote highlight
          highlightEl = document.getElementById('new-chapter-message');
          if (highlightEl) {
            highlightEl.style = 'display: block'
          }
          localStorage.setItem(key, updatedChapterCount)
        }
      }
    }

    function countChapters() {
      chapterCount = 0

      document.querySelectorAll('.chapter').forEach(function(el) {
        chapterCount = chapterCount + 1
      });

      return chapterCount
    }
  })();
  
});