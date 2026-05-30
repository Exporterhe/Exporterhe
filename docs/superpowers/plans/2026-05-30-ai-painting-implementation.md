# AI 绘画小程序实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 上线 MVP - 抖音 AI 绘画小程序，包含文生图（SD）、广告变现、抖音登录、会员体系

**Architecture:** 抖音小程序前端 + 字节云函数后端 + 第三方 SD API，流量主+会员混合变现

**Tech Stack:** 抖音小程序（原生）、Python 云函数、云开发数据库、第三方 SD API（如 SoulGen/Cartina）

---

## 项目结构

```
ai-painting/
├── miniprogram/                    # 抖音小程序前端
│   ├── pages/
│   │   ├── index/                  # 首页
│   │   ├── text2image/             # 文生图页
│   │   ├── my/                     # 我的页面
│   │   └── components/             # 公共组件
│   ├── app.js
│   ├── app.json
│   └── app.ttss
├── cloudfunctions/                 # 云函数
│   ├── text2image/                 # 文生图云函数
│   ├── login/                     # 登录云函数
│   └── membership/                 # 会员云函数
└── README.md
```

---

## Task 1: 抖音小程序初始化

**Files:**
- Create: `miniprogram/app.js`
- Create: `miniprogram/app.json`
- Create: `miniprogram/app.ttss`
- Create: `miniprogram/pages/index/index.js`
- Create: `miniprogram/pages/index/index.json`
- Create: `miniprogram/pages/index/index.ttss`
- Create: `miniprogram/pages/index/index.ttml`

- [ ] **Step 1: 创建项目目录结构**

```bash
mkdir -p ai-painting/miniprogram/pages/index
mkdir -p ai-painting/miniprogram/pages/text2image
mkdir -p ai-painting/miniprogram/pages/my
mkdir -p ai-painting/miniprogram/components
mkdir -p ai-painting/cloudfunctions
```

- [ ] **Step 2: 创建 app.json 页面配置**

```json
{
  "pages": [
    "pages/index/index",
    "pages/text2image/index",
    "pages/my/index"
  ],
  "window": {
    "navigationBarTitleText": "AI 绘画",
    "navigationBarBackgroundColor": "#FFFFFF",
    "navigationBarTextStyle": "black"
  },
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#FF6B9D",
    "backgroundColor": "#FFFFFF",
    "borderStyle": "white",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "assets/home.png",
        "selectedIconPath": "assets/home-active.png"
      },
      {
        "pagePath": "pages/my/index",
        "text": "我的",
        "iconPath": "assets/my.png",
        "selectedIconPath": "assets/my-active.png"
      }
    ]
  },
  "style": "v2",
  "lazyCodeLoading": "requiredComponents"
}
```

- [ ] **Step 3: 创建 app.js 主入口**

```javascript
App({
  onLaunch() {
    // 检查登录态
    this.checkLoginStatus();
  },
  globalData: {
    userInfo: null,
    isMember: false,
    memberExpireTime: null
  },
  checkLoginStatus() {
    const token = tt.getStorageSync('token');
    if (token) {
      // 验证 token 有效性
      this.validateToken(token);
    }
  },
  validateToken(token) {
    // 调用云函数验证
  }
});
```

- [ ] **Step 4: 创建首页 index.ttml**

```html
<view class="container">
  <view class="header">
    <image class="logo" src="/assets/logo.png" />
    <text class="title">AI 绘画</text>
  </view>

  <view class="feature-cards">
    <view class="card" bindtap="goToText2Image">
      <image class="card-icon" src="/assets/text2image.png" />
      <text class="card-title">文生图</text>
      <text class="card-desc">输入文字，AI 为你生成图片</text>
    </view>
  </view>

  <view class="tips">
    <text class="tip-text">免费用户每次生成需观看广告</text>
    <text class="tip-text">开通会员享无限生成</text>
  </view>
</view>
```

- [ ] **Step 5: 创建首页样式 index.ttss**

