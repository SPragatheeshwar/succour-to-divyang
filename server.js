const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const { v4: uuidV4 } = require('uuid')

const patients = []

app.set('view engine', 'ejs')
app.use(express.static('public'))

io.on('connection', socket => {

  socket.on('show-patients',()=>{
    socket.emit('helpers',{patients})
  })



  socket.on('join-room', (roomId, userId) => {
    socket.join(roomId)
      patients.push({roomId,userId})
    socket.to(roomId).broadcast.emit('user-connected', userId)

    socket.on('disconnect', () => {
      socket.to(roomId).broadcast.emit('user-disconnected', userId)
      let index = patients.indexOf({roomId,userId})
      if (index > -1) {
        patients.splice(index, 1); // 2nd parameter means remove one item only
      }
    })
  })

  socket.on('end-call',(roomId,userId) => {
    console.log("Emit")
    patients.forEach(el => {
      if (el.roomId == roomId ){
        // var destination = '/home';
        // socket.emit('redirect', destination);
        socket.disconnect()
      }
    })
  })
})

app.get("/home",(req,res)=>{
  res.render("home")
})


app.get('/helpers',(req,res)=>{
  console.log(patients)
  res.render('helper')
})

app.get('/', (req, res) => {
  res.redirect(`/${uuidV4()}`)
})

app.get('/:room', (req, res) => {
  console.log("first")
  res.render('room', { roomId: req.params.room })
})



server.listen(3000)