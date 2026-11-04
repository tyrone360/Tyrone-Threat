const CACHE_NAME = "tyrone-threat-v1";

const STATIC_FILES = [
    "/static/css/style.css",
    "/static/js/script.js",
    "/static/icons/icon-192.png",
    "/static/icons/icon-512.png"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_FILES))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", event => {
    const request = event.request;

    if (request.method !== "GET") return;

    const url = new URL(request.url);

    if (url.origin !== self.location.origin) return;

    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request).then(response => {
                if (response.ok && url.pathname === "/") {
                    const copy = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put("/", copy));
                }
                return response;
            }).catch(() => caches.match("/"))
        );
        return;
    }

    if (url.pathname.startsWith("/api/")) return;

    event.respondWith(
        caches.match(request).then(cached => {
            if (cached) return cached;

            return fetch(request).then(response => {
                if (response.ok) {
                    const copy = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put(request, copy));
                }
                return response;
            });
        })
    );
});
