console.log("loaded properly !!!!")

function useState(id, value){
    elements = document.querySelectorAll(id)
    for (i = 0; i < elements.length; i++){
        elements[i].innerText = value
    }
}

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

function testik2() {
    fetch("https://localhost:8443/api/idk", {
        method: "GET",
    })
        .then(response => response.text())
        .then(text => {
            console.log("Response:", text);
            useState("#response", text)
        })
        .catch(err => console.error(err));
}