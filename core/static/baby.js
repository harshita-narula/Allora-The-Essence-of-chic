document.getElementById("signin-btn").addEventListener("click", function () {
    document.getElementById("signin-modal").style.display = "block";
});


document.querySelector(".close-btn").addEventListener("click", function () {
    document.getElementById("signin-modal").style.display = "none";
});


window.addEventListener("click", function (event) {
    if (event.target === document.getElementById("signin-modal")) {
        document.getElementById("signin-modal").style.display = "none";
    }
});

document.getElementById("voice-search").addEventListener("click", function () {
    const searchBox = document.querySelector(".search-box input");

    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Your browser does not support voice search.");
        return;
    }

    
    const recognition = new SpeechRecognition();

    recognition.lang = "en-US"; 
    recognition.interimResults = false; 
    recognition.maxAlternatives = 1; 

    
    recognition.start();

    recognition.onstart = function () {
        console.log("Listening...");
        searchBox.placeholder = "Listening...";
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript; 
        console.log("You said:", transcript);
        searchBox.value = transcript; 
        searchBox.placeholder = "Search for Allora";

        
        fetch('/save_voice_input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ search_text: transcript })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log("Voice input saved successfully!");
            }
        })
        .catch(error => {
            console.error("Error sending data to the backend:", error);
        });
    };

    recognition.onerror = function (event) {
        console.error("Error:", event.error);
        alert("Voice search error: " + event.error);
        searchBox.placeholder = "Search for Allora";
    };

    recognition.onend = function () {
        console.log("Stopped listening.");
        searchBox.placeholder = "Search for Allora"; 
    };
});

document.getElementById("image-capture").addEventListener("click", function () {
const fileInput = document.createElement("input");
fileInput.type = "file";
fileInput.accept = "image/*";
fileInput.onchange = async (event) => {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append("image", file);

        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (response.ok) {
            alert(`Image uploaded successfully! Filename: ${result.filename}`);
        } else {
            alert("Error: " + result.error);
        }
    }
};
fileInput.click();
});

document.addEventListener("DOMContentLoaded", function () {
const placeholderTexts = [
    "Search for Allora",
    "Search for Makeup",
    "Search for Haircare",
    "Search for Skincare",
    "Search for Appliances",
    "Search for Bath & Body",
    "Search for Natural",
    "Search for Mom & Baby",
    "Search for Men",
    "Search for Health & Awareness",
    "Search for Lingerie & Accessories",
    "Search for Fragrance",
];

let currentIndex = 0;
const searchInput = document.getElementById("search-input");

setInterval(() => {
    currentIndex = (currentIndex + 1) % placeholderTexts.length; 
    searchInput.setAttribute("placeholder", placeholderTexts[currentIndex]); 
}, 2000);
});


document.getElementById("qr-scanner").addEventListener("click", function () {
    alert("QR Scanner functionality is under development!");
    
});


<button id="scrollToTop" class="scroll-top">↑</button>

const scrollToTopBtn = document.getElementById("scrollToTop");

window.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
};

scrollToTopBtn.addEventListener("click", function() {
    window.scrollTo({ top: 0, behavior: "smooth" });
});