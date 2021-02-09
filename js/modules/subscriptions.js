;(function () {
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
    document.querySelector('#user-sub').style = ''
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
