import os
import requests
import time
from tqdm import tqdm  

def download_images(image_urls, save_path):
    # 自动创建两级文件夹（不存在则创建，存在不报错）
    os.makedirs(save_path, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0'
    }

    # 初始化进度条，总长度=图片数量
    pbar = tqdm(total=len(image_urls), desc="📥 漫画下载中", unit="张", colour="green")
    fail_count = 0  # 统计失败数量

    # 批量下载
    for index, img_info in enumerate(image_urls, 1):
        img_url = img_info.get("url")
        if not img_url:
            pbar.set_postfix_str("URL为空，跳过")
            pbar.update(1)
            fail_count += 1
            continue

        try:
            # 下载图片
            img_response = requests.get(img_url, headers=headers, timeout=15)
            img_response.raise_for_status()

            # 保存文件（001.jpg 格式）
            img_name = f"{index:03d}.jpg"
            img_path = os.path.join(save_path, img_name)

            with open(img_path, "wb") as f:
                f.write(img_response.content)

            # 更新进度条（无额外打印，保持整洁）
            pbar.update(1)
            time.sleep(0.2)  # 防封延迟

        except Exception as e:
            # 仅记录失败，不打断进度条
            pbar.set_postfix_str(f"第{index}张下载失败")
            pbar.update(1)
            fail_count += 1

    # 关闭进度条
    pbar.close()

    # 最终统计提示
    success_num = len(image_urls) - fail_count
    print(f"\n📊 下载完成 | 成功：{success_num} 张 | 失败：{fail_count} 张")
    print(f"📂 保存路径：{os.path.abspath(save_path)}")