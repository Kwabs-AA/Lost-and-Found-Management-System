document.addEventListener("DOMContentLoaded", function() {
    function additional() {
        var category = document.getElementById("category").value;
        var lostindexInput = document.getElementById("lostindex");
        var lostdescInput = document.getElementById("lostdesc");
        var lostname = document.getElementById("name");

        if (category === "ID") {
            lostindexInput.style.display = "block";
            lostdescInput.style.display = "none";
            lostname.style.display = "none";
        } else if (category === "") {
            alert("please choose a category");
        } else {
            lostindexInput.style.display = "none";
            lostdescInput.style.display = "block";
            lostname.style.display = "block";
        }
    }

    // Call additional() initially to set the correct visibility
    additional();

    // Add event listener for the category select element
    document.getElementById("category").addEventListener("change", additional);
});
