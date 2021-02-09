self.addEventListener('notificationclick', function (event) {
  event.notification.close()
  event.waitUntil(clients.openWindow(event.notification.data.url))
})

self.addEventListener('push', function (event) {
  if (event.data) {
    event.waitUntil(showNotification(event.data.json()))
  }
})

function showNotification (d) {
  return self.registration.showNotification(d.title, {
    icon: '/img/notification.png',
    body: d.body,
    data: {
      url: d.url
    }
  })
}
