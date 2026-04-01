console.log("connected")

const saveBtn = document.querySelector("#save")
const deleteBtn = document.querySelector("#unsave")
const colorPicker = document.querySelector("#colorPicker")

saveBtn.addEventListener("click", function(){
    console.log("Favorite color", colorPicker.value)

    let data = "color="+encodeURIComponent(colorPicker.value)

    fetch("http://localhost:5000/sessions/settings", {
        headers: {
            "Authorization": authorizationHeader(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method: "PUT",
        body: data
    })
    .then(function(response){
        console.log("Returned from api call")
    })
})

function authorizationHeader(){
    let sessionID = localStorage.getItem("sessionID")
    if (sessionID){
        console.log("Found a session on the client")
        return `Bearer ${sessionID}`
    }
    else {
        return "";
    }
}

function createSessionId(){
    fetch("http://localhost:5000/sessions", {
        headers: {
            "Authorization": authorizationHeader()
        }
    }).then(function(response){
        response.json().then(function(session){
            localStorage.setItem('sessionID', session.id)
            if (session.data.fav_color)
            {
                document.body.style.backgroundColor = session.data.fav_color
            }
        })
    })
}

createSessionId()