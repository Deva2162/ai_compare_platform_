// document.getElementById('submitBtn').addEventListener('click', async () => {
//     const prompt = document.getElementById('promptInput').value;
//     const submitBtn = document.getElementById('submitBtn');
//     const loading = document.getElementById('loading');
//     const resultsContainer = document.getElementById('resultsContainer');

//     if (!prompt) {
//         alert("Please enter a prompt");
//         return;
//     }

//     // Reset UI
//     resultsContainer.innerHTML = '';
//     submitBtn.disabled = true;
//     loading.classList.remove('hidden');

//     try {
//         const response = await fetch('/ask', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ prompt: prompt }),
//         });

//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         const data = await response.json();
        
//         // Render cards
//         data.forEach(ai => {
//             const card = document.createElement('div');
//             card.className = 'card';
            
//             const fastestBadge = ai.is_fastest ? '<span class="fastest-badge">⚡ Fastest</span>' : '';

//             card.innerHTML = `
//                 <div class="card-header">
//                     <span class="model-name">${ai.model}</span>
//                     <div>
//                         ${fastestBadge}
//                         <span class="response-time">${ai.time}s</span>
//                     </div>
//                 </div>
//                 <div class="response-text">
//                     ${ai.response}
//                 </div>
//             `;
//             resultsContainer.appendChild(card);
//         });

//     } catch (error) {
//         console.error('Error:', error);
//         resultsContainer.innerHTML = `<p style="color:red;">An error occurred while fetching responses. Please try again.</p>`;
//     } finally {
//         submitBtn.disabled = false;
//         loading.classList.add('hidden');
//     }
// });
const submitBtn = document.getElementById("submitBtn");
const promptInput = document.getElementById("promptInput");
const resultsContainer = document.getElementById("resultsContainer");
const loading = document.getElementById("loading");

submitBtn.addEventListener("click", async () => {
    const prompt = promptInput.value;
    if (!prompt) return alert("Enter a prompt");

    loading.classList.remove("hidden");
    resultsContainer.innerHTML = "";

    const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    loading.classList.add("hidden");

    data.forEach(ai => {
        resultsContainer.innerHTML += `
            <div class="card">
                <h2>${ai.model}</h2>
                <p>${ai.response}</p>
                <small>Response Time: ${ai.time}s</small>
            </div>
        `;
    });
});
