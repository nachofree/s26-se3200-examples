
console.log("Connected")

//color picker

let inputFavColor = document.querySelector('#colorPicker')
let saveColorButton = document.querySelector('#save')
let unsaveColorButton = document.querySelector('#unsave')

unsaveColorButton.addEventListener("click", function () {

  fetch("http://localhost:8080/sessions", {
    headers: {
      "Authorization": authorizationHeader(),
      "Content-Type": "application/x-www-form-urlencoded"

    },
    method: "DELETE",
  })
    .then(function (response) {
      console.log("response is : ", response.text())
      document.body.style.backgroundColor = "white";

    })
})

saveColorButton.addEventListener("click", function () {
  console.log("Favcolor: ", inputFavColor.value)
  let data = "color=" + encodeURIComponent(inputFavColor.value)

  fetch("http://localhost:8080/sessions/settings", {
    headers: {
      "Authorization": authorizationHeader(),
      "Content-Type": "application/x-www-form-urlencoded"

    },
    method: "PUT",
    body: data,
    // credentials: "include"
  })
    .then(function (response) {
      console.log("response is : ", response.text())
      document.body.style.backgroundColor = inputFavColor.value;

    })
})

function authorizationHeader() {
  let sessionID = localStorage.getItem("sessionID");
  if (sessionID) {
    console.log("Found session id in authorizationHeader()")
    return `Bearer ${sessionID}`;
  }
  else {
    return null;
  }
}

function createSessionId() {
  console.log("The auth header is", authorizationHeader())
  fetch("http://localhost:8080/sessions", {
    headers: {
      "Authorization": authorizationHeader()
    }
  }).then(function (response) {
    //server responds with a session id the first time
    if (response.status == 200) {
      response.json().then(function (session) {
        localStorage.setItem('sessionID', session.id);
        console.log("Your favorite color is ", session.data.fav_color)
        if (session.data.fav_color) {
          inputFavColor.value = session.data.fav_color;
          document.body.style.backgroundColor = session.data.fav_color
        }
        //only load if the are authenticated

        //loadrcfromServer();

      })
    }
  })
}
createSessionId();
