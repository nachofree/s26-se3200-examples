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

console.log("connected")
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