```css
.container {
  min-height: 100vh;
  background: linear-gradient(180deg, #FFF5F8 0%, #FFFFFF 100%);
  padding: 32rpx;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48rpx 0;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  border-radius: 32rpx;
  margin-bottom: 24rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333333;
}

.feature-cards {
  margin-top: 48rpx;
}

.card {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 48rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(255, 107, 157, 0.1);
}

.card-icon {
  width: 120rpx;
  height: 120rpx;
  margin-bottom: 24rpx;
}

.card-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 12rpx;
}

.card-desc {
  font-size: 28rpx;
  color: #999999;
}

.tips {
  margin-top: 64rpx;
  text-align: center;
}

.tip-text {
  font-size: 24rpx;
  color: #FF6B9D;
  display: block;
  margin-bottom: 12rpx;
}
```

- [ ] **Step 6: 创建首页逻辑 index.js**

```javascript
const app = getApp();

Page({
  data: {
    userInfo: null
  },
  onLoad() {
    this.setData({
      userInfo: app.globalData.userInfo
    });
  },
  goToText2Image() {
    tt.navigateTo({
      url: '/pages/text2image/index'
    });
  },
  goToMy() {
    tt.switchTab({
      url: '/pages/my/index'
    });
  }
});
```

- [ ] **Step 7: Commit**

```bash
cd ai-painting
git init
git add miniprogram/
git commit -m "feat(miniprogram): 初始化抖音小程序项目结构"
```

---

## Task 2: 文生图页面

**Files:**
- Create: `miniprogram/pages/text2image/index.ttml`
- Create: `miniprogram/pages/text2image/index.js`
- Create: `miniprogram/pages/text2image/index.ttss`
- Create: `miniprogram/pages/text2image/index.json`

- [ ] **Step 1: 创建文生图页面结构 text2image.ttml**

```html
<view class="container">
  <view class="prompt-section">
    <textarea
      class="prompt-input"
      placeholder="描述你想要的图片，如：一只可爱的粉色小猫"
      maxlength="500"
      bindinput="onPromptInput"
    />
    <text class="char-count">{{prompt.length}}/500</text>
  </view>

  <view class="style-section">
    <text class="section-title">选择风格</text>
    <view class="style-list">
      <view
        class="style-item {{currentStyle === item.id ? 'active' : ''}}"
        wx:for="{{styles}}"
        wx:key="id"
        bindtap="selectStyle"
        data-id="{{item.id}}"
      >
        <image class="style-img" src="{{item.preview}}" />
        <text class="style-name">{{item.name}}</text>
      </view>
    </view>
  </view>

  <view class="generate-btn" bindtap="onGenerate">
    <text class="btn-text">生成图片</text>
  </view>

  <view class="result-section" wx:if="{{resultImage}}">
    <image class="result-img" src="{{resultImage}}" mode="aspectFit" />
    <view class="result-actions">
      <view class="action-btn" bindtap="saveImage">
        <text>保存图片</text>
      </view>
      <view class="action-btn primary" bindtap="shareImage">
        <text>分享</text>
      </view>
    </view>
  </view>

  <view class="loading-mask" wx:if="{{isGenerating}}">
    <view class="loading-content">
      <view class="loading-icon"></view>
      <text class="loading-text">AI 创作中...</text>
    </view>
  </view>
</view>
```

- [ ] **Step 2: 创建样式 text2image.ttss**

