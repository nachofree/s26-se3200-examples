// app.js

function handleApiResponse(response) {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

function displayData(data) {
    var container = document.getElementById('data-container');
    container.innerHTML = '';
    if (!Array.isArray(data)) {
        container.textContent = 'Unexpected data format.';
        return;
    }
    data.forEach(createGuitarCard);
}

function createGuitarCard(guitar) {
    var container = document.getElementById('data-container');
    var card = document.createElement('div');
    card.className = 'guitar-card';

    var img = document.createElement('img');
    img.className = 'guitar-img';
    img.alt = guitar.make + ' ' + guitar.model;
    img.src = getSampleGuitarImage(guitar);
    card.appendChild(img);

    var info = document.createElement('div');
    info.className = 'guitar-info';
    info.innerHTML =
        '<strong>' + guitar.make + ' ' + guitar.model + '</strong><br>' +
        'Color: ' + guitar.color + '<br>' +
        'Price: $' + guitar.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});

    var actions = document.createElement('div');
    actions.className = 'guitar-actions';

    var editBtn = document.createElement('button');
    editBtn.className = 'edit-btn';
    editBtn.textContent = 'Edit';
    editBtn.disabled = true;
    actions.appendChild(editBtn);

    var deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.textContent = 'Delete';
    deleteBtn.disabled = true;
    actions.appendChild(deleteBtn);

    card.appendChild(info);
    card.appendChild(actions);
    container.appendChild(card);
}

function getSampleGuitarImage(guitar) {
    var images = {
        'Fender Stratocaster': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
        'Gibson Les Paul Standard': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80',
        'PRS Custom 24': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
        'Ibanez RG550': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
        'Yamaha Pacifica 112V': 'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80',
        'Taylor 214ce': 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
        'Martin D-28': 'https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=400&q=80',
        'Epiphone SG Standard': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80',
        'Gretsch G5420T': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
        'Schecter Hellraiser C-1': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80'
    };
    var key = guitar.make + ' ' + guitar.model;
    if (images[key]) {
        return images[key];
    }
    return 'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80'; // fallback
}

function renderAddGuitarForm() {
    var container = document.getElementById('data-container');
    var formWrapper = document.createElement('div');
    formWrapper.className = 'add-guitar-form-wrapper';
    var form = document.createElement('form');
    form.className = 'add-guitar-form';
    form.innerHTML =
        '<h2>Add New Guitar</h2>' +
        '<input type="text" name="make" placeholder="Make" required />' +
        '<input type="text" name="model" placeholder="Model" required />' +
        '<input type="number" name="price" placeholder="Price" step="0.01" required />' +
        '<input type="text" name="color" placeholder="Color" required />' +
        '<button type="submit" disabled>Add Guitar</button>';
    formWrapper.appendChild(form);
    container.parentNode.insertBefore(formWrapper, container);
}

function handleError(error) {
    var container = document.getElementById('data-container');
    container.textContent = 'Error: ' + error.message;
    container.style.color = '#d32f2f';
}

function fetchData() {
    fetch('https://api.jsonbin.io/v3/b/6977df03ae596e708ff88cef')
        .then(handleApiResponse)
        .then(function(result) {
            if (result && result.record) {
                displayData(result.record);
                renderAddGuitarForm();
            } else {
                displayData([]);
                renderAddGuitarForm();
            }
        })
        .catch(handleError);
}

document.addEventListener('DOMContentLoaded', fetchData);
