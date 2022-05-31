try {
  get('#notifications-toggle').addEventListener('click', show_notifications);
} 
catch (error) {
  console.error(error);
}
const notifications_url = JSON.parse(get('#notifications_url').textContent);
var notification_page = 1;

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
            append_notification(notification.id, notification.message,
                                notification.seen, new Date(notification.created_on));
        });
    }

    if(notifications.next !== null) {
        notification_page++;
        load_more = `<button class="btn btn-primary" 
                    onclick="load_notifications()">Load more</button>
                    `;

        get('#load-more-btn').innerHTML = load_more;
      }
    else {
        notification_page = null;
        get('#load-more-btn').innerHTML = '';
      }
}

async function get_notifications(page) {
    var response = await fetch(notifications_url + `?page=${page}`);

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
    fetch(notifications_url + `?pk=${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        mode: "same-origin",
      })
      .then(async (response) => {
        return {
          status_code: response.status,
        };
      })
      .then((resp) => {
        if(resp.status_code === 204) {
          get(`#notification-${id}`).remove();
        }
      })
}
