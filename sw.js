// 5度圏ルーレット — オフライン用サービスワーカー
// アプリを更新したら CACHE の版数を上げること（古いキャッシュは activate で消える）
const CACHE = "cof-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-512-maskable.png",
  "./apple-touch-icon.png",
  "./favicon-64.png"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// 静的アプリなのでキャッシュ優先。無ければネットワークへ、失敗したらトップを返す。
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    caches.match(req).then(hit =>
      hit || fetch(req).catch(() => caches.match("./index.html"))
    )
  );
});
