# NOTICE

本仓库是 https://github.com/cybdarlnig-png/gopeed-extension-xunlei 的 fork，并在其上做了修改。

- 上游作者：cybdarlnig-png
- 取用版本：0.8.4
- 本仓库维护者：longzho
- fork 关系：GitHub 页面上的 "forked from cybdarlnig-png/gopeed-extension-xunlei" 即可溯源

## 关于扩展标识

`manifest.json` 里的 `author` 字段写成 `longzho`，`name` 改为 `xunlei-pan-share-dir`。这样扩展标识是 `longzho@xunlei-pan-share-dir`，与官方版的 `cybdarlnig-png@xunlei-pan` 分开，两个版本可以同时安装、各自开关。

`author` 在这里只是 Gopeed 用来区分扩展的技术标识，不改变代码的著作权归属。原作者署名保留在本文件与 README 中。

## 修改内容

1. `parseShareUrl` 保留链接里的 `path` 参数。
2. 新增 `parseSharePath`，把 `path` 拆成目录名数组。
3. 遍历改为先按目录名逐级下潜到链接指定的目录，再从那里列出内容。
4. 新增设置项 `folder_depth`，默认 0，只列当前目录这一层。
5. 当前目录没有文件时给出明确提示。

其余逻辑、接口地址、请求头均与上游一致。

## 授权状态

上游仓库没有 LICENSE，也没有授权声明。版权归作者所有。本仓库不声明自己的许可证，仅作个人学习与自用性质的技术验证。如果作者提出异议，应当删除或改为直接使用官方版本。
