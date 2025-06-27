document.addEventListener('DOMContentLoaded', () => {
    const contentEl = document.getElementById('content');
    const saveBtn = document.getElementById('save-btn');
    const notesList = document.getElementById('notes-list');
    
    // 加载已有笔记
    fetch('/api/notes')
        .then(res => res.json())
        .then(notes => {
            notes.forEach(note => {
                const noteEl = document.createElement('div');
                noteEl.className = 'note';
                noteEl.innerHTML = `
                    <small>${new Date(note.created_at).toLocaleString()}</small>
                    <p>${note.content.substring(0, 100)}...</p>
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