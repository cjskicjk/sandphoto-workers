import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
OUT = os.path.join(ROOT, 'src', 'index.js')

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    'LICENSE': 'text/plain; charset=utf-8',
}

assets = {}
for name in sorted(os.listdir(PUBLIC)):
    path = os.path.join(PUBLIC, name)
    if not os.path.isfile(path):
        continue
    with open(path, 'rb') as f:
        content = f.read().decode('utf-8')
    ext = os.path.splitext(name)[1]
    mime = MIME.get(name) or MIME.get(ext, 'application/octet-stream')
    assets['/' + name] = {'type': mime, 'body': content}

header = """// SandPhoto (sandphoto-js) served as a single Cloudflare Worker.
// All files are static and inlined from public/ by scripts/build-worker.py.
// No server-side processing: the app runs entirely in the browser (Canvas API).
const ASSETS = """
body = json.dumps(assets, ensure_ascii=False)
handler = """;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    let path = url.pathname;
    if (path === '/') path = '/index.html';
    const asset = ASSETS[path];
    if (!asset) {
      return new Response('Not found', { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }
    const headers = { 'Content-Type': asset.type };
    if (path !== '/index.html') headers['Cache-Control'] = 'public, max-age=86400';
    return new Response(asset.body, { headers });
  },
};
"""
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(header + body + handler)
print('wrote', OUT, len(header) + len(body) + len(handler), 'bytes,', len(assets), 'assets')
