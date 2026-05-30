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
    // TODO: 后续实现会员页面后再启用
    tt.showToast({ title: '会员功能即将上线', icon: 'none' });
  },
  viewHistory() {
    // TODO: 后续实现历史记录页面后再启用
    tt.showToast({ title: '历史记录即将上线', icon: 'none' });
  },
  contactService() {
    tt.makePhoneCall({
      phoneNumber: '400-xxx-xxxx'
    });
  }
});