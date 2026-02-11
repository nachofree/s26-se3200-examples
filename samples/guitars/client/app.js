function build_guitar_div(guitar)
{
    let grid_div = document.querySelector("#guitar_grid")
    let new_div = document.createElement("div")
    let div_header = document.createElement("h1")
    let p_price = document.createElement("p")
    let p_rating = document.createElement("p")

    div_header.innerHTML = guitar.name
    p_price.innerHTML = guitar.price
    p_rating.innerHTML = guitar.rating

    grid_div.appendChild(new_div)
    new_div.appendChild(div_header)
    new_div.appendChild(p_price)
    new_div.appendChild(p_rating)
}


const createBtn = document.querySelector('#add_btn')
createBtn.onclick = function (){
    console.log("clicked")
    //get the information from the form and send it
    let name = document.querySelector('#guitar_name').value
    let price = document.querySelector('#guitar_price').value
    let rating = document.querySelector('#guitar_rating').value
    console.log(name,price, rating)
    let mydata = "name="+encodeURIComponent(name)
    mydata += "&price="+encodeURIComponent(price)
    mydata += "&rating="+encodeURIComponent(rating)
    console.log("The query string is ", mydata)
    fetch("http://localhost:5000/guitars", {
        method: "POST",
        body: mydata,
        headers: {
            "Content-Type":"application/x-www-form-urlencoded"
        }
    }).then(function(response){
        console.log("New review created", response)
        document.getElementById('guitar_form').reset();
        modal.classList.remove('show');
        load_page();
    })
}



// Modal functionality
const modal = document.getElementById('guitar_modal');
const addBtn = document.getElementById('add_guitar_btn');
const cancelBtn = document.getElementById('cancel_btn');

addBtn.addEventListener('click', function() {
    modal.classList.add('show');
});

cancelBtn.addEventListener('click', function() {
    modal.classList.remove('show');
    document.getElementById('guitar_form').reset();
});

// Close modal when clicking outside of it
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.classList.remove('show');
        document.getElementById('guitar_form').reset();
    }
});

function load_page(){
console.log("connected")
//make sure that nothing is in the guitar_grid
let grid_div = document.querySelector("#guitar_grid")
grid_div.innerHTML = ""

fetch("http://localhost:5000/guitars")
.then(function(response){
    console.log(response)
    return response.json();
    // return response.text();
   
})
 .then(function(data){
        console.log(data)
        data.forEach(function (guitar){
            build_guitar_div(guitar)
        })
    })
}

load_page()