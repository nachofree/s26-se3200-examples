function build_guitar_div(guitar)
{
    let grid = document.querySelector('.guitar_grid')
    let div = document.createElement('div')
    div.classList.add('guitar_div')
    let h = document.createElement('h1')
    h.innerHTML = guitar.name
    let p_price = document.createElement('p')
    p_price.classList.add('price')
    let p_rating = document.createElement('p')
    p_rating.classList.add('rating')
    p_rating.style.setProperty("--rating", guitar.rating)
    p_price.innerHTML = guitar.price
    // p_rating.innerHTML = guitar.rating

    grid.appendChild(div)
    div.appendChild(h)
    div.appendChild(p_price)
    div.appendChild(p_rating)
}



console.log("connected")
fetch("http://localhost:5000/guitars")
.then(function(response){
    console.log(response)
    // response.json();
    return response.json();
   
})
 .then(function(data){
        console.log(data)
        //add guitar item
        data.forEach( function (guitar){
            console.log(guitar)
            build_guitar_div(guitar)
        })
    })