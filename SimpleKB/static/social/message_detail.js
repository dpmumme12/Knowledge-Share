const request_user = {"id": JSON.parse(get("#request_user_id").textContent),
                      "username": JSON.parse(get("#request_username").textContent),
                      "profile_img": JSON.parse(get("#request_user_img").textContent)
                    }
const chat_user = {"id": JSON.parse(get("#chat_user_id").textContent),
                   "username": JSON.parse(get("#chat_username").textContent),
                   "profile_img": JSON.parse(get("#chat_user_img").textContent)
                  }
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const messagesDiv = get(".messages");
const loader = get(".loader");
var pagination_page = 1;
const hideLoader = () => {
  loader.classList.remove('show-loader');
};

const showLoader = () => {
  loader.classList.add('show-loader');
};

get("#refresh-button").addEventListener("click", refresh_messages)

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  fetch('/api/messages', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      "sender": request_user.id,
      "recipient": chat_user.id,
      "content": msgText
      }),
    mode: "same-origin",
  })
  .then(async (response) => {
    const data = await response.json();
    return {
      data: data,
      status_code: response.status,
    };
  })
  .then((resp) => {
    if(resp.status_code === 201) {
      appendMessage(request_user.username, request_user.profile_img,
                    "right", resp.data.content, new Date(resp.data.message_sent_date),
                    "beforeend");
      msgerChat.scrollTop += 500000;
    }
  })
});


async function get_messages(page) {
    let response = await fetch(`/api/messages?page=${page}&username=${chat_user.username}`)

    if(!response.ok) {
      error_message(`An error ocurred gathering messages: ${response.status}`);
    }
    
    return await response.json();
}


function appendMessage(name, img, side, text, date, append) {
  const msgHTML = `
    <div class="msg ${side}-msg">
    <img src="${img}" class="msg-img"/>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(date)}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  messagesDiv.insertAdjacentHTML(append, msgHTML);
}


async function load_messages() {
  showLoader();
  var messages = await get_messages(pagination_page);
  var scroll = 0;
  
  messages.results.forEach(message => {
    if(message.sender === request_user.id) {
      appendMessage(request_user.username, request_user.profile_img,
                    "right", message.content, new Date(message.message_sent_date),
                    "afterbegin");
    }
    else {
      appendMessage(chat_user.username, chat_user.profile_img,
                    "left", message.content, new Date(message.message_sent_date),
                    "afterbegin");
    }
   scroll += get(".msg").clientHeight;
  });

  msgerChat.scrollTop += scroll;

  if(messages.next !== null) {
    pagination_page++;
  }
  else {
    pagination_page = null;
  }
  hideLoader();
}


async function refresh_messages() {
  pagination_page = 1;
  messagesDiv.innerHTML = '';
  await load_messages();
}

load_messages();

msgerChat.addEventListener('scroll', () => {
  if (msgerChat.scrollTop === 0 && pagination_page !== null) {
    load_messages();
  };
}, {
  passive: true
});
