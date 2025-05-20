;(function ChapterIndexModule () {
  var chapterIndexToggle = document.getElementById('chapter-index-toggle')
  var chapterIndexList = document.getElementById('chapter-index-list')
  if (chapterIndexToggle && chapterIndexList) {
    chapterIndexToggle.onclick = function () {
      if (getComputedStyle(chapterIndexList).getPropertyValue('display') === 'none') {
        chapterIndexToggle.style = 'text-align: left'
        chapterIndexList.style = 'display: block'
      } else {
        chapterIndexList.style = 'display: none'
        chapterIndexToggle.style = 'text-align: center'
      }
    }
  }
})()
