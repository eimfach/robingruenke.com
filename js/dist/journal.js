// auto generated, don't modify 

document.addEventListener("DOMContentLoaded", function(event) {

;(function ApiModule () {
  var api = {}

  defineReadOnlyProperty('extendApi', extendApi)
  defineReadOnlyProperty('empty', empty)
  defineReadOnlyProperty('hide', hide)
  defineReadOnlyProperty('setFontColor', setFontColor)
  defineReadOnlyProperty('setText', setText)

  function defineReadOnlyProperty (name, value) {
    Object.defineProperty(api, name, {
      value: value,
      writeable: false
    })
  }

  function empty (el) {
    while (el.firstChild) {
      el.removeChild(el.firstChild)
    }
  }

  function extendApi (name, val) {
    defineReadOnlyProperty(name, val)
  }

  function hide (cssSelector) {
    document.querySelector(cssSelector).style = 'display: none'
  }

  function setFontColor (cssSelector, color) {
    document.querySelector(cssSelector).style = 'color: ' + color
  }

  function setText (cssSelector, text) {
    var el = document.querySelector(cssSelector)
    var node = document.createTextNode(text)
    empty(el)
    el.appendChild(node)
  }

  window.robingruenkedotcom = api
})()

// https://github.com/javan/form-request-submit-polyfill/blob/master/form-request-submit-polyfill.js
;(function RequestSubmitPolyfillModule (prototype) {
  if (typeof prototype.requestSubmit == 'function') return

  prototype.requestSubmit = function (submitter) {
    if (submitter) {
      validateSubmitter(submitter, this)
      submitter.click()
    } else {
      submitter = document.createElement('input')
      submitter.type = 'submit'
      submitter.hidden = true
      this.appendChild(submitter)
      submitter.click()
      this.removeChild(submitter)
    }
  }

  function validateSubmitter (submitter, form) {
    submitter instanceof HTMLElement ||
      raise(TypeError, "parameter 1 is not of type 'HTMLElement'")
    submitter.type == 'submit' ||
      raise(TypeError, 'The specified element is not a submit button')
    submitter.form == form ||
      raise(
        DOMException,
        'The specified element is not owned by this form element',
        'NotFoundError'
      )
  }

  function raise (errorConstructor, message, name) {
    throw new errorConstructor(
      "Failed to execute 'requestSubmit' on 'HTMLFormElement': " +
        message +
        '.',
      name
    )
  }
})(HTMLFormElement.prototype)

// https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent
;(function CustomEventPolyfillModule () {
  if (typeof window.CustomEvent === 'function') return false

  function CustomEvent (event, params) {
    params = params || { bubbles: false, cancelable: false, detail: null }
    var evt = document.createEvent('CustomEvent')
    evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail)
    return evt
  }

  window.CustomEvent = CustomEvent
})()

// Source: https://gist.github.com/k-gun/c2ea7c49edf7b757fe9561ba37cb19ca
/**
 * Element.prototype.classList for IE8/9, Safari.
 * @author    Kerem Güneş <k-gun@mail.com>
 * @copyright Released under the MIT License <https://opensource.org/licenses/MIT>
 * @version   1.2
 * @see       https://developer.mozilla.org/en-US/docs/Web/API/Element/classList
 */
;(function ClassListPolyfillModule () {
  // Helpers.
  var trim = function (s) {
      return s.replace(/^\s+|\s+$/g, '')
    },
    regExp = function (name) {
      return new RegExp('(^|\\s+)' + name + '(\\s+|$)')
    },
    forEach = function (list, fn, scope) {
      for (var i = 0; i < list.length; i++) {
        fn.call(scope, list[i])
      }
    }

  // Class list object with basic methods.
  function ClassList (element) {
    this.element = element
  }

  ClassList.prototype = {
    add: function () {
      forEach(
        arguments,
        function (name) {
          if (!this.contains(name)) {
            this.element.className = trim(this.element.className + ' ' + name)
          }
        },
        this
      )
    },
    remove: function () {
      forEach(
        arguments,
        function (name) {
          this.element.className = trim(
            this.element.className.replace(regExp(name), ' ')
          )
        },
        this
      )
    },
    toggle: function (name) {
      return this.contains(name)
        ? (this.remove(name), false)
        : (this.add(name), true)
    },
    contains: function (name) {
      return regExp(name).test(this.element.className)
    },
    item: function (i) {
      return this.element.className.split(/\s+/)[i] || null
    },
    // bonus
    replace: function (oldName, newName) {
      this.remove(oldName), this.add(newName)
    }
  }

  // IE8/9, Safari
  // Remove this if statements to override native classList.
  if (!('classList' in Element.prototype)) {
    // Use this if statement to override native classList that does not have for example replace() method.
    // See browser compatibility: https://developer.mozilla.org/en-US/docs/Web/API/Element/classList#Browser_compatibility.
    // if (!('classList' in Element.prototype) ||
    //     !('classList' in Element.prototype && Element.prototype.classList.replace)) {
    Object.defineProperty(Element.prototype, 'classList', {
      get: function () {
        return new ClassList(this)
      }
    })
  }

  // For others replace() support.
  if (window.DOMTokenList && !DOMTokenList.prototype.replace) {
    DOMTokenList.prototype.replace = ClassList.prototype.replace
  }
})()


;(function StartUpModule () {
  document.body.className = 'grayscale'
})()


;(function PushSubscriptionModule () {
  if (!browserSupport()) {
    return
  }

  var User = UserSubscriptionState()

  if (Notification.permission !== 'granted') {
    nonTrackingUserSignalizationToBeUnsubscribed()
  } else if (User.isSubscribed()) {
    userSuccessFeedback('Subscription active')
  }

  listenForNotificationPermissionRevokation()
  displaySubscribeButton()

  function _subscribe () {
    if (User.isUnsubscribed()) {
      User.setSubscriptionPending()
      userSuccessFeedback('Subscription pending ...').then(function () {
        try {
          Notification.requestPermission().then(
            progressSubscriptionIfUserAgreed
          )
        } catch (e) {
          userErrorFeedback(
            'Sorry, Browser lacks conformity on Notification API.'
          )
        }
      })
    }
  }

  window.robingruenkedotcom.extendApi('subscribe', _subscribe)

  function UserSubscriptionState () {
    var states = ['unsubscribed', 'pending', 'subscribed']
    var statusSynced = window.localStorage.getItem('UserSubscriptionState')
    var status = statusSynced !== null ? statusSynced : states[0]

    return {
      isSubscribed: function () {
        return status === states[2]
      },
      isSubscriptionPending: function () {
        return status === states[1]
      },
      isUnsubscribed: function () {
        return status === states[0]
      },

      persistOnClientSide: function () {
        window.localStorage.setItem('UserSubscriptionState', status)
      },

      setSubscribed: function () {
        status = states[2]
      },
      setSubscriptionPending: function () {
        status = states[1]
      },
      setUnsubscribed: function () {
        status = states[0]
      }
    }
  }

  function applicationServerKey () {
    return 'BFB8jMwrn1Ihszc-5BF8F_xTxgOhbjN0CXQ_Ybdw-c-CLet_2ApuB2Vi4NcQACHuvbZRB6Sc09_f4HWGmVyEcOE'
  }

  function browserSupport () {
    var ableToListenInBackground = 'serviceWorker' in navigator
    var ableToSubscribeToPushService = 'PushManager' in window
    var ableToPersistPushServiceResponse = 'fetch' in window
    var ableToDisplayPushNotifications = 'Notification' in window
    var ableToPersistSubscriptionStatusWithoutUserTracking =
      'localStorage' in window

    return (
      ableToListenInBackground &&
      ableToSubscribeToPushService &&
      ableToPersistPushServiceResponse &&
      ableToDisplayPushNotifications &&
      ableToPersistSubscriptionStatusWithoutUserTracking
    )
  }

  function cacheGetPendingPushSubscription () {
    var raw = localStorage.getItem('PendingPushSubscription')

    if (raw === null) {
      return null
    }

    var timeEncodedResult = JSON.parse(raw)
    var cacheValid =
      msToHours(new Date().getTime() - timeEncodedResult[0]) < 0.1
    return cacheValid ? timeEncodedResult[1] : null
  }

  function cacheSetPendingPushSubscription (pS) {
    localStorage.setItem(
      'PendingPushSubscription',
      JSON.stringify([new Date().getTime(), pS])
    )

    return pS
  }

  function displaySubscribeButton () {
    var sub_button = document.querySelector('#user-sub')
    if (sub_button) {
      sub_button.style = ''
    }
  }

  function handleNotificationPermissionRevocation () {
    return function (e) {
      if (User.isSubscribed() && isPermissionStatusNotGranted(e.target)) {
        nonTrackingUserSignalizationToBeUnsubscribed()
      }
    }
  }

  function isPermissionStatusNotGranted (pS) {
    return pS.state === 'denied' || pS.state === 'prompt'
  }

  // progressive enhancement using the permission api
  function listenForNotificationPermissionRevokation () {
    if ('permissions' in navigator) {
      navigator.permissions
        .query({ name: 'notifications' })
        .then(function (pS) {
          pS.onchange = handleNotificationPermissionRevocation()
        })
    }
  }

  function msToHours (ms) {
    return ms / 1000 / 60 / 60
  }

  function nonTrackingUserSignalizationToBeSubscribed () {
    User.setSubscribed()
    User.persistOnClientSide()
    return userSuccessFeedback('Subscription active')
  }

  function nonTrackingUserSignalizationToBeUnsubscribed () {
    User.setUnsubscribed()
    User.persistOnClientSide()
    return userSuccessFeedback('Subscribe')
  }

  function nonTrackingPersistanceOfSubscriptionOnApi (pushSubscription) {
    return fetch('https://api.robingruenke.com/s/subscription', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(pushSubscription),
      url: 'https://api.robingruenke.com'
    })
  }

  function onceServiceWorkerActive (sW) {
    return new Promise(function (resolve, reject) {
      sW.onerror = reject

      if (sW.state === 'activated') {
        resolve()
      } else {
        sW.onstatechange = function (e) {
          if (e.target.state === 'activated') {
            resolve()
          }
        }
      }
    })
  }

  function progressSubscriptionIfUserAgreed (permission) {
    if (permission === 'granted') {
      registerPushNotificationsListener()
        .then(requestPushSubscriptionFromPushManagerOrCache)
        .then(nonTrackingPersistanceOfSubscriptionOnApi)
        .then(function (response) {
          if (response.ok) {
            nonTrackingUserSignalizationToBeSubscribed()
          } else {
            throwSubscriptionPersistanceError(response)
          }
        })
        .catch(function (e) {
          nonTrackingUserSignalizationToBeUnsubscribed()
          userErrorFeedback('Error: ' + e.message + ' [click to try again]')
        })
    }
  }

  function registerPushNotificationsListener () {
    return navigator.serviceWorker.register(
      '/js/service-worker/push-notifications.js'
    )
  }

  function requestPushSubscriptionFromPushManagerOrCache (registration) {
    var worker =
      registration.installing || registration.waiting || registration.active

    return onceServiceWorkerActive(worker).then(
      requestPushSubscriptionOrReusePending
    )

    function requestPushSubscriptionOrReusePending () {
      var pPS = cacheGetPendingPushSubscription()
      return pPS === null ? requestNewPushSubscription() : Promise.resolve(pPS)
    }

    function requestNewPushSubscription () {
      var withOptions = {
        applicationServerKey: applicationServerKey(),
        userVisibleOnly: true
      }
      return registration.pushManager
        .subscribe(withOptions)
        .then(cacheSetPendingPushSubscription)
    }
  }

  function throwSubscriptionPersistanceError (response) {
    var message = response.status + ' -  Bad API Response'
    if (response.status === 409) {
      message = message + ' [Spam protection] Try again later'
    }
    throw new Error(message)
  }

  function userFeedback (message, color) {
    return new Promise(function (resolve) {
      var selector = '#user-sub'
      if (!document.querySelector(selector)) {
        return false
      }
      robingruenkedotcom.setFontColor(selector, color)
      robingruenkedotcom.setText(selector, message)

      window.setTimeout(resolve, 3000)
    })
  }

  function userErrorFeedback (message) {
    return userFeedback(message, 'orange')
  }

  function userSuccessFeedback (message) {
    return userFeedback(message, 'limegreen')
  }
})()


