document.addEventListener("DOMContentLoaded", function() {
    function additional() {
        var category = document.getElementById("category").value;
        var lostindexInput = document.getElementById("lostindex");
        var lostdescInput = document.getElementById("lostdesc");
        var lostname = document.getElementById("name");
        
        if (category === "ID") {
            lostindexInput.parentElement.style.display = "block";
            lostdescInput.parentElement.style.display = "none";
            lostname.parentElement.style.display = "none";
        } else {
            lostindexInput.parentElement.style.display = "none";
            lostdescInput.parentElement.style.display = "block";
            lostname.parentElement.style.display = "block";
        }
    }

    // Call additional() initially to set the correct visibility
    additional();

    // Add event listener for the category select element
    document.getElementById("category").addEventListener("change", additional);
});