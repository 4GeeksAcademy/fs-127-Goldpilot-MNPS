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

    case 'set_user': {
      localStorage.setItem("token", action.payload.token);
      const savedAvatar = action.payload.user?.id
        ? localStorage.getItem(`avatar_${action.payload.user.id}`)
        : null;
      return {
        ...store,
        user: { ...action.payload.user, avatar: savedAvatar || undefined },
        token: action.payload.token,
      };
    }

    case 'set_user_data': {
      const savedAvatar = action.payload?.id
        ? localStorage.getItem(`avatar_${action.payload.id}`)
        : null;
      return {
        ...store,
        user: { ...action.payload, avatar: savedAvatar || undefined },
      };
    }

    case 'update_user':
      return {
        ...store,
        user: { ...store.user, ...action.payload },
      };

    case 'set_avatar':
      if (store.user?.id) {
        localStorage.setItem(`avatar_${store.user.id}`, action.payload);
      }
      return {
        ...store,
        user: { ...store.user, avatar: action.payload },
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
