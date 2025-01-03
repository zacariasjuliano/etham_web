async function sendMessage() {
    const user_input = document.getElementById("user_input").value;

    const response = await fetch("", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: `user_input=${user_input}`
    });

    const data = await response.json();
    
    // Adiciona a pergunta e a resposta ao chatbox
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p><b>Você:</b> ${user_input}</p>`;
    chatbox.innerHTML += `<p><b>PagaSó:</b> ${data.response}</p>`;

    // Limita o número de mensagens no chatbox (exemplo: 10 perguntas e respostas)
    const maxMessages = 10;
    const messages = chatbox.getElementsByTagName("p");

    if (messages.length > maxMessages * 2) { // Multiplicamos por 2 porque temos pergunta e resposta
        chatbox.removeChild(messages[0]);
        chatbox.removeChild(messages[1]);
    }

    // Limpa o campo de entrada de texto
    document.getElementById("user_input").value = "";
}
