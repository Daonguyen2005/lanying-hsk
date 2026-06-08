// Script to handle simple mock UI interactions

function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
        chatWindow.style.display = 'flex';
    } else {
        chatWindow.style.display = 'none';
    }
}

function openSurvey() {
    document.getElementById('surveyModal').style.display = 'flex';
}

function closeSurvey() {
    document.getElementById('surveyModal').style.display = 'none';
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('surveyModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
