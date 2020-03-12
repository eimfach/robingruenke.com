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