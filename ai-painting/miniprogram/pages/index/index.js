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