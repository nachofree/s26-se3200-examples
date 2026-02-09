function clearHighlights() {
        document.querySelectorAll('.highlight').forEach(function(el) {
            el.classList.remove('highlight');
        });
    }
    function showResult(text) {
        document.getElementById('result').textContent = text;
    }
    function onFirstChildBtnClick() {
        clearHighlights();
        document.querySelectorAll('.list-item p:first-child').forEach(function(el) { el.classList.add('highlight'); });
        showResult('Highlighted: .list-item p:first-child');
    }
    function onNthChildBtnClick() {
        clearHighlights();
        document.querySelectorAll('.list-item p:nth-child(2)').forEach(function(el) { el.classList.add('highlight'); });
        showResult('Highlighted: .list-item p:nth-child(2)');
    }
    function onHoverBtnClick() {
        clearHighlights();
        showResult('Hover over any paragraph to see the :hover effect!');
    }
    function onDescendantBtnClick() {
        clearHighlights();
        document.querySelectorAll('.list-item p').forEach(function(el) { el.classList.add('highlight'); });
        showResult('Highlighted: Descendant selector .list-item p');
    }
    function onComplexBtnClick() {
        clearHighlights();
        document.querySelectorAll('div.list-item p').forEach(function(el) { el.classList.add('highlight'); });
        showResult('Highlighted: div.list-item p');
    }

    document.getElementById('first-child-btn').addEventListener('click', onFirstChildBtnClick);
    document.getElementById('nth-child-btn').addEventListener('click', onNthChildBtnClick);
    document.getElementById('hover-btn').addEventListener('click', onHoverBtnClick);
    document.getElementById('descendant-btn').addEventListener('click', onDescendantBtnClick);
    document.getElementById('complex-btn').addEventListener('click', onComplexBtnClick);

    const cars = ["Saab", "Volvo", "Toyota", "Volkwagon", 'Ford', 'Dodge', 'Chevy', 'Gmc']
    console.log(cars[0])
    cars[1] = "honda"
    console.log(cars[1])
    console.log(cars.toString())


    let ul = document.createElement('ul')
    let body = document.querySelector('body')
    body.appendChild(ul)

    console.log("The lenght of ht earrary is ", cars.length)
    let r = Math.random()
    console.log("r is ", r)
    
    r = r * cars.length
    console.log("r is ", r)
    r = Math.floor(r)
    console.log("r is after flooring", r)

    console.log("A random car is ", cars[r])
    let rcar = cars[r]
    cars.forEach(buildCar)



    function buildCar (item) {
        console.log("The item is ", item, "the car is ", rcar)
        if (item === rcar)
        {
            console.log("YAYAYAYY")
        }
        else
        {
            console.log("NOTAMATCH")
        }
        console.log("The item is ", item)
        let li = document.createElement('li')
        ul.appendChild(li)
        li.innerHTML = item
    }

    let testElementText = document.querySelector("#inputText")
    let btn = document.querySelector("#submitBtn")
    let ol = document.querySelector("#myOL")

    btn.addEventListener('click', function (){
        console.log("heello")
        let li = document.createElement("li")
        li.innerHTML = testElementText.value
        ol.appendChild(li)

    })

    // fetch("https://icanhazdadjoke.com/", {
    fetch("https://api.jsonbin.io/v3/b/6977df03ae596e708ff88cef", {
        // headers: {
        //     'Accept': 'application/json'
        // }
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        // console.log(data);
        console.log(data.record)
        alert(data.record[0].make)
    });




