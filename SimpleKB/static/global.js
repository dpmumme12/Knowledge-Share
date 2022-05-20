document.getElementById('notifications-toggle').addEventListener('click', show_notifications);
const domain = window.location.origin;
var notification_page = 1;

//takes cookie name input and gets a cookie from browser if it exists 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function error_message(message) {
    document.getElementById('messages').innerHTML = `<div class=" alert-error alert d-flex align-items-center alert-dismissible fade show animate__animated animate__fadeInDown">
                                                        <svg class="bi flex-shrink-0 me-2" width="17" height="17" role="img">
                                                            <use xlink:href="#exclamation-triangle-fill"/>
                                                        </svg>
                                                        ${message}
                                                        <a class="alert-close-button" data-bs-dismiss="alert" aria-label="Close"><i class="fa-solid fa-xmark"></i></a>
                                                    </div>`;
}

async function show_notifications() {
    var notifications_canvas = document.getElementById('notifications-canvas');
    var bsOffcanvas = new bootstrap.Offcanvas(notifications_canvas);
    notification_page = 1;

    await load_notifications();
    get('#notification-count').innerHTML = '0';

    bsOffcanvas.show();
}

async function load_notifications() {
    notifications = await get_notifications(notification_page);
    
    if (notifications.results.length === 0) {
        get('#notifications-list').innerHTML = '<p>No notifications...</p>';
    }
    else {
        if(notification_page === 1) {get('#notifications-list').innerHTML = '';}
        notifications.results.forEach(notification => {
            append_notification(notification.id, notification.message, notification.seen, new Date(notification.created_on));
        });
    }

    if(notifications.next !== null) {
        notification_page++;
        load_more = `<button class="btn btn-primary" onclick="load_notifications()">Load more</button>`;

        get('#load-more-btn').innerHTML = load_more;
      }
    else {
        notification_page = null;
        get('#load-more-btn').innerHTML = '';
      }
}

async function get_notifications(page) {
    var response = await fetch(domain + `/api/notifications?page=${page}`);

    if(!response.ok) {
      error_message(`An error ocurred gathering notifications: ${response.status}`);
    }
    
    return await response.json();
}

function append_notification(id, content, seen, date) {
    notification_html = `
    <li id="notification-${id}" class="list-group-item">
        <div class="d-inline-block" style="width: 90%;">
        ${content}
        </div>
        <div class="d-inline-block float-end text-end" style="width: 10%;">
        <a style="cursor: pointer;" onclick="delete_notification(${id})">
        <i class="fa-solid fa-trash-can fa-xs text-danger"></i>
        </a>
        </div>
        <div class="w-100 text-end">
        <small>${formatDate(date)}</small>
        </div>
    </li>
  `;

  get('#notifications-list').insertAdjacentHTML('beforeend', notification_html);
}

function delete_notification(id) {
    fetch(domain + `/api/messages?pk=${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
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
        if(resp.status_code === 204) {
          get(`#notification-${id}`).remove();
        }
      })
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
