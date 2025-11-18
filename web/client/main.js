console.log("loaded properly !!!!")

function testik(){
    fetch("https://localhost:8443/api/idk")
        .then(response => response.text())
        .then(text => {
            console.log("Response:", text);
        })
        .catch(err => console.error(err));
}