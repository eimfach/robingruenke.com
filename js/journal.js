document.addEventListener("DOMContentLoaded", function(event) {

  (function StartUpModule(){
    document.body.className = "grayscale"
  })();

  (function ChapterIndexModule(){
    chapterIndexToggle = document.getElementById('chapter-index-toggle')
    chapterIndexList = document.getElementById('chapter-index-list')

    chapterIndexToggle.onclick = function(){
      if (getComputedStyle(chapterIndexList).getPropertyValue("display") === "none") {
        chapterIndexToggle.style = 'text-align: left'
        chapterIndexList.style = 'display: block'
      } else {
        chapterIndexList.style = 'display: none'
        chapterIndexToggle.style = 'text-align: center'
      }
       
    }
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
          highlightEl = document.getElementById('new-chapter-hint');

          if (highlightEl) {
            
            firstNewChapterEl = document.querySelectorAll('.chapter')[lastChapterCount]
            firstNewChapterElId = firstNewChapterEl.getAttribute('id')

            highlightEl.setAttribute('href', '#' + firstNewChapterElId)
            
            highlightEl.style = 'display: block'

            localStorage.setItem(key, updatedChapterCount)
          }
          
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