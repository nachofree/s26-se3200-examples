console.log("connected")
let count = 1;
let item = document.querySelectorAll(".item")
item.forEach(changeText)



function changeText(item)
{
    item.innerHTML = "FOO" + count
    count +=1;

}