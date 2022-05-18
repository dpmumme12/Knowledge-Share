const request_user = {"id": JSON.parse(document.getElementById("request_user_id").textContent),
                      "username": JSON.parse(document.getElementById("request_username").textContent),
                      "profile_img": JSON.parse(document.getElementById("request_user_img").textContent)
                    }
const chat_user = {"id": JSON.parse(document.getElementById("chat_user_id").textContent),
                   "username": JSON.parse(document.getElementById("chat_username").textContent),
                   "profile_img": JSON.parse(document.getElementById("chat_user_img").textContent)
                  }
const domain = window.location.origin
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
var pagination_page = 1;


msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  fetch(domain + '/api/messages', {
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
      appendMessage(request_user.username, request_user.profile_img, "right", resp.data.content, new Date(), "beforeend");
    }
  })
});


async function get_messages(page) {
    let response = await fetch(domain + `/api/messages?page=${page}&username=${chat_user.username}`)

    if(!response.ok) {
      error_message(`An error ocurred gathering the messages: ${response.status}`);
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

  msgerChat.insertAdjacentHTML(append, msgHTML);
  msgerChat.scrollTop += 500000;
}


async function load_messages() {
  var messages = await get_messages(pagination_page);
  console.log(messages)
  
  messages.results.forEach(message => {
    if(message.sender === request_user.id) {
      appendMessage(request_user.username, request_user.profile_img, "right", message.content, new Date(message.message_sent_date), "afterbegin");
    }
    else {
      appendMessage(chat_user.username, chat_user.profile_img, "left", message.content, new Date(message.message_sent_date), "afterbegin");
    }
  });

  if(messages.next !== null) {
    pagination_page++;
  }
  else {
    pagination_page = null;
  }
}


// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "  " + strTime;
}

load_messages();
