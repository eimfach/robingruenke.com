document.addEventListener("DOMContentLoaded", function(event) {

  (function StartUpModule(){
    document.body.className = "grayscale"
  })();

  (function ArticleUpdateHintModule(){
    if(window.localStorage) {
      lastChapterCount = localStorage.getItem('article-count')

      if(!lastChapterCount) {
        localStorage.setItem('article-count', countChapters())
      } else {
        updatedChapterCount = countChapters()
        console.log(updatedChapterCount, lastChapterCount)
        if (updatedChapterCount > lastChapterCount) {
          // enable blockquote highlight
          highlightEl = document.getElementById('new-chapter-message');
          if (highlightEl) {
            highlightEl.style = 'display: block'
          }
          localStorage.setItem('article-count', updatedChapterCount)
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