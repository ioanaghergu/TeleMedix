const fs = require('fs');
const https = require('https'); //module for creating a secure HTTPS server
const express = require('express');
const session = require('express-session');
const socketio = require('socket.io');


const app = express();
app.use(express.static(__dirname))

//to be able to connect two clients using WebRTC we have to use a secure connection
//the function that fetches the user feed requires a certificate, otherwise it will block the content
//so I generate a key and a certificate to run a secure connection
const key = fs.readFileSync('cert.key');
const cert = fs.readFileSync('cert.crt');

//create https server
const server = https.createServer({key, cert}, app);

app.use(session({
    secret: 'dfscdj',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: true } 
  }));


//enable real-time communication between clients by
//binding socket.io to our server, configuring the routes and permitted HTTP methods
const io = socketio(server, {
    cors: {
        origin: [
            'https://localhost',
            // 'https://LOCAL-IP' for testing on another device on the same network
           
        ],

        methods: ["GET", "POST"]

    }
});

server.listen(8080);

app.get('/:appointmentID/:pacientID/:medicID', (req, res) => {
    const appointmentID = req.params.appointmentID;
    const pacientID = req.params.pacientID;
    const medicID = req.params.medicID;

   req.session.appointmentID=appointmentID;
   req.session.pacientID=pacientID;
   req.session.medicID=medicID;

    console.log('Appointment ID:', appointmentID);
    console.log('Patient ID:', pacientID);
    console.log('Doctor ID:', medicID);

    res.redirect('https://localhost:8080');
});

app.get('/get-session-data', (req, res) => {
    const { appointmentID, pacientID, medicID } = req.session;
    res.json({ appointmentID, pacientID, medicID });
});


let offers = [];

const connectedSockets = [];

io.on('connection', (socket) => {
    console.log("Server: a client has connected");

    const username = socket.handshake.auth.username;
    
    connectedSockets.push({
        socketId: socket.id,
        username: username
    });

    if(offers.length)
    {
        socket.emit('availableOffers', offers);
    }

    socket.on('newOffer', newOffer => {
        offers.push({
            offererUsername: username,
            offer: newOffer,
            offererIceCandidates: [],
            answererUsername: null,
            answer: null,
            answererIceCandidates: []
        })

        socket.broadcast.emit('offerAwaiting', offers.slice(-1));
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
        socket.to(offererSocketId).emit('answerResponse', updatedOffer);
    })


})

