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