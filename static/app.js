const list = document.getElementById("todo-list");
const form = document.getElementById("add-form");
const newTitle = document.getElementById("new-title");
const errorBox = document.getElementById("error");
const summary = document.getElementById("summary");

async function api(path, options = {}) {
  const response = await fetch(`/api/todos${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = !message;
}

async function run(action) {
  try {
    showError("");
    await action();
    await refresh();
  } catch (error) {
    showError(`${error.message}. Is the server running?`);
  }
}

function startEditing(todo, titleSpan) {
  const input = document.createElement("input");
  input.type = "text";
  input.className = "title-input";
  input.value = todo.title;
  input.maxLength = 200;
  titleSpan.replaceWith(input);
  input.focus();

  let finished = false;
  const finish = (save) => {
    if (finished) return;
    finished = true;
    const title = input.value.trim();
    if (save && title && title !== todo.title) {
      run(() => api(`/${todo.id}`, { method: "PATCH", body: JSON.stringify({ title }) }));
    } else {
      input.replaceWith(titleSpan);
    }
  };

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") finish(true);
    if (event.key === "Escape") finish(false);
  });
  input.addEventListener("blur", () => finish(true));
}

function render(todos) {
  list.replaceChildren();
  for (const todo of todos) {
    const item = document.createElement("li");
    item.classList.toggle("done", todo.done);

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = todo.done;
    checkbox.addEventListener("change", () =>
      run(() => api(`/${todo.id}`, { method: "PATCH", body: JSON.stringify({ done: checkbox.checked }) }))
    );

    const title = document.createElement("span");
    title.className = "title";
    title.textContent = todo.title;
    title.title = "Double-click to rename";
    title.addEventListener("dblclick", () => startEditing(todo, title));

    const remove = document.createElement("button");
    remove.className = "delete";
    remove.textContent = "Delete";
    remove.addEventListener("click", () => run(() => api(`/${todo.id}`, { method: "DELETE" })));

    item.append(checkbox, title, remove);
    list.append(item);
  }

  const remaining = todos.filter((todo) => !todo.done).length;
  summary.textContent = todos.length ? `${remaining} of ${todos.length} left to do` : "Nothing to do yet.";
}

async function refresh() {
  render(await api(""));
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = newTitle.value.trim();
  if (!title) return;
  run(async () => {
    await api("", { method: "POST", body: JSON.stringify({ title }) });
    newTitle.value = "";
  });
});

run(async () => {});
