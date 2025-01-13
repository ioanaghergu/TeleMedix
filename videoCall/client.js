const urlParams = new URLSearchParams(window.location.search);

const username=urlParams.get('username');;
const appointmentId=urlParams.get('appointmentID');

console.log("Username", username);
console.log("Appointment", appointmentId);

document.querySelector('#username').innerHTML = username;


const constraints = {
    audio: {
        echoCancellation: true, 
        noiseSuppression: true, 
        autoGainControl: true  
    },
    video: true

};
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
    const controlsContainer = document.getElementById('controls');
    const joinButton = document.getElementById('join');
    controlsContainer.removeChild(joinButton);


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
            const stream = await navigator.mediaDevices.getUserMedia(constraints);

            localVideoEl.srcObject = stream;
            localStream = stream;
            localVideoEl.muted = true;

            document.getElementById('username').style.bottom = '340px';
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

        document.getElementById('remoteVideo').srcObject = remoteStream;

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
    const controlsContainer = document.getElementById('controls');
    
    const answerButton = document.getElementById('answer');
    
    controlsContainer.removeChild(answerButton);


    await fetchUserMedia();
    await createConnection(offerObj);

    document.getElementById('remoteVideo').style.display = 'block';
    document.getElementById('localVideo').classList.add('smallFrame');

    const username1 = document.getElementById('username');
    const username2 = document.getElementById('username2');
    
    username2.style.display = 'block';
    username2.style.top = '600px';
    username2.style.left = '20px';

    username1.style.bottom ='';
    username1.classList.add('smallUsername');
    //document.getElementById('username').style.position = 'fixed';
    //document.getElementById('username').style.bottom = '200px';

    

    const answer = await connection.createAnswer({});

    await connection.setLocalDescription(answer);

    console.log(offerObj);
    console.log(answer);

    offerObj.answererUsername=username;
    offerObj.answer = answer;

    const offererIceCandidates = await socket.emitWithAck('newAnswer', offerObj);

    offererIceCandidates.forEach(c => {
        connection.addIceCandidate(c);
        console.log("Client 2: added ice candidates");
    })

    console.log(offererIceCandidates);
}

const addAnswer = async(offer) => {

    const username1 = document.getElementById('username');
    const username2 = document.getElementById('username2');
    username2.innerHTML = offer.answererUsername;
    username2.style.display = 'block';
    username2.style.top = '600px';
    username2.style.left = '20px';

    

    document.getElementById('remoteVideo').style.display = 'block';
    document.getElementById('localVideo').classList.add('smallFrame');

    username1.classList.add('smallUsername');
    username1.style.bottom = '';
    //username1.style.position = 'fixed';
    
    await connection.setRemoteDescription(offer.answer);
}

function hangup() {
    leaveCall();
    document.getElementById('remoteVideo').style.display = 'none';
    document.getElementById('localVideo').classList.remove('smallFrame');
    document.getElementById('username').classList.remove('smallUsername');
    socket.emit('hangup', appointmentId);
    window.location.href=`http://127.0.0.1:5000/my-consultations?appointment_id=${appointmentId}&status_appointment=${status}`;
}

function endCall() {
    leaveCall();
    document.getElementById('remoteVideo').style.display = 'none';
    document.getElementById('localVideo').classList.remove('smallFrame');
    document.getElementById('username').classList.remove('smallUsername');
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

let toggleCamera = async () => {
    let videoTrack = localStream.getTracks().find(track => track.kind === 'video');

    if(videoTrack.enabled)
    {
        videoTrack.enabled = false;
        document.getElementById('camera').style.backgroundColor = 'rgb(255, 80, 80)';
    }
    else
    {
        videoTrack.enabled = true;
        document.getElementById('camera').style.backgroundColor = 'rgb(179, 102, 249, .9)';

    }
}

let toggleMic = async () => {
    let audioTrack = localStream.getTracks().find(track => track.kind === 'audio');

    if(audioTrack.enabled)
    {
        audioTrack.enabled = false;
        document.getElementById('mic').style.backgroundColor = 'rgb(255, 80, 80)';
    }
    else
    {
        audioTrack.enabled = true;
        document.getElementById('mic').style.backgroundColor = 'rgb(179, 102, 249, .9)';

    }
}

document.querySelector('#join').addEventListener('click', join);
document.querySelector('#hangup').addEventListener('click', hangup);
document.getElementById('camera').addEventListener('click', toggleCamera);
document.getElementById('mic').addEventListener('click', toggleMic);