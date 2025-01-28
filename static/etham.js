async function sendMessage() {
    const userInput = document.getElementById("user_input");
    const chatbox = document.getElementById("chatbox");
    const userMessage = userInput.value.trim();

    if (!userMessage) return;

    // Adiciona a mensagem do usuário
    chatbox.innerHTML += `<div class="message user"><b>Você:</b> ${userMessage}</div>`;

    // Limpa o campo de entrada
    userInput.value = "";

    try {
        const response = await fetch("", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `user_input=${encodeURIComponent(userMessage)}`
        });

        if (!response.ok) {
            throw new Error("Erro ao se comunicar com o servidor.");
        }

        const data = await response.json();

        // Adiciona a resposta do bot
        chatbox.innerHTML += `<div class="message bot"><b>PagaSó:</b> ${data.response}</div>`;
    } catch (error) {
        chatbox.innerHTML += `<div class="message bot"><b>PagaSó:</b> Ocorreu um erro, tente novamente.</div>`;
        console.error(error);
    }

    // Rolar automaticamente para a última mensagem
    chatbox.scrollTop = chatbox.scrollHeight;
}