```css
.container {
  min-height: 100vh;
  background: linear-gradient(180deg, #FFF5F8 0%, #FFFFFF 100%);
  padding: 32rpx;
}

.prompt-section {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  position: relative;
}

.prompt-input {
  width: 100%;
  height: 200rpx;
  font-size: 28rpx;
  color: #333333;
  line-height: 1.6;
}

.char-count {
  position: absolute;
  right: 32rpx;
  bottom: 16rpx;
  font-size: 24rpx;
  color: #CCCCCC;
}

.style-section {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 24rpx;
}

.style-list {
  display: flex;
  flex-wrap: wrap;
  gap: 24rpx;
}

.style-item {
  width: 140rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16rpx;
  border-radius: 16rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
}

.style-item.active {
  border-color: #FF6B9D;
  background: #FFF5F8;
}

.style-img {
  width: 100rpx;
  height: 100rpx;
  border-radius: 12rpx;
  margin-bottom: 12rpx;
}

.style-name {
  font-size: 22rpx;
  color: #666666;
}

.generate-btn {
  background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%);
  border-radius: 48rpx;
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 32rpx;
}

.btn-text {
  color: #FFFFFF;
  font-size: 32rpx;
  font-weight: bold;
}

.result-section {
  margin-top: 48rpx;
}

.result-img {
  width: 100%;
  border-radius: 24rpx;
  background: #F5F5F5;
}

.result-actions {
  display: flex;
  gap: 24rpx;
  margin-top: 24rpx;
}

.action-btn {
  flex: 1;
  height: 80rpx;
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #FFFFFF;
  border: 2rpx solid #FF6B9D;
}

.action-btn text {
  font-size: 28rpx;
  color: #FF6B9D;
}

.action-btn.primary {
  background: #FF6B9D;
}

.action-btn.primary text {
  color: #FFFFFF;
}

.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.loading-content {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 48rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-icon {
  width: 80rpx;
  height: 80rpx;
  border: 4rpx solid #F5F5F5;
  border-top-color: #FF6B9D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 24rpx;
  font-size: 28rpx;
  color: #333333;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

- [ ] **Step 3: 创建逻辑 text2image.js**

```javascript
const app = getApp();

Page({
  data: {
    prompt: '',
    currentStyle: 'anime',
    styles: [
      { id: 'anime', name: '动漫风', preview: '/assets/styles/anime.png' },
      { id: 'realistic', name: '写实风', preview: '/assets/styles/realistic.png' },
      { id: 'cartoon', name: '卡通风', preview: '/assets/styles/cartoon.png' },
      { id: 'watercolor', name: '水彩风', preview: '/assets/styles/watercolor.png' },
      { id: 'oil', name: '油画风', preview: '/assets/styles/oil.png' }
    ],
    resultImage: '',
    isGenerating: false
  },
  onPromptInput(e) {
    this.setData({
      prompt: e.detail.value
    });
  },
  selectStyle(e) {
    const styleId = e.currentTarget.dataset.id;
    this.setData({
      currentStyle: styleId
    });
  },
  async onGenerate() {
    const { prompt, currentStyle } = this.data;

    if (!prompt.trim()) {
      tt.showToast({ title: '请输入描述文字', icon: 'none' });
      return;
    }

    // 检查登录态
    if (!app.globalData.userInfo) {
      await this.doLogin();
    }

    // 检查会员或观看广告
    const canGenerate = await this.checkGeneratePermission();
    if (!canGenerate) return;

    this.setData({ isGenerating: true });

    try {
      const result = await this.callText2ImageAPI(prompt, currentStyle);
      this.setData({
        resultImage: result.imageUrl,
        isGenerating: false
      });
    } catch (err) {
      this.setData({ isGenerating: false });
      tt.showToast({ title: '生成失败，请重试', icon: 'none' });
    }
  },
  checkGeneratePermission() {
    return new Promise((resolve) => {
      if (app.globalData.isMember) {
        resolve(true);
      } else {
        // 显示广告
        this.showAd(() => resolve(true));
      }
    });
  },
  showAd(callback) {
    const adUnitId = 'your_ad_unit_id'; // 替换为实际广告位 ID
    tt.createRewardedVideoAd({
      adUnitId
    }).then(ad => {
      ad.onClose(() => callback());
      ad.onError(() => {
        tt.showToast({ title: '广告加载失败', icon: 'none' });
        resolve(false);
      });
      ad.load().then(() => ad.show());
    });
  },
  async doLogin() {
    return new Promise((resolve) => {
      tt.login({
        provider: 'toutiao',
        success(res) {
          // 调用云函数登录
          tt.cloud.callFunction({
            name: 'login',
            data: { code: res.code },
            success(result) {
              if (result.data.openid) {
                app.globalData.userInfo = result.data;
                app.globalData.isMember = result.data.isMember;
                resolve(result.data);
              }
            }
          });
        }
      });
    });
  },
  callText2ImageAPI(prompt, style) {
    return tt.cloud.callFunction({
      name: 'text2image',
      data: { prompt, style }
    });
  },
  saveImage() {
    tt.saveImageToPhotosAlbum({
      filePath: this.data.resultImage,
      success() {
        tt.showToast({ title: '保存成功', icon: 'success' });
      },
      fail() {
        tt.showToast({ title: '保存失败', icon: 'none' });
      }
    });
  },
  shareImage() {
    tt.showShareMenu({
      withShareTicket: true
    });
  }
});
```

- [ ] **Step 4: Commit**

```bash
git add miniprogram/pages/text2image/
git commit -m "feat(miniprogram): 添加文生图页面"
```

---

## Task 3: 云函数 - 登录

**Files:**
- Create: `cloudfunctions/login/index.js`
- Create: `cloudfunctions/login/package.json`

- [ ] **Step 1: 创建登录云函数 index.js**

```javascript
const cloud = require('tt-cloud-sdk'); // 字节云开发 SDK