;(function ChapterIndexModule () {
  var chapterIndexToggle = document.getElementById('chapter-index-toggle')
  var chapterIndexList = document.getElementById('chapter-index-list')
  if (chapterIndexToggle && chapterIndexList) {
    chapterIndexToggle.onclick = function () {
      if (
        getComputedStyle(chapterIndexList).getPropertyValue('display') ===
        'none'
      ) {
        chapterIndexToggle.style = 'text-align: left'
        chapterIndexList.style = 'display: block'
      } else {
        chapterIndexList.style = 'display: none'
        chapterIndexToggle.style = 'text-align: center'
      }
    }
  }
})()


;(function ArticleUpdateHintModule () {
  if (window.localStorage) {
    var pageTitle = document
      .getElementById('pagetitle')
      .textContent.trim()
      .split(' ')
      .join('-')
      .toLowerCase()
    var key = pageTitle + '-article-count'
    var lastChapterCount = localStorage.getItem(key)

    if (!lastChapterCount) {
      localStorage.setItem(key, countChapters())
    } else {
      var updatedChapterCount = countChapters()

      if (updatedChapterCount > lastChapterCount) {
        // enable blockquote highlight
        var highlightEl = document.getElementById('new-chapter-hint')

        if (highlightEl) {
          var firstNewChapterEl = document.querySelectorAll('.chapter')[
            lastChapterCount
          ]
          var firstNewChapterElId = firstNewChapterEl.getAttribute('id')

          highlightEl.setAttribute('href', '#' + firstNewChapterElId)

          highlightEl.style = 'display: block'

          localStorage.setItem(key, updatedChapterCount)
        }
      }
    }
  }

  function countChapters () {
    var chapterCount = 0

    document.querySelectorAll('.chapter').forEach(function () {
      chapterCount = chapterCount + 1
    })

    return chapterCount
  }
})()


