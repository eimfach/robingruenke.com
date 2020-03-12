(function ChapterIndexModule(){
  chapterIndexToggle = document.getElementById('chapter-index-toggle')
  chapterIndexList = document.getElementById('chapter-index-list')
  if (chapterIndexToggle) {
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