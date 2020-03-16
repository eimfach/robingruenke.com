document.addEventListener("DOMContentLoaded", function(event) {

  (function StartUpModule(){
    document.body.className = "grayscale"
  })();


  (function MenuModule(){

    var journalContent = document.getElementById("journal")
    var aboutContent = document.getElementById("about")
    var workContent = document.getElementById("work")
    var showCasesContent = document.getElementById("show")

    var lastActiveNode = aboutContent

    /* URL */
    var defaultVisibleElId = 'about'

    if (window.location) {
      var hash = window.location.hash
      if (hash.length > 1){
        hash = hash.replace(/^\#/, '')

        if (hash !== defaultVisibleElId) {
          navigationEl = document.getElementById(hash)
          if (navigationEl) {
            document.getElementById(defaultVisibleElId).style = 'display: none'
            navigationEl.style = 'display: block'
            lastActiveNode = navigationEl
          }
        }

      }
    }

    /* MENU ACTIONS */
    var mobileMenuToggleContainer = document.getElementById("mobile-menu-toggle-container")

    /* MOBILE MENU */
    document.getElementById("mobile-menu-toggle").onclick = function() {
      if (getComputedStyle(mobileMenuToggleContainer).getPropertyValue("display") === "none") {
        mobileMenuToggleContainer.style = "display: block"
      } else {
        mobileMenuToggleContainer.style = "display: none"
      }
    }

    document.querySelectorAll("#mobile-menu-toggle-container .item").forEach(function(menuItem) {
      menuItem.addEventListener("click", function() {
        mobileMenuToggleContainer.style = "display: none"
      })
    })

    document.getElementById("mobile-menu-button-journal").addEventListener("click", createToggleHandle(journalContent))
    document.getElementById("mobile-menu-button-about").addEventListener("click", createToggleHandle(aboutContent))
    document.getElementById("mobile-menu-button-work").addEventListener("click", createToggleHandle(workContent)) 
    document.getElementById("mobile-menu-button-show").addEventListener("click", createToggleHandle(showCasesContent))

    /* REGULAR MENU */
    document.getElementById("menu-button-journal").onclick = createToggleHandle(journalContent)
    document.getElementById("menu-button-about").onclick = createToggleHandle(aboutContent)
    document.getElementById("menu-button-work").onclick = createToggleHandle(workContent)
    document.getElementById("menu-button-show").onclick = createToggleHandle(showCasesContent)

    /* HELPERS */
    function createToggleHandle(item) {
      return function() {
        toggleView(item)
      }
    }

    function toggleView(item) {
      if (item == lastActiveNode) return

      item.style = "display: block";
      lastActiveNode.style = "display: none";
      lastActiveNode = item;
      if (window.history) {
        window.history.pushState(null, null, '#' + item.getAttribute('id'))
      }
    }
  })();

  (function ResourceModule(){
    var ytShowCase = document.getElementById('showcase-yt-thumbnail')
    ytShowCase.setAttribute("src", "https://i3.ytimg.com/vi/kRXV21tzib8/sddefault.jpg")
  })();

});