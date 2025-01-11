const urlParams = new URLSearchParams(window.location.search);

const username=urlParams.get('username');;
const appointmentId=urlParams.get('appointmentID');

console.log("Username", username);
console.log("Appointment", appointmentId);

document.querySelector('#username').innerHTML = username;


//for testing on another device on the same network
//const socket = io.connect('https://LOCAL-IP:8080',
const socket = io.connect('https://localhost:8080',
    {
        auth: {
            username,
            appointmentId
        }
    }
);

const localVideoEl = document.querySelector('#localVideo');
const remoteVideoEl = document.querySelector('#remoteVideo');

let localStream;
let remoteStream;
let connection;
let whoOffered = false; //true for local client, false for remote client
let status = "Attended";

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
    console.log(username);
    console.log(appointmentId);

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
                    //appointmentId: appointmentId,
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

function hangup() {
    leaveCall();
    socket.emit('hangup', appointmentId);
    window.location.href=`http://127.0.0.1:5000/my-consultations?appointment_id=${appointmentId}&status_appointment=${status}`;
}

function endCall() {
    leaveCall();
    console.log("call ended");
    window.location.href=`http://127.0.0.1:5000/my-consultations?appointment_id=${appointmentId}&status_appointment=${status}`;
    
}

function leaveCall() {
    if(connection)
    {
        connection.close();
        connection = null;
    }

    if(localStream)
    {
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;
    }

    if(remoteStream)
    {
        remoteStream.getTracks().forEach(track => track.stop());
        remoteStream = null;
    }

    localVideoEl.srcObject = null;
    remoteVideoEl.srcObject = null;
}


document.querySelector('#join').addEventListener('click', join);
document.querySelector('#hangup').addEventListener('click', hangup);
