//idk lol, just wanted to make react like use state 
function useState(id, value){
    elements = document.querySelectorAll(id)
    for (i = 0; i < elements.length; i++){
        elements[i].innerText = value
    }
}

//this will probably be deleted
function testik() {
    fetch("https://localhost:8443/api/idk", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: document.getElementById("meow").value,
        })
    })
        .then(response => response.text())
        .then(text => {
            console.log("Response:", text);
            useState("#response", text)
        })
        .catch(err => console.error(err));
}

//this will probably be deleted too duh >w<
function testik2() {
    const id = document.getElementById("idInput").value;

    fetch(`https://localhost:8443/api/idk?id=${encodeURIComponent(id)}`, {
        method: "GET"
    })
        .then(response => response.text())
        .then(text => {
            console.log("Response:", text);
            useState("#response", text);
        })
        .catch(err => console.error(err));
}
