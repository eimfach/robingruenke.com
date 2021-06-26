document.addEventListener('DOMContentLoaded', function () {
  ;(function StartUpModule () {
    document.body.className = 'grayscale'
  })()
  ;(function MenuModule () {
    var journalContent = document.getElementById('journal')
    var aboutContent = document.getElementById('about')
    var workContent = document.getElementById('work')
    var showCasesContent = document.getElementById('show')
    var contactButton = document.getElementById('cn')

    var lastActiveView = aboutContent
    var lastActiveBodyId

    activateViewByUrlOnce()
    stopEventPropagationOnContactButton(contactButton)
    bindMobileMenuToggleClickEvent()
    bindMenuItemClickEvents()

    function activateViewByUrlOnce () {
      var defaultVisibleElId = 'about'
      if (window.location) {
        var hash = window.location.hash
        if (hash.length > 1) {
          hash = hash.replace(/^\#/, '')

          if (hash !== defaultVisibleElId) {
            var navigationEl = document.getElementById(hash)
            if (navigationEl) {
              document.body.id = lastActiveBodyId = 'view-' + hash
              displayNotElement(defaultVisibleElId)
              displayElement(navigationEl)
              lastActiveView = navigationEl
            }
          }
        }
      }
    }

    function bindMenuItemClickEvents () {
      var mobileMenuToggleContainer = document.getElementById(
        'mobile-menu-toggle-container'
      )
      document.querySelectorAll('.menu .item').forEach(function (menuItem) {
        menuItem.addEventListener('click', function () {
          displayNotElement(mobileMenuToggleContainer)

          switch (menuItem.id) {
            case 'mobile-menu-button-journal':
            case 'menu-button-journal':
              showView(journalContent, 'view-journal')
              break

            case 'mobile-menu-button-about':
            case 'menu-button-about':
              showView(aboutContent, 'view-about')
              break

            case 'mobile-menu-button-work':
            case 'menu-button-work':
              showView(workContent, 'view-work')
              break

            case 'mobile-menu-button-show':
            case 'menu-button-show':
              showView(showCasesContent, 'view-show')
              break

            default:
              console.error('Invalid Menu Item traversed')
              break
          }
        })
      })
    }

    function bindMobileMenuToggleClickEvent () {
      var mobileMenuToggleContainer = document.getElementById(
        'mobile-menu-toggle-container'
      )
      document.getElementById('mobile-menu-toggle').onclick = function () {
        if (
          getComputedStyle(mobileMenuToggleContainer).getPropertyValue(
            'display'
          ) === 'none'
        ) {
          if (document.body.id === 'view-about') {
            lastActiveBodyId = document.body.id
            document.body.id = 'mobile-menu-bottom-wave'
          }
          mobileMenuToggleContainer.style = 'display: block'
        } else {
          if (lastActiveBodyId === 'view-about') {
            document.body.id = lastActiveBodyId
          }
          mobileMenuToggleContainer.style = 'display: none'
        }
      }
    }

    function displayElement (el) {
      el.style = 'display: block'
    }

    function displayNotElement (el) {
      el.style = 'display: none'
    }

    function newNavigationHistoryEntry (id) {
      if (window.history) {
        window.history.pushState(null, null, '#' + id)
      }
    }

    function showView (view, bodyRef) {
      document.body.id = lastActiveBodyId = bodyRef
      if (view == lastActiveView) return

      displayElement(view)
      displayNotElement(lastActiveView)
      lastActiveView = view

      newNavigationHistoryEntry(view.id)
    }

    function stopEventPropagationOnContactButton (contactButton) {
      contactButton.onclick = function (e) {
        e.stopPropagation()
      }
    }
  })()
  ;(function ResourceModule () {
    var ytShowCase = document.getElementById('showcase-yt-thumbnail')
    ytShowCase.setAttribute(
      'src',
      'https://i3.ytimg.com/vi/kRXV21tzib8/sddefault.jpg'
    )
  })()
  ;(function ServiceOfferModule () {
    var toggleShopForm = document.getElementById('toggle-shop-form')
    var toggleWebAppForm = document.getElementById('toggle-webapp-form')
    var toggleToolForm = document.getElementById('toggle-tool-form')

    var shopForm = document.getElementById('service-shop-form-container')
    var webAppForm = document.getElementById('service-webapp-form-container')
    var toolForm = document.getElementById('service-tool-form-container')

    var currentVisibleForm

    var shopFormTextarea = shopForm.querySelector('textarea')
    var webAppFormTextarea = webAppForm.querySelector('textarea')
    var toolFormTextarea = toolForm.querySelector('textarea')

    toggleShopForm.onclick = toggleVisibility(shopForm)

    toggleWebAppForm.onclick = toggleVisibility(webAppForm)

    toggleToolForm.onclick = toggleVisibility(toolForm)

    shopForm.querySelector('.close').onclick = toggleVisibility(shopForm)

    webAppForm.querySelector('.close').onclick = toggleVisibility(webAppForm)

    toolForm.querySelector('.close').onclick = toggleVisibility(toolForm)

    hydrateFromPersistanceStorage(shopForm.getAttribute('id'), shopFormTextarea)
    hydrateFromPersistanceStorage(
      webAppForm.getAttribute('id'),
      webAppFormTextarea
    )
    hydrateFromPersistanceStorage(toolForm.getAttribute('id'), toolFormTextarea)

    persistInput(shopForm.getAttribute('id'), shopFormTextarea)
    persistInput(webAppForm.getAttribute('id'), webAppFormTextarea)
    persistInput(toolForm.getAttribute('id'), toolFormTextarea)

    function hydrateFromPersistanceStorage (key, textarea) {
      if (window.localStorage) {
        var persistanceValue = window.localStorage.getItem(key)
        if (persistanceValue) {
          textarea.value = persistanceValue
        }
      }
    }

    function persistInput (key, textarea) {
      if (window.localStorage) {
        textarea.oninput = function () {
          window.setTimeout(function () {
            window.localStorage.setItem(key, textarea.value)
          }, 10)
        }
      }
    }

    function toggleVisibility (form) {
      return function () {
        if (getComputedStyle(form).getPropertyValue('display') == 'none') {
          if (currentVisibleForm) {
            currentVisibleForm.style = 'display: none'
          }
          form.style = 'display: block'
          currentVisibleForm = form
        } else {
          form.style = 'display: none'
        }
      }
    }
  })()
})
