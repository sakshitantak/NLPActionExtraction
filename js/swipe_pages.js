var currentPage = 1;
function cardSwitch() {
    switch (currentPage) {
        case 1:
            document.getElementById("tokensOut").style.display = "block";
            document.getElementById("testCaseOut").style.display = "none";
            break;
        case 2:
            document.getElementById("tokensOut").style.display = "none";
            document.getElementById("testCaseOut").style.display = "block";
            break;
        default:
            break;
    }
}

function increasePage() {
    if (currentPage < 2)
        currentPage++;
    cardSwitch();
}

function decreasePage() {
    if (currentPage > 1)
        currentPage--;
    cardSwitch();
}

cardSwitch();