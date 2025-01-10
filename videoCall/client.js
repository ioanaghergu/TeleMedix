const username = "User-" + Math.floor(Math.random() * 1000);
document.querySelector('#username').innerHTML = username;

//for testing on another device on the same network
//const socket = io.connect('https://LOCAL-IP:8080', 
const socket = io.connect('https://localhost:8080',
    {
        auth: {
            username
        }
    }
);

const localVideoEl = document.querySelector('#localVideo');
const remoteVideoEl = document.querySelector('#remoteVideo');

let localStream;
let remoteStream;
let connection;
let whoOffered = false; //true for local client, false for remote client

let connConfiguration = {
    iceServers: [
        {
            urls: [
                'stun:stun.l.google.com:19302',
                'stun:stun1.l.google.com:19302'
            ]
        }
    ]
}

const join = async e => {
    console.log("client joined");

    await fetchUserMedia();
    console.log("got user media successfully");

    await createConnection();
    console.log("client connected");

    try{
        console.log("creating offer");
        const offer = await connection.createOffer();
        console.log(offer);
        connection.setLocalDescription(offer);
        whoOffered = true;
        socket.emit('newOffer', offer);

    }catch(err){
        console.log(err);
    }
}

const fetchUserMedia = () => {
    return new Promise(async(resolve, reject) => {
        try{
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                //audio: true
            });

            localVideoEl.srcObject = stream;
            localStream = stream;
            resolve();

        }catch(err){
            console.log(err);
            reject();
        }
    })
}

const createConnection = (offerObj) => {
    return new Promise(async(resolve, reject) => {
        connection = await new RTCPeerConnection(connConfiguration);
        remoteStream = new MediaStream();
        remoteVideoEl.srcObject = remoteStream;

        localStream.getTracks().forEach(track => {
            connection.addTrack(track, localStream);
        })

        connection.addEventListener("signalingstatechange", (event) => {
            console.log(event);
            console.log(connection.signalingState);
        })

        connection.addEventListener("icecandidate", (event) => {
            console.log("Local client: Ice candidate");
            console.log(event);

            if(event.candidate)
            {
                socket.emit('sendIceCandidateToServer', {
                    iceCandidate: event.candidate,
                    iceUsername: username,
                    whoOffered
                });
            }
        })

        connection.addEventListener('track', (event) => {
            console.log("got a track from the other client");
            console.log(event);
            event.streams[0].getTracks().forEach(track => {
                remoteStream.addTrack(track, remoteStream);
                console.log("connection is about to be active");
            })
        })

        if(offerObj)
        {
            console.log(connection.signalingState);
            await connection.setRemoteDescription(offerObj.offer);
            console.log(connection.signalingState);
        }

        resolve();

    })
}



const addNewIceCandidate = iceCandidate => {
    connection.addIceCandidate(iceCandidate);
    console.log("Remote client: added ice candidate");
}

const answerOffer = async(offerObj) => {
    await fetchUserMedia();
    await createConnection(offerObj);

    const answer = await connection.createAnswer({});

    await connection.setLocalDescription(answer);

    console.log(offerObj);
    console.log(answer);

    offerObj.answer = answer;

    const offererIceCandidates = await socket.emitWithAck('newAnswer', offerObj);

    offererIceCandidates.forEach(c => {
        connection.addIceCandidate(c);
        console.log("Client 2: added ice candidates");
    })

    console.log(offererIceCandidates);
}

const addAnswer = async(offer) => {
    await connection.setRemoteDescription(offer.answer);
}


document.querySelector('#join').addEventListener('click', join);

fetch('https://localhost:8080/get-session-data')
  .then(response => response.json())
  .then(data => {

    sessionStorage.setItem('appointmentID', data.appointmentID);
    sessionStorage.setItem('pacientID', data.pacientID);
    sessionStorage.setItem('medicID', data.medicID);

   
    console.log(sessionStorage.getItem('appointmentID'));
    console.log(sessionStorage.getItem('pacientID'));
    console.log(sessionStorage.getItem('medicID'));
  })
  .catch(error => {
    console.error('Error fetching session data:', error);
  });


