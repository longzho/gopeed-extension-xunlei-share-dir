import io

p = 'patch.py'
s = io.open(p, encoding='utf-8').read()
s = s.replace("manifest['version'] = '0.8.5'", "manifest['author'] = 'longzho'" + chr(10) + "manifest['name'] = 'xunlei-pan-share-dir'" + chr(10) + "manifest['version'] = '0.8.5'")
s = s.replace("'https://github.com/longzho/gopeed-extension-xunlei'", "'https://github.com/longzho/gopeed-extension-xunlei-share-dir'")
s = s.replace("'https://github.com/longzho/gopeed-extension-xunlei',", "'https://github.com/longzho/gopeed-extension-xunlei-share-dir',")
io.open(p, 'w', encoding='utf-8').write(s)

p = 'README.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace("注意：本仓库的扩展标识和官方版相同（`cybdarlnig-png@xunlei-pan`），会覆盖安装！", "本仓库是独立的扩展，标识为 `longzho@xunlei-pan-share-dir`，和市场上的官方版（`cybdarlnig-png@xunlei-pan`）不是同一条，两个可以同时装，各自开关、各自保存自己的设置。" + chr(10) + chr(10) + "代码和原版同源，署名与授权说明见 `NOTICE.md`。")
io.open(p, 'w', encoding='utf-8').write(s)

p = 'NOTICE.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace("- 取用版本：0.8.4", "- 取用版本：0.8.4" + chr(10) + "- 本仓库维护者：longzho")
section = "## 关于扩展标识" + chr(10) + chr(10) + "`manifest.json` 里的 `author` 字段写成 `longzho`，`name` 改为 `xunlei-pan-share-dir`。这样扩展标识是 `longzho@xunlei-pan-share-dir`，与官方版的 `cybdarlnig-png@xunlei-pan` 分开，两个版本可以同时安装、各自开关。" + chr(10) + chr(10) + "`author` 在这里只是 Gopeed 用来区分扩展的技术标识，不改变代码的著作权归属。原作者署名保留在本文件与 README 中。" + chr(10) + chr(10) + "## 修改内容"
s = s.replace("## 修改内容", section)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok')
