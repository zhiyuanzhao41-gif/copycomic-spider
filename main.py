# main.py
import json
import os
from catch import get_cct_and_contentkey
from decryption import aes_cbc_decrypt
from download import download_images

def main():
    print("="*60)
    print("🎯 漫画图片批量下载主程序")
    print("="*60)
    
    # 获取漫画URL
    target_url = input("请输入漫画章节URL：").strip()
    while not target_url:
        print("❌ URL不能为空！")
        target_url = input("请重新输入漫画章节URL：").strip()

    # 提取参数 + 漫画名、章节名
    print("\n" + "-"*60)
    print("🔍 开始提取数据...")
    cct, content_key, comic_title, chapter_name = get_cct_and_contentkey(target_url)
    
    if not cct or not content_key:
        print("❌ 提取失败，程序退出")
        return
    print(f"✅ 漫画名称：{comic_title}")
    print(f"✅ 章节名称：{chapter_name}")

    # 拼接两级文件夹路径
    save_path = os.path.join(comic_title, chapter_name)
    print(f"✅ 保存路径：{save_path}")

    # 解密图片URL
    print("\n" + "-"*60)
    print("🔐 开始解密...")
    try:
        decrypt_raw = aes_cbc_decrypt(cct, content_key)
        image_urls = json.loads(decrypt_raw)
        print(f"✅ 获取到 {len(image_urls)} 张图片")
    except Exception as e:
        print(f"❌ 解密失败：{e}")
        return

    # 下载图片（传入两级路径）
    print("\n" + "-"*60)
    download_images(image_urls, save_path)

    print("\n" + "="*60)
    print("🎉 下载完成！")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 手动终止程序")
    except Exception as e:
        print(f"\n❌ 程序异常：{e}")