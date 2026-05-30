App({
  onLaunch() {
    // 检查登录态
    this.checkLoginStatus();
  },
  globalData: {
    userInfo: null,
    isMember: false,
    memberExpireTime: null,
    remainCount: 0
  },
  checkLoginStatus() {
    const token = tt.getStorageSync('token');
    if (token) {
      // 验证 token 有效性
      this.validateToken(token);
    }
  },
  validateToken(token) {
    // 验证 token 有效性，如果无效则清除
    tt.cloud.callFunction({
      name: 'login',
      data: { token: token },
      success: (res) => {
        if (res.data && res.data.openid) {
          this.globalData.userInfo = res.data;
          this.globalData.isMember = res.data.isMember;
          this.globalData.memberExpireTime = res.data.memberExpireTime;
        } else {
          // token 无效，清除
          tt.removeStorageSync('token');
        }
      },
      fail: () => {
        // 验证失败，清除 token
        tt.removeStorageSync('token');
      }
    });
  }
});