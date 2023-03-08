'use strict';

let chatSocket = new WebSocket(url, `ws://${window.location.host}/connect`);

chatSocket.onopen = (e) => {
    console.log( ...data: `Соединение установлено`);
    btnSendEventListener(e.target);
}

chatSocket.onclose = () => {
    console.log( ...data: `Соединение закрыто`);
}

chatSocket.onerror = (e) => {
    console.log( ...data: `Ошибка соединения ${e}`);
}

chatSocket.onmessage = (e) => {
    console.log( ...data, `Новое сообщение`);
    data = JSON.parse(text, e.data);
    console.log( ...data: data);
}

