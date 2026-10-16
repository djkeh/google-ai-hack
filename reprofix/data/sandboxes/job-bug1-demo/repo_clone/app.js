// TaskFlow Pro — Team Sprint Board Application Logic
const state = {
  tasks: [
    { id: 'TASK-101', title: 'Fix OAuth token refresh race condition', points: 8, priority: 'high' },
    { id: 'TASK-102', title: 'Migrate billing webhook to idempotency keys', points: 5, priority: 'medium' },
    { id: 'TASK-103', title: 'Add Playwright regression gate to CI', points: 8, priority: 'high' },
  ],
  nextId: 104,
};

function updateHeaderMetrics() {
  const countEl = document.getElementById('active-count');
  const velocityEl = document.getElementById('velocity-pts');
  const totalPoints = state.tasks.reduce((sum, task) => sum + Number(task.points || 0), 0);
  countEl.textContent = String(state.tasks.length);
  velocityEl.textContent = String(totalPoints);
}

function renderTasks() {
  const listEl = document.getElementById('task-list');
  listEl.innerHTML = '';

  state.tasks.forEach((task) => {
    const card = document.createElement('div');
    card.className = 'task-card';
    card.id = `card-${task.id}`;
    card.setAttribute('data-testid', `card-${task.id}`);

    const priorityClass = task.priority === 'high' ? 'priority-high' : 'priority-medium';
    card.innerHTML = `
      <div class="task-info">
        <div class="task-meta">
          <span class="task-id">${task.id}</span>
          <span class="task-pts">${task.points} pts</span>
          <span class="task-priority ${priorityClass}">${task.priority}</span>
        </div>
        <div class="task-title">${task.title}</div>
      </div>
      <button
        class="btn-delete"
        id="delete-${task.id}"
        data-testid="delete-${task.id}"
        onclick="deleteTask('${task.id}')"
      >Delete Task</button>
    `;
    listEl.appendChild(card);
  });
}

function addTask() {
  const titleInput = document.getElementById('new-task-title');
  const ptsInput = document.getElementById('new-task-pts');
  const title = titleInput.value.trim();
  const points = parseInt(ptsInput.value, 10) || 3;

  if (!title) return;

  const newTask = {
    id: `TASK-${state.nextId++}`,
    title,
    points,
    priority: points >= 8 ? 'high' : 'medium',
  };
  state.tasks.push(newTask);
  titleInput.value = '';
  renderTasks();
  updateHeaderMetrics();
}

// BUG 1 (bug-counter-desync):
// Deleting a task removes its DOM card directly, but forgets to remove the task
// from `state.tasks` and recompute `updateHeaderMetrics()`.
// As a result, #active-count stays at 3 and #velocity-pts stays at 21!
function deleteTask(taskId) {
  state.tasks = state.tasks.filter((t) => t.id !== taskId);
  renderTasks();
  updateHeaderMetrics();
}

// BUG 2 (bug-discount-nan):
// Entering a percentage string like "15%" causes Number("15%") -> NaN,
// rendering "$NaN" in #estimate-total and logging an error banner.
function calculateEstimate() {
  const hours = Number(document.getElementById('est-hours').value);
  const rate = Number(document.getElementById('est-rate').value);
  const rawDiscount = document.getElementById('est-discount').value.trim();

  // Fixed parsing: strip '%' symbol before converting to Number
  const cleanedDiscount = rawDiscount.replace(/%/g, '').trim();
  const discountPct = cleanedDiscount === '' ? 0 : Number(cleanedDiscount);

  const subtotal = hours * rate;
  const finalTotal = subtotal * (1 - discountPct / 100);

  const totalEl = document.getElementById('estimate-total');
  const errorEl = document.getElementById('estimate-error');

  if (Number.isNaN(finalTotal)) {
    totalEl.textContent = '$NaN';
    totalEl.classList.add('is-nan');
    errorEl.textContent = `TypeError: Invalid discount number "${rawDiscount}" -> produced $NaN`;
    errorEl.classList.add('visible');
    console.error(`Uncaught TypeError: Estimate calculation produced NaN for discount="${rawDiscount}"`);
    return;
  }

  totalEl.classList.remove('is-nan');
  errorEl.classList.remove('visible');
  errorEl.textContent = '';
  totalEl.textContent = '$' + finalTotal.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

// Initialize board
renderTasks();
updateHeaderMetrics();
