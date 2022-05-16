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
        if (resp.status_code === 200) {
            console.log(resp.data)
          }
        })
}