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