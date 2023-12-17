$(document).ready(function () {



    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        
        $(".siri-message").text(message);
    }
        

    
});