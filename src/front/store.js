export const initialStore=()=>{
  return{
    message: null,
    todos: [
      {
        id: 1,
        title: "Make the bed",
        background: null,
      },
      {
        id: 2,
        title: "Do my homework",
        background: null,
      }
    ],
    user: null,
    token: localStorage.getItem("token") || null,
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };

    case 'add_task':

      const { id,  color } = action.payload

      return {
        ...store,
        todos: store.todos.map((todo) => (todo.id === id ? { ...todo, background: color } : todo))
      };

    case 'set_user':
      localStorage.setItem("token", action.payload.token);
      return {
        ...store,
        user: action.payload.user,
        token: action.payload.token,
      };

    case 'logout':
      localStorage.removeItem("token");
      return {
        ...store,
        user: null,
        token: null,
      };

    default:
      throw Error('Unknown action.');
  }
}
