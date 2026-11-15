# SandPhoto on Cloudflare Workers

来源：https://github.com/gmajian/sandphoto-js（原 PHP 版 sandphoto 的纯浏览器重写，GPL-3.0）
功能：证件照排版生成器——把证件照拼到一张 6 寸相纸上，拖拽上传、实时预览、下载打印，支持 10 种语言，默认中文。照片全程在浏览器里处理，不上传服务器。

部署方式：Cloudflare Workers 单文件版。`public/` 里的 6 个静态文件（index.html、app.js、sandphoto.js、ui-generator.js、phototypes.js、styles.css，外加 LICENSE）由 `scripts/build-worker.py` 内联进 `src/index.js`，经 custom.cloudflare 连接器 upload-script 部署，无数据库、无构建。

线上地址：https://sandphoto.gentle-bar-7648.workers.dev

改动：改完 `public/` 里的文件后，重新跑 `python3 scripts/build-worker.py` 再重新部署。
