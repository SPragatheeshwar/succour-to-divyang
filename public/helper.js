const socket = io('/')
const links = document.getElementById('links')



socket.emit('show-patients')
socket.on("helpers",function(data){
    console.log("Got it")
    console.log(data)
    data.patients.forEach(element => {
        var z = document.createElement('a'); // is a node
        console.log(element.roomId)
        console.log("HELO")
        z.href = `/${element.roomId}`
        z.innerText = `${element.userId}`
        links.appendChild(z);
    });
})



