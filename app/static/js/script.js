const ToDos = {

    loadingElement: document.getElementById('loading'),
    sectionContainer: document.getElementById('section-container'),
    errorElement: document.getElementById('error'),
    todoList: document.getElementById('todo-list'),

    async init() {
        try {
            const todos = await this.fetchTodos2();
            this.fillTodosList(todos);
        } catch (e) {
            this.showError(e.message);
            return;
        }
    },

    setLoading(loading) {
        this.loadingElement.style.display = loading ? '' : 'none';
    },

    showError(error) {
        this.errorElement.textContent = error;
        this.errorElement.style.display = '';
    },

    async fetchTodos() {
        this.setLoading(true);
        const todosResponse = await fetch(`${window.origin}/getTodos`);
        this.setLoading(false);
        if (!todosResponse.ok) {
            throw new Error('Не удалось получить задачи... ');
        }
        const todos = await todosResponse.json();
        return todos;
    },

    async fetchTodos2() {
        this.setLoading(true);
        const todosResponse = await fetch('https://jsonplaceholder.typicode.com/todos');
        this.setLoading(false);
        if (!todosResponse.ok) {
            throw new Error('Не удалось получить комментарии... ');
        }
        const todos = await todosResponse.json();
        return todos;
    },

    async fillTodosList(todos) {
        for (const todo of todos) {
            const todoItem = document.querySelector(`li[data-id="${todo.id}"]`);
            let todo_status = 0;
            if(todoItem)
            {
                const todos = await this.fetchTodos();
                for (let i = 0; i < todos.length; i++) {
                    if(todos[i].id === todo.id) {
                        todo_status = todos[i].done;
                        break;
                    }
                }
                const headerBlock = document.getElementById('header-block'+todo.id);
                const checkboxDiv = document.createElement('div');
                checkboxDiv.classList.add("checkbox-done");
                checkboxDiv.classList.add("float-right");
                checkboxDiv.classList.add("custom-control");
                checkboxDiv.classList.add("custom-checkbox");
                checkboxDiv.classList.add("form-control-lg");
                const chk = document.createElement('input');
                chk.setAttribute('type',"checkbox");
                chk.setAttribute('name',"todoDone")
                chk.classList.add("custom-control-input");
                chk.setAttribute('id',"customCheck"+todo.id)
                const chkLabel = document.createElement('label');
                chkLabel.htmlFor = "customCheck"+todo.id;
                if(todo_status === 0)
                {
                    chk.checked = false;
                    chkLabel.innerText='Невыполнено';
                }
                else {
                    chkLabel.innerText='Выполнено';
                    chk.checked = true;
                    todoItem.classList.add("done-todo");
                    headerBlock.classList.add("done-todo");
                }
                chk.addEventListener('change', async () => {
                    let currentCheckboxStatus = chk.checked
                    if (!confirm('Вы уверены, что хотите поменять статус этого задания?')) {
                        if (currentCheckboxStatus)
                            chk.checked = false
                        else
                            chk.checked = true
                        return;
                    }
                    let entry = {};

                    if(chk.checked)
                    {
                        todoItem.classList.add("done-todo");
                        headerBlock.classList.add("done-todo");
                        chkLabel.innerText='Выполнено';
                        entry = {
                            todo_id: todo.id,
                            done: "done"
                        }
                    }
                    else {
                        chkLabel.innerText='Неыполнено';
                        todoItem.classList.remove("done-todo");
                        headerBlock.classList.remove("done-todo");
                        entry = {
                            todo_id: todo.id,
                            done: "undone"
                        }
                    }
                    await fetch(`${window.origin}`, {
                            method: "PATCH",
                            credentials: "include",
                            body: JSON.stringify(entry),
                            cache: "no-cache",
                            headers: new Headers({
                                "content-type": "application/json"
                            })
                        });
                });
                checkboxDiv.appendChild(chk);
                checkboxDiv.appendChild(chkLabel);
                todoItem.appendChild(checkboxDiv);
                todoItem.appendChild(document.createElement('hr'));
                const titleEl = document.createElement('div');
                const header2 = document.createElement('h2');
                const comment = document.createElement('div');
                header2.textContent = "Комментарий к задаче:";
                titleEl.appendChild(header2);
                comment.textContent = todo.title;
                titleEl.appendChild(comment);
                titleEl.classList.add('collapse');
                titleEl.setAttribute('id', "demo"+todo.id);
                todoItem.appendChild(titleEl);
                todoItem.appendChild(document.createElement('br'));
                const button = document.createElement('button');
                button.classList.add('btn');
                button.classList.add('btn-danger');
                button.classList.add('btn-sm');
                button.classList.add('float-right');
                button.classList.add('ml-auto');
                button.textContent = 'Удалить';
                button.addEventListener('click', () => { this.removeTodo(todo.id) });
                todoItem.appendChild(button);
                this.todoList.appendChild(todoItem);
                const button_edit = document.createElement('button');
                button_edit.classList.add('btn');
                button_edit.classList.add('float-left');
                button_edit.classList.add('btn-primary');
                button_edit.classList.add('btn-sm');
                button_edit.textContent = 'Редактировать';
                button_edit.addEventListener('click', (ev) => { this.editTodoWindow(ev, todo.id) });
                button_edit.setAttribute('data-toggle', "modal")

                todoItem.appendChild(button_edit);
                this.todoList.appendChild(todoItem);
            }
        }
    },

    async removeTodo(id) {
        if (!confirm('Вы уверены, что хотите удалить это задание?')) {
            return;
        }

        try {
            this.setLoading(true);
            const res = await fetch('https://jsonplaceholder.typicode.com/todos/${id}', { method: 'delete' });
            this.setLoading(false);
            if (!res.ok) {
                throw new Error("Не удалось удалить запись...");
            }

            const entry = {
                todo_id: id
            };

            await fetch(`${window.origin}`, {
                method: "DELETE",
                credentials: "include",
                body: JSON.stringify(entry),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json"
                })
            });
            document.querySelector(`li[data-id="${id}"]`).remove();
        } catch (error) {
            this.showError(error.message);
        }
    },

    async editTodoWindow(ev, id){
        ev.preventDefault();
        this.setLoading(true);
        const todoResponse = await fetch(`${window.origin}/getTodoData/${id}`);
        this.setLoading(false);
        if (!todoResponse.ok) {
            throw new Error('Не удалось получить данные задачи... ');
        }
        const todo_data = await todoResponse.json();
        var newModal = `
  <div class="modal fade" id="edit-todo-window${id}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="title-modal${id}">Редактировать задачу</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
      <label>Название задачи:</label>
        <input id='edit-title${id}'>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
        <button type="button" class="btn btn-primary" id='save-todo-edit${id}'>Сохранить изменения</button>
      </div>
    </div>
  </div>
</div>
  `;
  $('body').append(newModal);
  $('#edit-todo-window'+id).modal('show');
  $('#edit-title'+id).val(todo_data['name']);
  $('#save-todo-edit'+id).on('click', async (e) => {
            e.preventDefault();
            let new_name=$('#edit-title'+id).val()
            if (new_name==todo_data['name']) {$('#edit-todo-window'+id).modal('hide'); return}
            else{
            const entry = {
                        todo_id: id,
                        name: new_name
                    };

            await fetch(`${window.origin}`, {
                method: "PATCH",
                credentials: "include",
                body: JSON.stringify(entry),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json"
                })
            });
            $('#edit-todo-window'+id).modal('hide');
            $('[data-target="#demo'+id+'"]')[0].innerText=new_name;//this.init();
    }});
    }
}

ToDos.init();

