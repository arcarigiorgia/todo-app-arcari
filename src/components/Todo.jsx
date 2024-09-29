import React, { useEffect, useRef, useState } from 'react';
import todo_icon from '../assets/todo_icon2.png';
import Todoitems from './Todoitems';

const Todo = () => {
    const [todoList, setTodoList] = useState([]);
    const inputRef = useRef();

    // Function to fetch tasks from the API
    const fetchTasks = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8080/getTasks');
            const data = await response.json();
            setTodoList(data);
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    };

    // Add a new task using POST request
    const add = async () => {
        const inputText = inputRef.current.value.trim();

        if (inputText === "") {
            return null;
        }

        const newTodo = {
            text: inputText,
            isComplete: false,
        };

        try {
            const response = await fetch('http://127.0.0.1:8080/createTask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newTodo),
            });

            const result = await response.json();
            setTodoList((prev) => [...prev, result.task]);
        } catch (error) {
            console.error("Error creating task:", error);
        }

        inputRef.current.value = "";
    };

    // Delete a task using DELETE request
    const deleteTodo = async (id) => {
        try {
            await fetch(`http://127.0.0.1:8080/deleteTask/${id}`, {
                method: 'DELETE',
            });
            setTodoList((prev) => prev.filter((todo) => todo.id !== id));
        } catch (error) {
            console.error("Error deleting task:", error);
        }
    };

    // Toggle task completion using a PUT request
    const toggle = async (id) => {
        const updatedTodo = todoList.find(todo => todo.id === id);
        updatedTodo.isComplete = !updatedTodo.isComplete;

        try {
            // Assuming to add an update endpoint in backend
            await fetch(`http://127.0.0.1:8080/updateTask/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedTodo),
            });

            setTodoList((prev) =>
                prev.map((todo) => (todo.id === id ? updatedTodo : todo))
            );
        } catch (error) {
            console.error("Error updating task:", error);
        }
    };

    // Fetch tasks on component mount
    useEffect(() => {
        fetchTasks();
    }, []);

    return (
        <div className='bg-white place-self-center w-11/12 max-w-md flex flex-col p-7 min-h-[550px] rounded-xl'>
            <div className='flex items-center mt-7 gap-2'>
                <img className='w-8' src={todo_icon} alt="" />
                <h1 className='text-3xl font-extrabold'>My ToDo List</h1>
            </div>
            <div className='flex items-center my-7 bg-gray-200 rounded-full'>
                <input ref={inputRef} className='bg-transparent border-0 outline-none flex-1 h-14 pl-6 pr-2 placeholder:text-violet-700' type="text" placeholder='Add your tasks' />
                <button onClick={add} className='border-none rounded-3xl bg-violet-500 w-32 h-14 text-white text-lg front-medium cursor-pointer'> + </button>
            </div>
            <div>
                {todoList.map((item, index) => (
                    <Todoitems key={index} text={item.text} id={item.id} isComplete={item.isComplete} deleteTodo={deleteTodo} toggle={toggle} />
                ))}
            </div>
        </div>
    );
};

export default Todo;
