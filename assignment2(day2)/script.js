const evalData = [
    {
        query: "How do I reset my SmartHome X1?",
        noRag: "Generic advice: 'Hold reset button with paperclip.'",
        rag: "Hold 'Pair' button for 15s until LED is solid blue.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "Standalone guessed button type wrongly."
    },
    {
        query: "What is the battery life of the wireless camera?",
        noRag: "Typically 2-6 months depending on usage.",
        rag: "4-6 months (at 5 events per day usage profile).",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "RAG provided specific usage context."
    },
    {
        query: "Does the SmartHome X1 support Zigbee 3.0?",
        noRag: "Likely supports Zigbee and Z-Wave.",
        rag: "Explicitly supports Zigbee 3.0 and Thread.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "Standalone was non-committal/uncertain."
    },
    {
        query: "How do I set up a 'Coming Home' routine?",
        noRag: "Create routine in app; name it 'Coming Home'.",
        rag: "Enable Geofencing in Settings > Locations first.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "RAG caught the mandatory pre-requisite."
    },
    {
        query: "What are the power requirements for the Hub Pro?",
        noRag: "Guess: 5V USB adapter (Micro-USB/Type-C).",
        rag: "Requires 12V 2A DC input.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "Standalone guessed wrong voltage."
    },
    {
        query: "Can I connect the system to a 5GHz Wi-Fi?",
        noRag: "Yes, supports both 2.4GHz and 5GHz bands.",
        rag: "No, 2.4GHz only for stability reasons.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "Standalone hallucinated dual-band support."
    },
    {
        query: "LED is flashing red 3 times. What does it mean?",
        noRag: "General error, low battery, or lost connection.",
        rag: "Authentication Failed (Admin password check).",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "RAG mapped the exact error code."
    },
    {
        query: "How does 'End-to-End Encryption' work?",
        noRag: "Uses standard AES or SSL protocols.",
        rag: "AES-256 (local) and TLS 1.3 (cloud).",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "RAG gave exact protocol versions."
    },
    {
        query: "Which 3rd-party bulbs are compatible?",
        noRag: "Likely Philips Hue and TP-Link Tradfri.",
        rag: "Philips Hue (Bridge req) and LIFX (Direct).",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "RAG identified Bridge requirement."
    },
    {
        query: "Way to backup automation settings locally?",
        noRag: "Check app's settings or advanced menu.",
        rag: "Export .shx1 via web portal only.",
        rel: 5,
        faith: 5,
        halluc: "No",
        notes: "Standalone misled user to mobile app."
    }
];

function getScoreClass(score) {
    if (score >= 4) return 'score-high';
    if (score >= 3) return 'score-mid';
    return 'score-low';
}

function renderTable() {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    evalData.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.style.animationDelay = `${index * 0.1}s`;
        tr.classList.add('fadeInUp');

        tr.innerHTML = `
            <td class="query-text">${item.query}</td>
            <td>
                <div class="response-box no-rag-box"><strong>No RAG:</strong> ${item.noRag}</div>
                <div class="response-box rag-box"><strong>RAG:</strong> ${item.rag}</div>
            </td>
            <td><span class="score-badge ${getScoreClass(item.rel)}">${item.rel}</span></td>
            <td><span class="score-badge ${getScoreClass(item.faith)}">${item.faith}</span></td>
            <td><span class="halluc-${item.halluc.toLowerCase()}">${item.halluc}</span></td>
            <td class="notes-cell">${item.notes}</td>
        `;
        tbody.appendChild(tr);
    });
}

document.addEventListener('DOMContentLoaded', renderTable);
