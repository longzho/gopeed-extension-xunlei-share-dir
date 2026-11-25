import io
import json

p = 'up/manifest.json'
m = json.load(io.open(p, encoding='utf-8'))
m['homepage'] = 'https://github.com/longzho/gopeed-extension-xunlei-share-dir'
m['repository'] = {'url': m['homepage'], 'directory': ''}
io.open(p, 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=2))
print('manifest fixed')
