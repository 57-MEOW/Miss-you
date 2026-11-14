// 离线缓存：第一次打开时把所有文件存进手机，之后断网也能用。
// 版本号由 build.py 自动更新，不用手动改。
const VERSION = "mailbox-20261111-175705";
const FILES = ["./", "./index.html", "./letters.enc.json", "./manifest.webmanifest", "./icon-180.png", "./icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// 先用缓存，没有再去网上拿（在国内永远走缓存）
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
