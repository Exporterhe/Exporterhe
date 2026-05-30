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