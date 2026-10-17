// Harir Store — Service Worker v1
const CACHE = 'harir-v1';
const STATIC = [
  '/',
  '/manifest.json',
  '/icon-192.png',
  '/og-image.png',
  'https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Tajawal:wght@400;500;700&family=Inter:wght@400;500;600;700;900&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Only handle GET requests
  if(e.request.method !== 'GET') return;

  const url = new URL(e.request.url);

  // Network-first for Supabase API calls (always fresh data)
  if(url.hostname.includes('supabase.co')){
    e.respondWith(
      fetch(e.request).catch(() => new Response('{}', {headers:{'Content-Type':'application/json'}}))
    );
    return;
  }

  // Cache-first for fonts and static assets
  if(url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com'){
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }))
    );
    return;
  }

  // Network-first for HTML (always fresh)
  if(e.request.destination === 'document'){
    e.respondWith(
      fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-first for everything else
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