exports.main = async (event, context) => {
  const { code } = event;

  // 通过 code 获取 openid（示例，实际需根据字节云开发文档调整）
  const res = await cloud.request({
    url: 'https://open.toutiao.com/api/v2/oauth/code2session',
    method: 'POST',
    data: {
      appid: process.env.APPID,
      code,
      grant_type: 'authorization_code'
    }
  });

  const { openid } = res.data;

  // 查询用户是否已存在
  const db = cloud.database();
  const users = db.collection('users');

  let user = await users.where({ openid }).get();

  if (user.data.length === 0) {
    // 新用户创建
    await users.add({
      data: {
        openid,
        createTime: Date.now(),
        isMember: false,
        memberExpireTime: null,
        generateCount: 0,
        adFreeCount: 0
      }
    });
    user = await users.where({ openid }).get();
  }

  return {
    openid,
    isMember: user.data[0].isMember,
    memberExpireTime: user.data[0].memberExpireTime,
    generateCount: user.data[0].generateCount
  };
};
```

- [ ] **Step 2: 创建 package.json**

```json
{
  "name": "login",
  "version": "1.0.0",
  "dependencies": {
    "tt-cloud-sdk": "^1.0.0"
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add cloudfunctions/login/
git commit -m "feat(cloud): 添加登录云函数"
```

---

## Task 4: 云函数 - 文生图

**Files:**
- Create: `cloudfunctions/text2image/index.js`
- Create: `cloudfunctions/text2image/package.json`
- Modify: `cloudfunctions/text2image/.env` (添加 API Key)

- [ ] **Step 1: 创建文生图云函数 index.js**

```javascript
const cloud = require('tt-cloud-sdk');

// 第三方 SD API 配置（示例使用 SoulGen）
const SD_API_URL = 'https://api.soulgen.ai/v1/text2image';
const SD_API_KEY = process.env.SD_API_KEY;

exports.main = async (event, context) => {
  const { prompt, style } = event;

  // 参数校验
  if (!prompt || prompt.trim().length === 0) {
    return { error: 'prompt 不能为空' };
  }

  // 调用第三方 SD API
  try {
    const response = await cloud.request({
      url: SD_API_URL,
      method: 'POST',
      header: {
        'Authorization': `Bearer ${SD_API_KEY}`,
        'Content-Type': 'application/json'
      },
      data: {
        prompt,
        style,
        width: 1024,
        height: 1024,
        num_images: 1
      }
    });

    if (response.status !== 200) {
      throw new Error(`API 请求失败: ${response.status}`);
    }

    // 假设返回格式 { image_url: "https://..." }
    return {
      imageUrl: response.data.image_url,
      imageId: response.data.id
    };
  } catch (err) {
    console.error('SD API Error:', err);
    return { error: '图片生成失败，请重试' };
  }
};
```

- [ ] **Step 2: 创建 .env.example**

```env
# 第三方 SD API Key
SD_API_KEY=your_sd_api_key_here

# MJ API Key（后续扩展用）
MJ_API_KEY=your_mj_api_key_here
```

- [ ] **Step 3: Commit**

```bash
git add cloudfunctions/text2image/
git commit -m "feat(cloud): 添加文生图云函数"
```

---

## Task 5: "我的"页面

**Files:**
- Create: `miniprogram/pages/my/index.ttml`
- Create: `miniprogram/pages/my/index.js`
- Create: `miniprogram/pages/my/index.ttss`

- [ ] **Step 1: 创建"我的"页面结构 my.ttml**

```html
<view class="container">
  <view class="user-card">
    <view class="avatar-section">
      <image class="avatar" src="{{userInfo.avatar || '/assets/default-avatar.png'}}" />
      <view class="user-info">
        <text class="nickname">{{userInfo.nickname || '游客'}}</text>
        <text class="member-tag" wx:if="{{isMember}}">会员</text>
        <text class="member-tag normal" wx:else>普通用户</text>
      </view>
    </view>
  </view>

  <view class="member-banner" wx:if="{{!isMember}}" bindtap="openMember">
    <view class="banner-content">
      <text class="banner-title">开通会员</text>
      <text class="banner-desc">广告免费 · 无限生成 · MJ 高质量</text>
    </view>
    <text class="banner-btn">立即开通</text>
  </view>

  <view class="member-info" wx:else>
    <view class="member-item">
      <text class="item-label">会员到期时间</text>
      <text class="item-value">{{memberExpireTime}}</text>
    </view>
    <view class="member-item">
      <text class="item-label">剩余生成次数</text>
      <text class="item-value">{{remainCount}}</text>
    </view>
  </view>

  <view class="menu-list">
    <view class="menu-item" bindtap="viewHistory">
      <text class="menu-text">生成记录</text>
      <text class="menu-arrow">></text>
    </view>
    <view class="menu-item" bindtap="openMember">
      <text class="menu-text">会员中心</text>
      <text class="menu-arrow">></text>
    </view>
    <view class="menu-item" bindtap="contactService">
      <text class="menu-text">联系客服</text>
      <text class="menu-arrow">></text>
    </view>
  </view>
</view>
```

- [ ] **Step 2: 创建样式 my.ttss**

```css
.container {
  min-height: 100vh;
  background: #F5F5F5;
}

.user-card {
  background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%);
  padding: 48rpx 32rpx;
}

.avatar-section {
  display: flex;
  align-items: center;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.5);
}

