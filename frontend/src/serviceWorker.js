// This file provides optional code for registering a service worker.
// By default, the service worker is not registered.


const isRunningOnLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
    // IPv6 localhost address [::1].
    window.location.hostname === '[::1]' ||
    // Consider 127.0.0.1/8 range as localhost for IPv4.
    window.location.hostname.match(
      /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
    )
);

export function registerServiceWorker(config) {
  if (process.env.NODE_ENV === 'production' && 'serviceWorker' in navigator) {
    // URL constructor is supported in all browsers that handle service workers.
    const publicUrl = new URL(process.env.PUBLIC_URL, window.location.href);
    if (publicUrl.origin !== window.location.origin) {
      // Service worker won't work if PUBLIC_URL is hosted on a different origin.
      // This might occur if assets are being served from a CDN.
      return;
    }

    window.addEventListener('load', () => {
      const serviceWorkerUrl = `${process.env.PUBLIC_URL}/service-worker.js`;

      if (isRunningOnLocalhost) {
        // Running on localhost, check if service worker exists.
        verifyServiceWorker(serviceWorkerUrl, config);

        // Additional logging for developers running on localhost.
        navigator.serviceWorker.ready.then(() => {
          console.log(
            'This app is using a service worker to cache resources and serve them ' +
              'in a cache-first manner. Learn more at https://bit.ly/CRA-PWA'
          );
        });
      } else {
        // Not running on localhost, simply register the service worker.
        registerActiveServiceWorker(serviceWorkerUrl, config);
      }
    });
  }
}

function registerActiveServiceWorker(serviceWorkerUrl, config) {
  navigator.serviceWorker
    .register(serviceWorkerUrl)
    .then(registration => {
      registration.onupdatefound = () => {
        const newWorker = registration.installing;
        if (newWorker == null) {
          return;
        }
        newWorker.onstatechange = () => {
          if (newWorker.state === 'installed') {
            if (navigator.serviceWorker.controller) {
              // New content is available, but the old content will still be served
              // until all tabs of this page are closed.
              console.log(
                'New content is available; it will be used once all ' +
                  'tabs of this page are closed. See https://bit.ly/CRA-PWA for more info.'
              );

              // Trigger onUpdate callback if it exists
              if (config && config.onUpdate) {
                config.onUpdate(registration);
              }
            } else {
              // Everything has been cached for offline use.
              console.log('Content is now available offline.');

              // Trigger onSuccess callback if it exists
              if (config && config.onSuccess) {
                config.onSuccess(registration);
              }
            }
          }
        };
      };
    })
    .catch(error => {
      console.error('Service worker registration failed:', error);
    });
}

function verifyServiceWorker(serviceWorkerUrl, config) {
  // Check if the service worker file can be found. Reload the page if  not found.
  fetch(serviceWorkerUrl)
    .then(response => {
      const contentType = response.headers.get('content-type');
      if (
        response.status === 404 ||
        (contentType != null && contentType.indexOf('javascript') === -1)
      ) {
        // No service worker found. Likely a different app. Reload the page.
        navigator.serviceWorker.ready.then(registration => {
          registration.unregister().then(() => {
            window.location.reload();
          });
        });
      } else {
        // Service worker is available and valid. Proceed with registration.
        registerActiveServiceWorker(serviceWorkerUrl, config);
      }
    })
    .catch(() => {
      console.log('No internet connection found. The app is running in offline mode.');
    });
}

export function unregisterServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then(registration => {
      registration.unregister();
    });
  }
}
