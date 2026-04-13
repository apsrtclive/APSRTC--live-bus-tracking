// ═══════════════════════════════════════════════════════
// APSRTC Live — Service Worker (PWA Offline Support)
// ═══════════════════════════════════════════════════════

const CACHE_NAME = 'apsrtc-live-v12'; // v12: Network-First for HTML
const STATIC_ASSETS = [
    '/',
    '/static/style.css',
    '/static/leaflet.css',
    '/static/leaflet.js',
    '/static/js/translations.js',
    '/static/favicon.ico',
    '/static/manifest.json',
    '/offline'
];

// Install — cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker v12...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Caching static assets');
            return cache.addAll(STATIC_ASSETS).catch(err => {
                console.warn('[SW] Some assets failed to cache:', err);
            });
        })
    );
    self.skipWaiting();
});

// Activate — clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker v12...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.filter(name => name !== CACHE_NAME).map(name => {
                    console.log('[SW] Deleting old cache:', name);
                    return caches.delete(name);
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch — Smart caching strategy
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Skip non-GET requests
    if (event.request.method !== 'GET') return;

    // 1. API calls — Network first, fallback to cache
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    if (response.status === 200) {
                        const clone = response.clone();
                        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                    }
                    return response;
                })
                .catch(() => caches.match(event.request).then(cached => {
                    return cached || new Response(JSON.stringify({ error: 'Offline' }), {
                        headers: { 'Content-Type': 'application/json' }
                    });
                }))
        );
        return;
    }

    // 2. Navigation / HTML pages — Network First
    // Ensures users always see latest design while online.
    if (event.request.mode === 'navigate' || event.request.headers.get('accept')?.includes('text/html')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    if (response.status === 200) {
                        const clone = response.clone();
                        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                    }
                    return response;
                })
                .catch(() => caches.match(event.request).then(cached => {
                    // Fallback to offline page if fully offline
                    return cached || caches.match('/offline');
                }))
        );
        return;
    }

    // 3. Static assets — Stale-While-Revalidate
    // Fastest load using cache, update in background.
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            const fetchPromise = fetch(event.request).then(networkResponse => {
                if (networkResponse.status === 200) {
                    const clone = networkResponse.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return networkResponse;
            }).catch(() => null);

            return cachedResponse || fetchPromise;
        })
    );
});
