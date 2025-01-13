const fs = require('fs');
const https = require('https'); //module for creating a secure HTTPS server
const express = require('express');
const socketio = require('socket.io');
const path = require('path');



const app = express();
app.use(express.static(__dirname))

//to be able to connect two clients using WebRTC we have to use a secure connection
//the function that fetches the user feed requires a certificate, otherwise it will block the content
//so I generate a key and a certificate to run a secure connection
const key = fs.readFileSync('cert.key');
const cert = fs.readFileSync('cert.crt');

//create https server
const server = https.createServer({key, cert}, app);

//enable real-time communication between clients by
//binding socket.io to our server, configuring the routes and permitted HTTP methods
const io = socketio(server, {
    cors: {
        origin: [
            'https://localhost',
            //'https://LOCAL-IP' //for testing on another device on the same network
           
        ],

        methods: ["GET", "POST"]

    }
});

server.listen(8080);

app.get('/:appointmentID/:username', (req, res) => {
    const appointmentID = req.params.appointmentID;
    const username = req.params.username;

    const redirectURL = `https://localhost:8080/?appointmentID=${appointmentID}&username=${username}`;

    //const redirectURL = `https://LOCAL_IP:8080/?appointmentID=${appointmentID}&username=${username}`;
 
    res.redirect(redirectURL); 
});


let offers = [];

const connectedSockets = [];

io.on('connection', (socket) => {
    console.log("Server: a client has connected");

    const username = socket.handshake.auth.username;
    const appointmentId = socket.handshake.auth.appointmentId;

    console.log("server", username)
    console.log("server", appointmentId)
    
    connectedSockets.push({
        socketId: socket.id,
        username: username,
        appointment_id: appointmentId
    });

    if(!appointmentId)
    {
        console.log("Disconnect client");
        socket.disconnect();
        return;
    }

    const offersToSend = offers.filter(o => o.offererAppointmentId === appointmentId)
    console.log(offersToSend);

    if(offersToSend.length)
    {
        socket.emit('availableOffers', offersToSend);
    }

    socket.on('newOffer', newOffer => {
        offers.push({
            offererUsername: username,
            offer: newOffer,
            offererIceCandidates: [],
            offererAppointmentId: appointmentId,
            answererUsername: null,
            answer: null,
            answererIceCandidates: [],
            answererAppointmentId:null
        })

        socket.broadcast.emit('offerAwaiting', offersToSend.slice(-1));
    })

    socket.on('sendIceCandidateToServer', iceCandidateObj => {
        const {iceCandidate, iceUsername, whoOffered} = iceCandidateObj;
        console.log(iceCandidate);

        if(whoOffered)
        {
            const offer = offers.find(o => o.offererUsername === iceUsername);

            if(offer)
            {
                offer.offererIceCandidates.push(iceCandidate);

                if(offer.answererUsername)
                {
                    const answererSocket = connectedSockets.find(s => s.username === offer.answererUsername);

                    if(answererSocket)
                    {
                        socket.to(answererSocket.socketId).emit('receivedIceCandidateFromServer', iceCandidate);
                    }
                    else
                    {
                        console.log("Can't find answerer for the ice candidate received");
                    }
                }
            }

        }
        else
        {
            const offer = offers.find(o => o.answererUsername === iceUsername);
            const offererSocket = connectedSockets.find(s => s.username === offer.offererUsername);

            if(offererSocket)
            {
                socket.to(offererSocket.socketId).emit('receivedIceCandidateFromServer', iceCandidate);
            }
            else
            {
                console.log("Can't find offerer for the ice candidate received");
            }
          
        }


    })

    socket.on('newAnswer', (offer, ackFunction) => {
        console.log(offer);
        const offererSocket = connectedSockets.find(s => s.username === offer.offererUsername);

        if(!offererSocket)
        {
            console.log('No matching socket');
            return;
        }

        const offererSocketId = offererSocket.socketId;

        const updatedOffer = offers.find(o => o.offererUsername === offer.offererUsername);
        updatedOffer.answer = offer.answer;
        updatedOffer.answererUsername=username;
        updatedOffer.answererAppointmentId=appointmentId;
        socket.to(offererSocketId).emit('answerResponse', updatedOffer);
    })

    socket.on('hangup', (appointmentId) => {

        const socketToSendTo = connectedSockets.find(s => s.appointment_id === appointmentId);
        const socketToSentToId = socketToSendTo.socketId;
        socket.to(socketToSentToId).emit('callEnded');
    })
})
