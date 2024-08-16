document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');

    async function fetchTasks() {
        const response = await fetch('/tasks/');
        const tasks = await response.json();
        taskList.innerHTML = tasks.map(task => `
            <li>
                <strong>${task.title}</strong>
                <p>${task.description}</p>
                <button onclick="deleteTask('${task._id}')">Delete</button>
            </li>
        `).join('');
    }

    taskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        await fetch('/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, completed: false })
        });
        taskForm.reset();
        fetchTasks();
    });

    async function deleteTask(taskId) {
        await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
        fetchTasks();
    }

    fetchTasks();
});
