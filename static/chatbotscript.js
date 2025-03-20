document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendButton");
    const chatContainer = document.getElementById("chatContainer");
    const chatIcon = document.getElementById("chatIcon");

    function sendMessage() {
        let userMessage = chatInput.value.trim();
        if (userMessage === "") return;

       
        sendButton.disabled = true;

      
        let userMsgElem = document.createElement("p");
        userMsgElem.innerHTML = `<strong>You:</strong> ${userMessage}`;
        chatBody.appendChild(userMsgElem);

      
        fetch("/ask", {
            method: "POST",
            body: JSON.stringify({ message: userMessage }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            let botMsgElem = document.createElement("p");
            botMsgElem.innerHTML = `<strong>Allora Bot:</strong> ${data.reply}`;
            botMsgElem.style.color = "#007bff";
            chatBody.appendChild(botMsgElem);

           
            setTimeout(() => {
                chatBody.scrollTop = chatBody.scrollHeight;
                sendButton.disabled = false; 
            }, 10);
        })
        .catch(error => {
            console.error("Error:", error);
            let errorElem = document.createElement("p");
            errorElem.innerHTML = `<strong>Allora Bot:</strong> Oops! Something went wrong. Please try again later.`;
            errorElem.style.color = "red";
            chatBody.appendChild(errorElem);
            sendButton.disabled = false;  
        });

        
        chatInput.value = "";
        chatInput.focus();
    }

    
    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });

    
    window.toggleChat = function() {
        chatContainer.style.display = chatContainer.style.display === "none" ? "block" : "none";
        chatIcon.style.display = chatContainer.style.display === "none" ? "flex" : "none";
    };
});