"""
公众号文章下载工具 v2
根据微信文章链接，抓取内容并保存为 Markdown 文件（包含本地图片）
"""

import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Windows 终端编码处理
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class WechatDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_article(self, url):
        """获取文章页面 HTML"""
        print(f"正在获取页面: {url}")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def parse_article(self, html):
        """解析 HTML，提取标题、正文、图片"""
        soup = BeautifulSoup(html, 'html.parser')

        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title')
        if not title_tag:
            title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else 'untitled'

        # 提取正文内容
        content_tag = soup.find('div', id='js_content')
        if not content_tag:
            content_tag = soup.find('div', class_='rich_media_content')

        if not content_tag:
            raise ValueError("无法找到文章内容区域")

        # 提取所有图片 URL
        images = []
        for img in content_tag.find_all('img'):
            data_src = img.get('data-src') or img.get('src')
            if data_src and data_src.startswith('http'):
                images.append(data_src)

        return {
            'title': title,
            'content': content_tag,
            'images': images
        }

    def sanitize_filename(self, filename):
        """清理文件名中的非法字符，包括中文特殊引号"""
        # 替换英文引号和中文引号
        filename = filename.replace('"', '_').replace('"', '_')
        filename = filename.replace(''', '_').replace(''', '_')
        # 替换其他非法字符
        filename = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', filename)
        # 合并多个下划线
        filename = re.sub(r'_+', '_', filename)
        if len(filename) > 200:
            filename = filename[:200]
        return filename.strip('_').strip()

    def download_images(self, image_urls, folder):
        """下载所有图片到本地文件夹"""
        os.makedirs(folder, exist_ok=True)

        downloaded = {}
        for i, url in enumerate(image_urls):
            try:
                print(f"下载图片 {i+1}/{len(image_urls)}...")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                # 根据 Content-Type 判断扩展名
                content_type = response.headers.get('Content-Type', '')
                ext = '.jpg'
                if 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'webp' in content_type:
                    ext = '.webp'

                filename = f"img_{i+1:03d}{ext}"
                filepath = os.path.join(folder, filename)

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                # 记录 URL -> 本地路径 的映射
                downloaded[url] = f"{os.path.basename(folder)}/{filename}"
                print(f"  -> {filename}")
            except Exception as e:
                print(f"  -> 下载失败: {e}")
                downloaded[url] = url  # 失败时保留原 URL

        return downloaded

    def convert_to_markdown(self, content, image_map):
        """将 BeautifulSoup 元素转换为 Markdown"""
        markdown_parts = []

        def process_element(element, depth=0):
            if not element:
                return ""

            result = []

            # 处理字符串节点
            if isinstance(element, str):
                text = str(element).strip()
                if text:
                    return text + " "
                return ""

            # 获取标签名
            tag_name = element.name if hasattr(element, 'name') else None
            if not tag_name:
                # 处理没有名字的元素（如NavigableString）
                return str(element).strip() + " " if str(element).strip() else ""

            # 根据标签类型处理
            if tag_name in ['script', 'style', 'nav']:
                return ""

            elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = tag_name[1]
                text = element.get_text(strip=True)
                if text:
                    result.append(f"{'#' * int(level)} {text}\n")

            elif tag_name == 'p':
                text = ""
                for child in element.children:
                    text += process_element(child, depth)
                text = text.strip()
                if text:
                    result.append(f"{text}\n\n")

            elif tag_name == 'img':
                src = element.get('data-src') or element.get('src', '')
                alt = element.get('alt', '')
                if src in image_map:
                    local_path = image_map[src]
                    result.append(f"![{alt}]({local_path})\n")
                elif src.startswith('http'):
                    result.append(f"![{alt}]({src})\n")

            elif tag_name == 'section':
                # 递归处理 section 内部
                for child in element.children:
                    result.append(process_element(child, depth))

            elif tag_name in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    text = li.get_text(strip=True)
                    prefix = "- " if tag_name == 'ul' else "1. "
                    result.append(f"{prefix}{text}\n")
                result.append("\n")

            elif tag_name == 'blockquote':
                text = element.get_text(strip=True)
                if text:
                    for line in text.split('\n'):
                        result.append(f"> {line}\n")
                    result.append("\n")

            elif tag_name == 'pre':
                code = element.get_text(strip=False)
                result.append(f"```\n{code}\n```\n\n")

            elif tag_name == 'code':
                if element.parent.name != 'pre':
                    text = element.get_text(strip=True)
                    result.append(f"`{text}`")

            elif tag_name in ['strong', 'b']:
                text = element.get_text(strip=True)
                result.append(f"**{text}**")

            elif tag_name in ['em', 'i']:
                text = element.get_text(strip=True)
                result.append(f"*{text}*")

            elif tag_name == 'br':
                result.append("\n")

            elif tag_name == 'a':
                text = element.get_text(strip=True)
                href = element.get('href', '')
                if href and text:
                    result.append(f"[{text}]({href})")
                else:
                    result.append(text)

            elif tag_name == 'span':
                # 递归处理 span 内容
                for child in element.children:
                    result.append(process_element(child, depth))

            elif tag_name in ['div', 'article', 'main']:
                # 递归处理块级容器
                for child in element.children:
                    result.append(process_element(child, depth))

            else:
                # 其他标签，尝试递归处理子元素
                if hasattr(element, 'children'):
                    for child in element.children:
                        result.append(process_element(child, depth))

            return "".join(result)

        # 处理 body 或直接处理内容
        if hasattr(content, 'children'):
            for child in content.children:
                processed = process_element(child)
                if processed.strip():
                    markdown_parts.append(processed)

        # 清理多余的空行
        markdown = "".join(markdown_parts)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        return markdown.strip()

    def save_markdown(self, title, content, image_map, output_path):
        """保存为 Markdown 文件"""
        markdown_content = self.convert_to_markdown(content, image_map)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(markdown_content)
            f.write("\n")

        print(f"已保存 Markdown: {output_path}")

    def download(self, url, output_dir='.'):
        """主流程：下载并保存文章"""
        # 获取页面
        html = self.fetch_article(url)

        # 解析文章
        article = self.parse_article(html)
        original_title = article['title']
        # 生成安全的文件夹名（只保留中文、英文、数字、下划线）
        safe_folder_name = re.sub(r'[^\w\u4e00-\u9fff]+', '_', original_title)
        safe_folder_name = safe_folder_name.strip('_')
        if not safe_folder_name:
            safe_folder_name = 'wechat_article'
        # 限制长度
        if len(safe_folder_name) > 100:
            safe_folder_name = safe_folder_name[:100]

        print(f"\n文章标题: {original_title}")
        print(f"发现 {len(article['images'])} 张图片")

        # 创建图片目录
        images_folder = os.path.join(output_dir, f"{safe_folder_name}_images")

        # 下载图片
        image_map = self.download_images(article['images'], images_folder)

        # 保存 Markdown
        md_path = os.path.join(output_dir, f"{safe_folder_name}.md")
        self.save_markdown(original_title, article['content'], image_map, md_path)

        print(f"\n完成！")
        print(f"  Markdown: {md_path}")
        print(f"  图片目录: {images_folder}")

        return {
            'title': article['title'],
            'md_path': md_path,
            'images_folder': images_folder,
            'images_count': len(image_map)
        }


def main():
    if len(sys.argv) < 2:
        print("用法: python wechat_downloader.py <文章链接> [输出目录]")
        print("示例: python wechat_downloader.py \"https://mp.weixin.qq.com/s/xxxxx\"")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'

    downloader = WechatDownloader()
    try:
        result = downloader.download(url, output_dir)
        print(f"\n成功下载 {result['images_count']} 张图片")
    except Exception as e:
        print(f"下载失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
