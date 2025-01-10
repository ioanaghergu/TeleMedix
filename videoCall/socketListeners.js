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


function createOffers(offers) {
    const answerEl = document.querySelector('#answer');
    offers.forEach(o => {
        console.log(o);
        const newOfferEl = document.createElement('div');
        newOfferEl.innerHTML = `<button class="btn btn-success col-1">Answer ${o.offererUsername}</button>`;
        newOfferEl.addEventListener('click', () => answerOffer(o));
        answerEl.appendChild(newOfferEl);
    })
}