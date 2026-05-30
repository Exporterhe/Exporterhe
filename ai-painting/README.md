# AI 绘画小程序

抖音 AI 绘画小程序，支持文生图、图生图功能。

## 功能

- 文生图：输入文字描述，AI 为你生成图片
- 图生图：上传参考图，生成新风格图片
- 流量主模式：免费用户观看广告生成
- 会员模式：付费会员无限生成

## 技术栈

- 前端：抖音小程序
- 后端：字节云函数
- AI：Stable Diffusion API / Midjourney API

## 开发

```bash
# 安装云函数依赖
cd cloudfunctions/text2image
npm install

cd ../login
npm install

cd ../membership
npm install

# 部署云函数（使用抖音开发者工具）
```

## 配置

1. 在 `.env` 中配置第三方 API Key
2. 在小程序后台创建广告位，获取广告位 ID
3. 配置云函数环境变量