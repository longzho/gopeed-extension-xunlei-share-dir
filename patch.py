import json
import os

base = 'up'


def read(path):
    with open(os.path.join(base, path), encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(os.path.join(base, path), 'w', encoding='utf-8') as f:
        f.write(text)


idx = read('index.js')

old1 = """  return {
    shareId: decodeURIComponent(parts[1]),
    passCode: parsed.searchParams.get('pwd') || parsed.searchParams.get('pass_code') || ''
  };"""
new1 = """  return {
    shareId: decodeURIComponent(parts[1]),
    passCode: parsed.searchParams.get('pwd') || parsed.searchParams.get('pass_code') || '',
    path: parsed.searchParams.get('path') || parsed.searchParams.get('parent_path') || ''
  };"""
assert old1 in idx, 'parseShareUrl 未命中'
idx = idx.replace(old1, new1)

old2 = """function normalizePath(path) {
  return String(path || '').replace(/^\\/+|\\/+$/g, '');
}"""
new2 = """function normalizePath(path) {
  return String(path || '').replace(/^\\/+|\\/+$/g, '');
}

function parseSharePath(value) {
  var decoded = String(value || '');
  try {
    decoded = decodeURIComponent(decoded);
  } catch (e) {
    // 解不开就按原串处理
  }
  var segments = decoded.split('/');
  var result = [];
  for (var i = 0; i < segments.length; i += 1) {
    var segment = segments[i].trim();
    if (!segment || segment === '.') {
      continue;
    }
    result.push(segment);
  }
  return result;
}"""
assert old2 in idx, 'normalizePath 未命中'
idx = idx.replace(old2, new2)

old3 = """  async function walk(parentId, path) {
    var items = await listFolder(parentId);

    for (var i = 0; i < items.length; i += 1) {
        var item = items[i];
        var itemId = getItemId(item);
        if (!itemId) {
          continue;
        }
      if (!parentId && !state.rootItemIds[itemId]) {
        state.rootItemIds[itemId] = true;
        state.rootItems.push(item);
      }
      if (isFolder(item)) {
        if (!state.folders[itemId]) {
          state.folders[itemId] = true;
          await walk(itemId, path + getItemName(item) + '/');
        }
      } else {
        if (state.fileItems.length >= MAX_FILES) {
          throw new Error('分享文件数量超过 ' + MAX_FILES + ' 个，已停止解析。');
        }
        state.fileItems.push({ item: item, path: path, parentId: parentId, info: null });
      }
    }
  }

  await walk('', '');
"""
new3 = """  var depthSetting = parseInt(setting('folder_depth', '0'), 10);
  var depthLimit = isNaN(depthSetting) ? 0 : (depthSetting < 0 ? Infinity : depthSetting);
  var explicitRoot = false;

  async function walk(parentId, path, level) {
    var items = await listFolder(parentId);

    for (var i = 0; i < items.length; i += 1) {
        var item = items[i];
        var itemId = getItemId(item);
        if (!itemId) {
          continue;
        }
      if (level === 0 && !explicitRoot && !state.rootItemIds[itemId]) {
        state.rootItemIds[itemId] = true;
        state.rootItems.push(item);
      }
      if (isFolder(item)) {
        if ((depthLimit === Infinity || level + 1 <= depthLimit) && !state.folders[itemId]) {
          state.folders[itemId] = true;
          await walk(itemId, path + getItemName(item) + '/', level + 1);
        }
      } else {
        if (state.fileItems.length >= MAX_FILES) {
          throw new Error('分享文件数量超过 ' + MAX_FILES + ' 个，已停止解析。');
        }
        state.fileItems.push({ item: item, path: path, parentId: parentId, info: null });
      }
    }
  }

  var startParentId = '';
  var startPath = '';
  var startFolder = null;
  var segments = parseSharePath(share.path);
  if (segments.length) {
    var parent = '';
    for (var s = 0; s < segments.length; s += 1) {
      var listing = await listFolder(parent);
      var matched = null;
      for (var m = 0; m < listing.length; m += 1) {
        var candidate = listing[m];
        if (isFolder(candidate) && getItemName(candidate) === segments[s]) {
          matched = candidate;
          break;
        }
      }
      if (!matched) {
        throw new Error('分享里找不到链接指定的目录：「' + segments.slice(0, s + 1).join('/') + '」，可以从上级目录的链接重试。');
      }
      parent = getItemId(matched);
      startFolder = matched;
    }
    startParentId = parent;
    startPath = getItemName(startFolder) + '/';
    explicitRoot = true;
    state.rootItems.push(startFolder);
    state.rootItemIds[getItemId(startFolder)] = true;
  }

  await walk(startParentId, startPath, 0);
"""
assert old3 in idx, 'walk 段未命中'
idx = idx.replace(old3, new3)

old4 = """  var missing = state.fileItems.some(function (entry) {"""
new4 = """  if (!state.fileItems.length) {
    throw new Error('当前目录里没有文件。如果文件在下一层目录里，把扩展设置里的“解析深度”改成 1 或更大，或者打开那个子目录后再复制链接。');
  }

  var missing = state.fileItems.some(function (entry) {"""
assert old4 in idx, 'missing 段未命中'
idx = idx.replace(old4, new4, 1)

write('index.js', idx)

manifest = json.loads(read('manifest.json'))
manifest['description'] = '解析迅雷云盘分享链接。默认只读取链接指向的那个目录，可调整解析深度。'
manifest['author'] = 'longzho'
manifest['name'] = 'xunlei-pan-share-dir'
manifest['version'] = '0.8.5'
manifest['homepage'] = 'https://github.com/longzho/gopeed-extension-xunlei-share-dir'
manifest['repository'] = {
    'url': 'https://github.com/longzho/gopeed-extension-xunlei-share-dir',
    'directory': ''
}
if not any(s.get('name') == 'folder_depth' for s in manifest['settings']):
    manifest['settings'].insert(2, {
        'name': 'folder_depth',
        'title': '解析深度',
        'description': '从链接指向的目录开始，往下再解析几层。0 = 只解析当前目录；负数 = 不限深度，文件多时容易超时。',
        'type': 'number',
        'value': '0'
    })
with open(os.path.join(base, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

readme = read('README.md')
readme = readme.replace(
    '无论链接是否带 `path`，扩展都会从分享根目录开始递归读取全部内容。',
    '链接里的 `path` 现在会被真正使用。扩展先逐级比对目录名，找到那个目录，再只列它的内容。\n默认「解析深度」为 0，也就是只读当前目录这一层，不往下钻。')
readme = readme.replace(
    '- 带目录路径的分享：`https://pan.xunlei.com/s/分享ID?pwd=提取码&path=/目录`',
    '- 带目录路径的分享：`https://pan.xunlei.com/s/分享ID?pwd=提取码&path=/目录`\n  在浏览器里进入某个子目录后，地址栏里就带着这个 `path`，整条复制即可')
write('README.md', readme)
print('patched ok')