.user-info {
  margin-left: 24rpx;
}

.nickname {
  font-size: 36rpx;
  font-weight: bold;
  color: #FFFFFF;
  display: block;
}

.member-tag {
  font-size: 22rpx;
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.3);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  margin-top: 8rpx;
  display: inline-block;
}

.member-tag.normal {
  background: rgba(0, 0, 0, 0.2);
}

.member-banner {
  background: #FFFFFF;
  margin: 24rpx;
  border-radius: 16rpx;
  padding: 32rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.banner-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  display: block;
}

.banner-desc {
  font-size: 24rpx;
  color: #999999;
  margin-top: 8rpx;
  display: block;
}

.banner-btn {
  background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%);
  color: #FFFFFF;
  padding: 16rpx 32rpx;
  border-radius: 32rpx;
  font-size: 26rpx;
}

.member-info {
  background: #FFFFFF;
  margin: 24rpx;
  border-radius: 16rpx;
  padding: 32rpx;
}

.member-item {
  display: flex;
  justify-content: space-between;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #F5F5F5;
}

.member-item:last-child {
  border-bottom: none;
}

.item-label {
  font-size: 28rpx;
  color: #666666;
}

.item-value {
  font-size: 28rpx;
  color: #333333;
}

.menu-list {
  background: #FFFFFF;
  margin: 24rpx;
  border-radius: 16rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1rpx solid #F5F5F5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-text {
  font-size: 28rpx;
  color: #333333;
}

