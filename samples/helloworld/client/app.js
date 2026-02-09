console.log("connected")
fetch("http://localhost:5000/")
.then(function(response){
    console.log(response)
    // response.json();
    return response.text();
   
})
 .then(function(data){
        console.log(data)
    })