console.log("漫画下载助手脚本已注入！");

// 创建下载按钮和提示框
function createDownloadButton() {
  console.log("尝试创建下载按钮...");
  
  // 避免重复创建
  if (document.getElementById('manga-download-btn')) {
    console.log("按钮已存在，跳过创建");
    return;
  }

  // 创建按钮
  const btn = document.createElement('button');
  btn.id = 'manga-download-btn';
  btn.innerHTML = '📥';
  document.body.appendChild(btn);
  console.log("按钮元素已创建并添加到body");

  // 创建提示框
  const tip = document.createElement('div');
  tip.id = 'manga-download-tip';
  document.body.appendChild(tip);

  // 按钮点击事件
  btn.addEventListener('click', async () => {
    const currentUrl = window.location.href;
    const tipEl = document.getElementById('manga-download-tip');

    try {
      // 显示加载提示
      tipEl.textContent = '正在发送下载请求...';
      tipEl.style.display = 'block';
      tipEl.style.background = '#f3f4f6';
      tipEl.style.color = '#374151';

      // 发送URL到本地Python服务
      const response = await fetch('http://localhost:5000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: currentUrl })
      });

      const result = await response.json();
      if (result.code === 200) {
        tipEl.textContent = '✅ 下载请求已接收！';
        tipEl.style.background = '#dcfce7';
        tipEl.style.color = '#166534';
      } else {
        tipEl.textContent = `❌ ${result.msg}`;
        tipEl.style.background = '#fee2e2';
        tipEl.style.color = '#991b1b';
      }
    } catch (error) {
      tipEl.textContent = '❌ 连接Python服务失败，请检查程序是否运行！';
      tipEl.style.background = '#fee2e2';
      tipEl.style.color = '#991b1b';
      console.error('发送请求失败：', error);
    } finally {
      // 3秒后隐藏提示
      setTimeout(() => {
        tipEl.style.display = 'none';
      }, 3000);
    }
  });
}

// 多种触发方式，确保按钮一定会创建
if (document.readyState === 'loading') {
  // 页面还在加载，监听DOMContentLoaded
  document.addEventListener('DOMContentLoaded', createDownloadButton);
} else {
  // 页面已经加载完成，直接执行
  createDownloadButton();
}

// 额外监听load事件，防止特殊情况
window.addEventListener('load', () => {
  setTimeout(createDownloadButton, 100);
});