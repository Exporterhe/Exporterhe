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