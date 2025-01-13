socket.on('offerAwaiting', offers => {
    createOffers(offers);
 })
 
 socket.on('availableOffers', offers => {
    createOffers(offers);
 })
 
 socket.on('receivedIceCandidateFromServer', iceCandidate => {
     addNewIceCandidate(iceCandidate);
     console.log(iceCandidate);
 })
 
 socket.on('answerResponse', offer => {
     console.log(offer);
     addAnswer(offer);
 })
 
 socket.on('callEnded', () => {
     endCall();
 })
 
 
 function createOffers(offers) {
     offers.forEach(o => {
         console.log(o);
         
         document.getElementById('username2').innerHTML=o.offererUsername;
 
         const controlsContainer = document.getElementById('controls');
         const answerBtnContainer = document.createElement('div');
         answerBtnContainer.classList.add('control-container');
         answerBtnContainer.id = 'answer';
 
         const btnImage = document.createElement('img');
         btnImage.src='icons/call.png';
 
         answerBtnContainer.appendChild(btnImage);
         const firstChild = controlsContainer.firstChild;
         controlsContainer.insertBefore(answerBtnContainer, firstChild);
         answerBtnContainer.style.display = 'block';
 
         const joinButton = document.getElementById('join');
         controlsContainer.removeChild(joinButton);
 
         answerBtnContainer.addEventListener('click', () => answerOffer(o));
     })
 }