document.addEventListener('DOMContentLoaded', () => {
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
                notesList.innerHTML = '<p style="color: #666; font-style: italic;">还没有写过日记，开始写第一篇吧！</p>';
                return;
            }
            
            recentNotes.forEach(note => {
                const noteEl = document.createElement('div');
                noteEl.className = 'note';
                noteEl.innerHTML = `
                    <small>📅 ${new Date(note.created_at).toLocaleString()}</small>
                    <p>${note.content.length > 80 ? note.content.substring(0, 80) + '...' : note.content}</p>
                `;
                notesList.appendChild(noteEl);
            });
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
            location.reload(); // 简单刷新加载新内容
        });
    });
});