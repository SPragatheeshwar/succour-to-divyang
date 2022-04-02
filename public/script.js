const socket = io('/')
const videoGrid = document.getElementById('video-grid')
const endBtn = document.getElementById('end')
//A peer server is started on the host computer for faciltation between p2p
const myPeer = new Peer(undefined, {
  host: '/',
  port: '3001'
})
const myVideo = document.createElement('video')
myVideo.muted = true
var peerID;
const peers = {}

myPeer.on('open', id => {
  console.log("Joining room")
  console.log(ROOM_ID) //given by server on making connection
  console.log(id) //given by peer server
  peerID = id
  socket.emit('join-room', ROOM_ID, id)
})


navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true
}).then(stream => {
  //as soon as possible add current person stream
  addVideoStream(myVideo, stream)

  //HELPER SIDE
  //peers will be connected due to connectToNewUser
  myPeer.on('call', call => { 
    console.log("Only when patient is present")
    //when helper joins room
    call.answer(stream) //giving helper stream
    const video = document.createElement('video')
    //adding patient stream to helper screen
    call.on('stream', userVideoStream => {
      addVideoStream(video, userVideoStream)
    })
  })

  //PATIENT SIDE
  socket.on('user-connected', userId => {
    //when helper joins my call - we get  userId
    connectToNewUser(userId, stream)
  })
})

socket.on('user-disconnected', userId => {
  if (peers[userId]) peers[userId].close()
})

endBtn.onclick = endCall

function endCall(){
  console.log("END")
  socket.emit("end-call",ROOM_ID, peerID)
  window.location.replace('/home');
}


function connectToNewUser(userId, stream) {
    //happens when userid != id(patientid)
  const call = myPeer.call(userId, stream) //sending patient stream
  const video = document.createElement('video')

  //happens when userid != id
  call.on('stream', userVideoStream => { //getting helper stream
    //addVideoStream(video, userVideoStream)
  })
  call.on('close', () => {
    video.remove()
  })

  peers[userId] = call
}

function addVideoStream(video, stream) {
  video.srcObject = stream
  video.addEventListener('loadedmetadata', () => {
    video.play()
  })
  videoGrid.append(video)
}