.menu-arrow {
  font-size: 28rpx;
  color: #CCCCCC;
}
```

- [ ] **Step 3: 创建逻辑 my.js**

```javascript
const app = getApp();

Page({
  data: {
    userInfo: null,
    isMember: false,
    memberExpireTime: '',
    remainCount: 0
  },
  onLoad() {
    this.loadUserInfo();
  },
  onShow() {
    this.loadUserInfo();
  },
  loadUserInfo() {
    const userInfo = app.globalData.userInfo;
    this.setData({
      userInfo,
      isMember: app.globalData.isMember,
      memberExpireTime: app.globalData.memberExpireTime || '未开通',
      remainCount: app.globalData.remainCount || 0
    });
  },
  openMember() {
    // 跳转会员开通页（需根据实际页面路径调整）
    tt.navigateTo({
      url: '/pages/member/index'
    });
  },
  viewHistory() {
    tt.navigateTo({
      url: '/pages/history/index'
    });
  },
  contactService() {
    tt.makePhoneCall({
      phoneNumber: '400-xxx-xxxx'
    });
  }
});
```

- [ ] **Step 4: Commit**

```bash
git add miniprogram/pages/my/
git commit -m "feat(miniprogram): 添加我的页面"
```

---

## Task 6: 会员云函数

**Files:**
- Create: `cloudfunctions/membership/index.js`
- Create: `cloudfunctions/membership/package.json`

- [ ] **Step 1: 创建会员云函数 index.js**

```javascript
const cloud = require('tt-cloud-sdk');

const db = cloud.database();
const users = db.collection('users');

// 会员套餐配置
const MEMBERSHIP_PLANS = {
  monthly: {
    name: '月卡',
    price: 29.9,
    duration: 30, // 天
    generateLimit: 500
  },
  yearly: {
    name: '年卡',
    price: 199,
    duration: 365,
    generateLimit: 99999
  }
};

exports.main = async (event, context) => {
  const { action, openid, planType } = event;

  switch (action) {
    case 'getMembership':
      return await getMembership(openid);

    case 'subscribe':
      return await subscribeMembership(openid, planType);

    case 'checkPermission':
      return await checkGeneratePermission(openid);

    case 'deductCount':
      return await deductGenerateCount(openid);

    default:
      return { error: '未知操作' };
  }
};

async function getMembership(openid) {
  const result = await users.where({ openid }).get();

  if (result.data.length === 0) {
    return { isMember: false };
  }

  const user = result.data[0];
  const now = Date.now();

  // 检查会员是否到期
  if (user.isMember && user.memberExpireTime > now) {
    return {
      isMember: true,
      memberExpireTime: new Date(user.memberExpireTime).toLocaleDateString(),
      remainCount: user.generateCount
    };
  }

  // 会员已到期
  if (user.isMember && user.memberExpireTime <= now) {
    await users.doc(user._id).update({
      data: {
        isMember: false,
        generateCount: 0
      }
    });
  }

  return {
    isMember: false,
    memberExpireTime: null,
    remainCount: 0
  };
}

async function subscribeMembership(openid, planType) {
  const plan = MEMBERSHIP_PLANS[planType];
  if (!plan) {
    return { error: '无效的套餐类型' };
  }

  // 这里应该调用支付接口（字节小程序支付）
  // 示例省略支付流程，直接模拟开通
  const now = Date.now();
  const expireTime = now + plan.duration * 24 * 60 * 60 * 1000;

  await users.where({ openid }).update({
    data: {
      isMember: true,
      memberExpireTime: expireTime,
      generateCount: plan.generateLimit,
      memberPlan: planType
    }
  });

  return {
    success: true,
    memberExpireTime: new Date(expireTime).toLocaleDateString()
  };
}

