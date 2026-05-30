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
      const result = await this.callText2imageAPI(prompt, currentStyle);
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
  },
  showInterstitialAd() {
    const interstitialAd = tt.createInterstitialAd({
      adUnitId: 'your_interstitial_ad_unit_id'
    });

    interstitialAd.load()
      .then(() => interstitialAd.show())
      .catch(err => console.error('Interstitial ad error:', err));
  },
  async doLogin() {
    return new Promise((resolve) => {
      tt.login({
        provider: 'toutiao',
        success(res) {
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
  callText2imageAPI(prompt, style) {
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