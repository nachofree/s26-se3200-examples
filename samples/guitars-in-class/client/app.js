// Modal state variables
let modalMode = 'add'; // 'add' or 'edit'
let editingGuitarId = null; // ID of guitar being edited

function build_guitar_div(guitar) {
    let grid_div = document.querySelector("#guitar_grid")
    let new_div = document.createElement("div")
    let div_header = document.createElement("h1")
    let p_price = document.createElement("p")
    let p_rating = document.createElement("p")
    let actions_div = document.createElement("div")
    let edit_icon = document.createElement("span")
    let delete_icon = document.createElement("span")

    div_header.innerHTML = guitar.name
    p_price.innerHTML = guitar.price
    p_rating.innerHTML = guitar.rating

    actions_div.className = "guitar-actions"
    edit_icon.className = "material-icons"
    edit_icon.innerHTML = "edit"
    edit_icon.onclick = function() {
        openEditModal(guitar);
    }
    delete_icon.className = "material-icons"
    delete_icon.innerHTML = "delete"
    delete_icon.onclick = function() {
        // TODO: Implement delete functionality
        console.log("Delete guitar:", guitar.name);
        fetch("http://localhost:5000/guitars/"+guitar.id, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function () {
        console.log("New guitar created")
        load_page()
    })

    }

    grid_div.appendChild(new_div)
    new_div.appendChild(div_header)
    new_div.appendChild(p_price)
    new_div.appendChild(p_rating)
    new_div.appendChild(actions_div)
    actions_div.appendChild(edit_icon)
    actions_div.appendChild(delete_icon)
}


const modalAddBtn = document.querySelector("#add_btn")
modalAddBtn.onclick = function () {
    console.log("Clicked the button")
    let name = document.querySelector("#guitar_name").value
    let rating = document.querySelector("#guitar_rating").value
    let price = document.querySelector("#guitar_price").value

    console.log(name, rating, price)
    let data = "name=" + encodeURIComponent(name)
    data += "&rating=" + encodeURIComponent(rating)
    data += "&price=" + encodeURIComponent(price)

    console.log("The query string is ", data)
    
    if (modalMode === 'add') {
        fetch("http://localhost:5000/guitars", {
            method: "POST",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(function () {
            console.log("New guitar created")
            load_page()
            closeModal();
        })
    } else if (modalMode === 'edit') {
        fetch("http://localhost:5000/guitars/" + editingGuitarId, {
            method: "PUT",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(function () {
            console.log("Guitar updated")
            load_page()
            closeModal();
        })
    }
}




// Modal functionality
const modal = document.getElementById('guitar_modal');
const addBtn = document.getElementById('add_guitar_btn');
const cancelBtn = document.getElementById('cancel_btn');
const modalTitle = document.querySelector('.modal-content h2');
const modalSubmitBtn = document.getElementById('add_btn');

function openEditModal(guitar) {
    modalMode = 'edit';
    editingGuitarId = guitar.id;
    
    // Update modal title and button
    modalTitle.textContent = 'Edit Guitar';
    modalSubmitBtn.textContent = 'Save';
    
    // Populate form with guitar data
    document.querySelector('#guitar_name').value = guitar.name;
    document.querySelector('#guitar_price').value = guitar.price;
    document.querySelector('#guitar_rating').value = guitar.rating;
    
    // Open modal
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
    document.getElementById('guitar_form').reset();
    
    // Reset modal state
    modalMode = 'add';
    editingGuitarId = null;
    modalTitle.textContent = 'Add New Guitar';
    modalSubmitBtn.textContent = 'Add';
}

addBtn.addEventListener('click', function () {
    modal.classList.add('show');
});

cancelBtn.addEventListener('click', function () {
    closeModal();
});

// Close modal when clicking outside of it
window.addEventListener('click', function (event) {
    if (event.target === modal) {
        closeModal();
    }
});

function load_page() {
    let grid_div = document.querySelector("#guitar_grid")
    grid_div.innerHTML = ""
    console.log("connected")
    fetch("http://localhost:5000/guitars")
        .then(function (response) {
            console.log(response)
            return response.json();
            // return response.text();

        })
        .then(function (data) {
            console.log(data)
            data.forEach(function (guitar) {
                build_guitar_div(guitar)
            })
        })
}
load_page()