;(function GalleryModule () {
  document.querySelectorAll('.gallery-background').forEach(function (topEl) {
    var mainImage = topEl.querySelector('.main-image')

    topEl.querySelectorAll('.gallery-picture').forEach(function (img) {
      img.onclick = function () {
        var imgSrc = img.getAttribute('src')
        var mainImageSrc = mainImage.getAttribute('src')

        img.setAttribute('src', mainImageSrc)
        mainImage.setAttribute('src', imgSrc)
      }
    })
  })
})()


;(function FeedbackModule () {
  document
    .querySelectorAll('.feedback-container')
    .forEach(function (feedbackEl) {
      var feedbackElId = feedbackEl.getAttribute('id')
      var idfragment = feedbackElId.split('feedback-container-')[1]
      var feedbackToggle = feedbackEl.querySelector(
        '#feedback-toggle-' + idfragment
      )
      var formContainer = document.getElementById(
        'feedback-form-container-' + idfragment
      )

      if (window.localStorage) {
        var textarea = formContainer.querySelector('textarea')
        var key = 'feedback-' + idfragment
        var maxCharsCount = formContainer.querySelector('.max-1000-characters')
        var maxCharsHint = formContainer.querySelector('.max-char-hint')
        var previousText = window.localStorage.getItem(key)

        textarea.value = previousText || ''
        maxCharsCount.textContent = (previousText && previousText.length) || 0

        textarea.oninput = function (e) {
          var feedbackText = e.target.value

          if (feedbackText.length >= 1500) {
            textarea.value = feedbackText.slice(0, 1500)
            maxCharsHint.classList.add('red')
          } else {
            maxCharsHint.classList.remove('red')
          }

          maxCharsCount.textContent = textarea.value.length

          window.setTimeout(function () {
            window.localStorage.setItem(
              'feedback-' + idfragment,
              textarea.value
            )
          }, 0)
        }
      }

      feedbackToggle.onclick = function () {
        if (
          getComputedStyle(formContainer).getPropertyValue('display') == 'none'
        ) {
          formContainer.style = 'display: block'

          if (window.location) {
            var clearedUrl = window.location.href.replace(/#.+/, '')
            window.location.href = clearedUrl + '#' + feedbackElId
          }
        } else {
          formContainer.style = 'display: none'
        }
      }
    })
})()


;(function LikeSubmitModule () {
  var featureContainer = document.getElementById('feature-like-journal')

  if (featureContainer) {
    var likeForm = featureContainer.querySelector('#like-form')
    var submitIcon = likeForm.querySelector('.submit')

    submitIcon.onclick = function () {
      // HTMLFormElement.prototype.requestSubmit helps with applying a form submit event emitter on any element besides button and input
      // It does trigger a submit event (HTMLFormElement.prototype.submit does not)
      likeForm.requestSubmit()
    }

    if (typeof window.fetch === 'function') {
      likeForm.onsubmit = function (e) {
        e.preventDefault()

        submitIcon.onclick = null
        submitIcon.classList.remove('icon-bubble-love-streamline-talk')
        submitIcon.classList.remove('font-big')
        submitIcon.textContent = 'Thanks :)'

        var formData = {
          method: likeForm.method,
          headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
          },
          body: new URLSearchParams(new FormData(likeForm)).toString()
        }
        // send the form
        fetch('/', formData).catch(function () {
          var retries = 0
          var interval = setInterval(function () {
            if (retries === 10) {
              clearInterval(interval)
            } else {
              retries = retries + 1
              fetch('/', formData).then(function () {
                clearInterval(interval)
              })
            }
          }, 20000)
        })
      }
    }
  }
})()





});