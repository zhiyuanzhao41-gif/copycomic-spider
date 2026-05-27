from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def aes_cbc_decrypt(cct: str, content_key: str) -> str:
    """
    AES-CBC 解密函数
    
    参数说明：
    - cct: 密钥字符串
    - content_key: 包含IV和密文的字符串
      * 前16位：IV（偏移量）
      * 第17位到最后：密文（16进制表示）
    
    返回：解密后的明文字符串
    """
    try:
        # ===================== 第一步：处理密钥 =====================

        # 将cct编码为字节，作为AES密钥
        key = cct.encode("utf-8")

        
        # 验证密钥长度（AES要求16、24或32字节）
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"密钥长度{len(key)}不符合AES标准，需要16、24或32字节")

        # ===================== 第二步：提取IV =====================
        
        # 提取IV（前16个字符）
        iv_str = content_key[:16]
        
        iv = iv_str.encode("utf-8")
        
        if len(iv) != 16:
            raise ValueError(f"IV长度{len(iv)}不符合标准（需要16字节）")

        # ===================== 第三步：提取密文（16进制） =====================
        ciphertext_hex = content_key[16:]
        
        # 将16进制字符串转换为字节
        try:
            ciphertext = bytes.fromhex(ciphertext_hex)

        except ValueError as e:
            raise ValueError(f"16进制转换失败: {str(e)}")

        # ===================== 第四步：AES-CBC 解密 =====================

        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_raw = cipher.decrypt(ciphertext)


        # ===================== 第五步：去除 PKCS7 填充 =====================
        try:
            decrypted_bytes = unpad(decrypted_raw, AES.block_size)

        except ValueError as e:
            print(f"[WARNING] PKCS7 去填充失败: {e}")
            print(f"[DEBUG] 尝试直接解码为UTF-8...")
            decrypted_bytes = decrypted_raw
        
        decrypted_str = decrypted_bytes.decode("utf-8", errors="ignore")
        
        return decrypted_str

    except ValueError as e:
        raise ValueError(f"解密参数错误: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"解密失败: {type(e).__name__}: {str(e)}")