async function checkGeneratePermission(openid) {
  const result = await users.where({ openid }).get();

  if (result.data.length === 0) {
    return { canGenerate: false, reason: '用户不存在' };
  }

  const user = result.data[0];

  // 会员且有额度
  if (user.isMember && user.memberExpireTime > Date.now() && user.generateCount > 0) {
    return { canGenerate: true };
  }

  // 非会员需要看广告
  return { canGenerate: true, needAd: true };
}

async function deductGenerateCount(openid) {
  const result = await users.where({ openid }).get();

  if (result.data.length === 0) {
    return { error: '用户不存在' };
  }

  const user = result.data[0];

  if (user.generateCount > 0) {
    await users.doc(user._id).update({
      data: {
        generateCount: user.generateCount - 1
      }
    });
  }

  return { success: true, remainCount: user.generateCount - 1 };
}
```

- [ ] **Step 2: Commit**

```bash
git add cloudfunctions/membership/
git commit -m "feat(cloud): 添加会员云函数"
```

---

## Task 7: 广告接入

**Files:**
- Modify: `miniprogram/pages/text2image/index.js` (showAd 方法)

- [ ] **Step 1: 更新广告逻辑**

```javascript
// 在 text2image/index.js 中更新 showAd 方法
showAd(callback) {
  // 激励视频广告
  const rewardedVideoAd = tt.createRewardedVideoAd({
    adUnitId: 'your_rewarded_video_ad_unit_id'
  });

  rewardedVideoAd.onClose((res) => {
    if (res.isEnded) {
      // 用户完整观看广告
      callback(true);
    } else {
      tt.showToast({ title: '请完整观看广告', icon: 'none' });
    }
  });

  rewardedVideoAd.onError(() => {
    tt.showToast({ title: '广告加载失败', icon: 'none' });
  });

  rewardedVideoAd.load()
    .then(() => rewardedVideoAd.show())
    .catch(err => {
      console.error('Ad load error:', err);
      tt.showToast({ title: '广告加载失败', icon: 'none' });
    });
}
```

- [ ] **Step 2: 添加插屏广告（可选）**

```javascript
// 在页面切换时显示插屏广告
showInterstitialAd() {
  const interstitialAd = tt.createInterstitialAd({
    adUnitId: 'your_interstitial_ad_unit_id'
  });

  interstitialAd.load()
    .then(() => interstitialAd.show())
    .catch(err => console.error('Interstitial ad error:', err));
}
```

- [ ] **Step 3: Commit**

```bash
git add miniprogram/pages/text2image/index.js
git commit -m "feat(miniprogram): 接入激励视频广告"
```

---

## Task 8: 项目配置与部署

**Files:**
- Create: `ai-painting/project.config.json` (小程序项目配置)
- Create: `ai-painting/.gitignore`
- Create: `ai-painting/README.md`

- [ ] **Step 1: 创建 project.config.json**

```json
{
  "miniprogramRoot": "miniprogram/",
  "cloudfunctionRoot": "cloudfunctions/",
  "projectname": "ai-painting",
  "appid": "your_appid_here"
}
```

- [ ] **Step 2: 创建 .gitignore**

```
node_modules/
.cloudfunctions/
.env
*.log
.DS_Store
```

- [ ] **Step 3: 创建 README.md**

```markdown
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
```

- [ ] **Step 4: Commit**

```bash
git add project.config.json .gitignore README.md
git commit -m "docs: 添加项目配置和 README"
```

---

## 自检清单

- [ ] 规格覆盖：所有设计文档中的功能都有对应实现任务
- [ ] 无占位符：代码中无 TBD/TODO/待实现等占位符
- [ ] 类型一致性：函数名、变量名在所有任务中保持一致
- [ ] 依赖关系：Task 3(登录) → Task 4(图生图) → Task 5(我的页) → Task 6(会员)
- [ ] 广告接入：已在 Task 2 和 Task 7 中覆盖
- [ ] 云函数：3 个云函数（login/text2image/membership）都有完整代码