// это из вебинара

const socket = new WebSocket('ws://127.0.0.1:8000');

socket.onopen = function(e) {
  socket.send(JSON.stringify({
    message: 'Hello from Js client'
  }));
};

socket.onmessage = function(event) {
  try {
    console.log(event);
  } catch (e) {
    console.log('Error:', e.message);
  }
};

// это из E6.6. Асинхронный код — Promises, Async/Await, JSONP
// Создаем promise
const f1 = () => {
    return new Promise((resolve, reject) => {
      resolve("Успешное выполнение promise 1");
    });
  };
  
  const f2 = new Promise((resolve, reject) => {
    resolve("Успешное выполнение promise 2");
  });
  
  // Объявляем асинхронную функцию
  const usePromise = async () => {
    console.log('начало');
    
    // Дожидаемся получения результата от первой функции
    const promiseResult1 = await f1();
    console.log('promiseResult1', promiseResult1);
    
    // Дожидаемся получения результата промиса
    const promiseResult2 = await f2;
    console.log('promiseResult2', promiseResult2)
    
    console.log('конец');
  };
  
  usePromise();




// мой код отсюда

socket.onopen = () => load_users();
function load_users() {
    socket.send(JSON.stringify({'load': 'users'}));
};

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    console.log(data);

    if ('message' in data) {
        document.querySelector('#message').innerText = data.message;
    };
    if ('MessageList' in data) {
        if (userLogged) {
            printChat(data);
        };
    };
    if ('UserList' in data) {
        if (userLogged) {
            viewUserCard(userLogged);
        } else {
            console.log('Пользователь не выбран');
            printUsers(data);
        };
    };
    if ('RoomList' in data) {
        if (userLogged) {
            printRooms(data);
        };
    };
};


// Список пользователей. Сохрани хотя бы логику 
// https://stackoverflow.com/questions/73978053/how-to-add-a-delete-button-for-newly-displayed-objects-in-an-array

function printUsers(data) {
    let list = [];
    for (let key in data) {
        const newString = `<tr><td>${data[key]}</td>
        <td><button onclick='userLogged(${key})'>выбрать</button></td>
        <td><button onclick='deleteUser(${key})'>удалить</button></td>`;
        list = list + newString;
    };
    divSelectUsers.innerHTML = `<table> ${list}</table><br>`;
};

// удаление
function deleteUser(id) {
    socket.send(JSON.stringify({'delete_user': id}));
    console.log({'delete_user': id});
};


function viewUserProfile(userId) {
    fetch(domain + 'users/' + userId +'/')
        .catch(err => console.log(err))
        .then(response => response.json())
        .then(result => printUserProfile(result))
    socket.send(JSON.stringify({'load': 'rooms'}));
};

// Вывод профиля пользователя
function printUserProfile(item) {
    if (item.room == null) {
        room = 'Не выбрана';
    } else {
        let idRoom = item.room[item.room.length-2];
        room = listrooms[idRoom];
    };

    divUser.innerHTML = `
    <div class='div'>
        <img src="${item.avatar}">
        <br>
        <strong>Сменить аватарку:</strong><br>
        <input id='avatar-input' type='file' accept='image/*'><br>
        <button onclick='editAvatar(${item.id})'>Отправить</button>
        <p>ID: ${item.id}</p>
        <p>Имя: ${item.name} <button onclick='changeUserName(${item.id})'>Изменить</button></p>
        <p>Комната в чате: ${room}</p>
        <h4 class='message' id='message'></h4>
    </div>
    `;
};

// Функция загрузки аватарки..........
// туть



function changeUserName(userId) {
    let name = prompt('Введите новое имя');
    socket.send(JSON.stringify({'order': 'changeUserName', 'id': userId, 'name': name }));
    console.log('Отправлен запрос на сервер изменить имя на:', name);
};


// комнаты как пользователи. Но я написала фигни в пользователях()
function printRooms(data) {
    delete data.RoomList;
    let list = [];
    for (let key in data) {
        const newString = `<tr><td><b>${data[key]}</b></td>
        <td><button onclick='deleteRoom(${key})'>Удалить</button></td>
        <td><button onclick='editRoom(${key})'>Изменить</button></td>
        <td><button onclick='selectRoom(${key})'>Подключиться</button></td></tr>`;
        list = list + newString;
    };


function deleteRoom(id) {
    socket.send(JSON.stringify({'delete_room': id}));
    console.log({'delete_room': id});
}


function editRoom(id) {
    let name = prompt('Введите новое имя комнаты');
    socket.send(JSON.stringify({'order': 'changeRoomName', 'id': id, 'name': name }));
    console.log('Отправлен запрос на сервер изменить имя комнаты на:', name);
};


function selectRoom(id) {
    socket.send(JSON.stringify({'load': 'messageList', 'newroom_id': id}));
    console.log({'load': 'messageList', 'newroom_id': id});
    chatSocket.send(JSON.stringify({'roomselect': 'newroom_id', id, 'oldroom_id': currentRoom}));
    currentRoom = id; 
};
