const default_user_img = document.getElementById("default_user_img").textContent;
const user_id = document.getElementById("user_id").textContent;
const domain = window.location.origin

function get_messages() {
    fetch(domain + '/api/messages?' + new URLSearchParams({username: 'doug.test'}), {
        method: "GET",
        headers: {
        "Content-Type": "application/json",
        },
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
        console.log(resp.data)
        if (resp.status_code === 200) {
            resp.data.results.forEach(message => {
                if(message.sender == user_id) {
                    appendMessage('Doug', '', "right", message.content);
                }
                else {
                    appendMessage('Doug.test', '', "left", message.content);
                }
            });
          }
        })
}


const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
    <img src="${img}" class="msg-img"/>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}


// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

get_messages()
