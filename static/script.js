// 动图列表
const gifList = [
    '/static/heart-dog.gif',
    '/static/couple-dance.gif', 
    '/static/ezgif-47812851c06b81.gif',
    '/static/20220302224226_e3e67.gif'
];

// 随机选择动图
function getRandomGif() {
    return gifList[Math.floor(Math.random() * gifList.length)];
}

// 应用随机动图到所有动图元素
function applyRandomGifs() {
    // 为每个动图元素独立随机选择动图
    const gifElements = document.querySelectorAll('.dog-gif, .dog-gif-small, .heart-gif, .heart-gif-large');
    gifElements.forEach(element => {
        element.style.backgroundImage = `url('${getRandomGif()}')`;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // 首先应用随机动图
    applyRandomGifs();
    
    const contentEl = document.getElementById('content');
    const saveBtn = document.getElementById('save-btn');
    const notesList = document.getElementById('notes-list');
    
    // 加载最近的笔记（只显示最新的3篇）
    fetch('/api/notes')
        .then(res => res.json())
        .then(notes => {
            // 只显示最新的3篇日记
            const recentNotes = notes.slice(-3).reverse();
            
            if (recentNotes.length === 0) {
                notesList.innerHTML = '<div style="text-align: center;"><div class="dog-gif" style="margin: 0 auto 10px;"></div><p style="color: #ff8fa3; font-style: italic;"><div class="heart-gif"></div> 我们的爱情日记还在等待第一个故事呢！小君宝宝，快来和小黑一起开始记录吧～</p></div>';
                // 应用随机动图到新创建的元素
                applyRandomGifs();
                return;
            }
            
            recentNotes.forEach(note => {
                const noteEl = document.createElement('div');
                noteEl.className = 'note';
                noteEl.innerHTML = `
                    <small><div class="heart-gif"></div> ${new Date(note.created_at).toLocaleString()}</small>
                    <p>${note.content.length > 80 ? note.content.substring(0, 80) + '... <div class="heart-gif"></div> 点击查看我们完整的甜蜜回忆～' : note.content}</p>
                `;
                notesList.appendChild(noteEl);
            });
            // 应用随机动图到新创建的日记元素
            applyRandomGifs();
        });
    
    // 保存笔记
    saveBtn.addEventListener('click', () => {
        const content = contentEl.value;
        if (!content.trim()) return;
        
        fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        })
        .then(res => res.json())
        .then(() => {
            contentEl.value = '';
            // 显示成功提示
            const successMsg = document.createElement('div');
            successMsg.innerHTML = '<div class="heart-gif"></div> 又一个珍贵的回忆被小黑悄悄收藏了～';
            successMsg.style.cssText = 'position: fixed; top: 20px; right: 20px; background: linear-gradient(45deg, #ff8fa3, #ffb6c1); color: white; padding: 12px 20px; border-radius: 25px; z-index: 1000; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 143, 163, 0.4);';
            document.body.appendChild(successMsg);
            // 应用随机动图到成功提示
            const heartGif = successMsg.querySelector('.heart-gif');
            if (heartGif) {
                heartGif.style.backgroundImage = `url('${getRandomGif()}')`;
            }
            setTimeout(() => {
                document.body.removeChild(successMsg);
                location.reload(); // 刷新加载新内容
            }, 2000);
        });
    });
});