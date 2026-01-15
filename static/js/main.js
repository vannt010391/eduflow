// EduFlow AI - Main JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Timer functionality for focus sessions
let timerInterval = null;
let startTime = null;

function startTimer(duration) {
    startTime = new Date();
    const endTime = new Date(startTime.getTime() + duration * 60000);

    timerInterval = setInterval(function() {
        const now = new Date();
        const remaining = Math.max(0, endTime - now);

        if (remaining === 0) {
            clearInterval(timerInterval);
            playNotification();
            alert('Time is up! Great work!');
            return;
        }

        const minutes = Math.floor(remaining / 60000);
        const seconds = Math.floor((remaining % 60000) / 1000);

        const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        const timerElement = document.getElementById('timer-display');
        if (timerElement) {
            timerElement.textContent = display;
        }
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function playNotification() {
    // Simple notification sound (browser beep)
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGGe56+abSQwPTqXh8LlnHwU7k9jzzXksBSh+zPLajjwJFF3z6+aoUw0ISZ3d8r9uIgUuhc/y2os5CRllue7mnkwND0+m4PG8aCAFOZPX88t2KgUofM3y2YA4CRNc8+vmpVQOCE2j3/OxbSAFMIPL8N+ROAUVW/Ps56JTDghNouDzsW0gBTCFy/DdkzcFFVvz6+aaTA8OT6bg8bxoHgU7k9jzzXgrBSh+zPLdjjsJFVz06uijVRQLSZ3e88BuIQUug8/y2Yk3CBhov+77n04ODFCB4/C3YhcFO5PY88x4KgQpf87y2I87CRVb9OvmonVTDQhNouDzsWofBTCFy/DdkTkFFVvz7OaaTQwPT6Xh8LplHgU7lNjzy3kvBCh+yPLaizsJFVz06uikVRULSZ3e8r5vIgUvgsny1ok2BxloveznmkwND0+m4fC4Zh0GOpTX88t0KwUqfszy2I09CRRd9OvmpFQOCUqd3vK+biMFL4PJ8taJNgcZaL3s55lLDQ9Pptz0t2YeBjuV1/PMcisGKn3M8tmNPAkTXfTr5qRUDglKnd7yvmwiBS+DyfLWiTYHGWi97OaZSw0PT6Xg8LlmHQY7ldjzznIsBC+CyPLXiTYHGWi87OeaTA0OTqXh8LlmHgU7lNjzzXgrBSp+zPLZjTwJE132aueYSAwPT6Xg8LloHgU7lNjzy3IrBSp9zPLZjTwJFF3z6+aaTA8OT6Xg8bxnHgU7k9jzzXgrBSl+zPLajjsJFVzz6+aiVQ4JTaPf87FtIAUyhMvw3Y85CBVb8+znoVMLCEyd3vO/biEFLoXP8tuLOQgZZ7nu5p9MDhBOpN/yvWcdBTmT2PPNeCoFKX7M8tqNOwkVXPPr5qJVDglNo9/zsW0gBTGEy/DejzkIFVvz7OajVA0ITqPg87BqHgU5k9fzzHkqBSh9zPLajzoJFV3z6+ejUw0ITaPf8rBqHgU5k9fzzHkqBSh9zPLajjoJFVvz6+ejUw0ITaPf8rFtHwU5k9fzzHkqBSh9zPLajjoJFVvz6+ejUw0ITaPf8rFtHwU5k9fzzHkqBSh9zPLajjoJFVvz6+ejUw0ITaPf8rFtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0IT6Pf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fzzHkqBSh9zPLajjoJFV3z6+ejUw0ITaPf87FtHwU5k9fz');
    audio.play().catch(e => console.log('Could not play notification sound'));
}

// Confirmation dialogs
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Chart.js integration (if needed for analytics)
function createChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
