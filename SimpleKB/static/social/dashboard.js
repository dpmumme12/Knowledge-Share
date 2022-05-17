const main_follow_button = document.getElementById("main-follow-button");
const default_user_img = document.getElementById("default_user_img").textContent;
const user_id = document.getElementById("user_id").textContent;

if (main_follow_button !== null) {
  main_follow_button.addEventListener("click", follow_unfollow);
}

document.getElementById("following-div").addEventListener("click", get_following);
document.getElementById("followers-div").addEventListener("click", get_following);

function follow_unfollow(event) {
  var button = event.currentTarget;
  var id = button.getAttribute("data-id");
  var follower_count = Number(
    document.getElementById("follower-count").textContent
  );

  fetch(`/api/follow-unfollow/${id}`, {
    method: "POST",
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
      if (resp.status_code === 201) {
        if (resp.data.is_following) {
          button.classList.remove("btn-primary");
          button.classList.add("btn-danger");
          button.innerHTML = "Unfollow";
          if (button.id === "main-follow-button") {
            document.getElementById("follower-count").innerHTML = follower_count + 1;
          }
        } else {
          button.classList.remove("btn-danger");
          button.classList.add("btn-primary");
          button.innerHTML = "Follow";
          if (button.id === "main-follow-button") {
            document.getElementById("follower-count").innerHTML = follower_count - 1;
          }
        }
      }
    });
}


function get_following(event) {
  var modal = new bootstrap.Modal(
    document.getElementById("following-followers-popup")
  );
  var div = event.currentTarget;
  var url = div.getAttribute("data-url");
  if (div.id === "following-div") {
    document.getElementById("modal-title").innerHTML = "Following";
  } else {
    document.getElementById("modal-title").innerHTML = "Followers";
  }
  document.getElementById("modal-list").innerHTML = "";

  fetch(url, {
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
      if (resp.status_code === 200) {
        if (resp.data.length == 0) {
          document.getElementById("modal-list").innerHTML =
            "<p>No users found...</p>";
        } else {
          resp.data.forEach((user) => {
            const li = document.createElement("li");
            li.classList.add("list-group-item");
            const parent_div = document.createElement("div");
            const div1 = document.createElement("div");
            div1.classList.add(
              "d-inline-block",
              "popup-card-div",
              "follow-div"
            );
            div1.addEventListener(
              "click",
              (event) => (window.location.href = `/dashboard/${user.username}`)
            );
            const img = document.createElement("img");
            img.classList.add("rounded-circle", "popup-profile-img");
            if (user.profile_image !== "") {
              img.src = user.profile_image;
            } else {
              img.src = default_user_img;
            }
            const div2 = document.createElement("div");
            div2.classList.add("d-inline-block", "float-end");
            const button = document.createElement("button");
            button.classList.add("btn");
            if (user.is_following === true) {
              button.classList.add("btn", "btn-danger");
              button.innerHTML = "Unfollow";
            } else {
              button.classList.add("btn", "btn-primary");
              button.innerHTML = "Follow";
            }
            button.setAttribute("data-id", user.id);
            button.addEventListener("click", follow_unfollow);
            const p = document.createElement("p");
            p.classList.add("mb-0", "mt-1", "follow-div");
            p.innerHTML = "@" + user.username;
            p.addEventListener(
              "click",
              (event) => (window.location.href = `/dashboard/${user.username}`)
            );
            div1.appendChild(img);
            if (user.id != user_id && user_id != "null") {
              div2.appendChild(button);
            }
            parent_div.appendChild(div1);
            parent_div.appendChild(div2);
            parent_div.appendChild(p);
            li.appendChild(parent_div);

            document.getElementById("modal-list").appendChild(li);
          });
        }
      }
    });

  modal.show();
}
