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