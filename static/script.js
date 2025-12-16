document.getElementById("form").addEventListener("submit", function (e) {
  e.preventDefault();

  // Mostra loading com animação
  const loadingEl = document.getElementById("loading");
  const resultEl = document.getElementById("result");

  loadingEl.style.display = "block";
  resultEl.style.display = "none";

  // Array de mensagens festivas que vão mudando
  const loadingMessages = [
    "🎅 O Papai Noel está preparando tudo...",
    "✨ Adicionando magia de Natal...",
    "🎄 Decorando a cena com luzes...",
    "⭐ Criando sua foto especial...",
    "🎁 Quase pronto, só mais um toque final...",
    "❄️ Adicionando neve mágica...",
    "🔔 Ouvindo os sinos de Natal...",
  ];

  let messageIndex = 0;
  const loadingText = document.getElementById("loading-text");

  // Muda a mensagem a cada 3 segundos
  const messageInterval = setInterval(() => {
    messageIndex = (messageIndex + 1) % loadingMessages.length;
    loadingText.style.opacity = "0";

    setTimeout(() => {
      loadingText.textContent = loadingMessages[messageIndex];
      loadingText.style.opacity = "1";
    }, 300);
  }, 3000);

  const formData = new FormData(this);

  fetch("/generate", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro na resposta do servidor");
      }
      return response.json();
    })
    .then((data) => {
      // Para o intervalo de mensagens
      clearInterval(messageInterval);

      if (data.success) {
        // Esconde loading com fade out
        loadingEl.style.opacity = "0";
        setTimeout(() => {
          loadingEl.style.display = "none";
          loadingEl.style.opacity = "1";
        }, 500);

        // Mostra resultado com fade in
        document.getElementById("generated-image").src = data.image;
        document.getElementById("message").innerText = data.message;

        // Configura botão de download
        const downloadBtn = document.getElementById("download-btn");
        downloadBtn.onclick = function () {
          downloadImage(data.image, "foto-natal-papai-noel.jpg");
        };

        resultEl.style.display = "block";
        resultEl.style.opacity = "0";
        setTimeout(() => {
          resultEl.style.opacity = "1";
        }, 100);

        // Scroll suave até o resultado
        resultEl.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        throw new Error(data.error || "Erro desconhecido");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      clearInterval(messageInterval);

      loadingEl.style.display = "none";

      // Mensagem de erro personalizada
      alert(
        "🎅 Ops! O Papai Noel teve um problema técnico. Tente novamente!\n\nErro: " +
          error.message
      );
    });
});

// Função para baixar a imagem
function downloadImage(imageUrl, filename) {
  // Mostra feedback visual
  const btn = document.getElementById("download-btn");
  const originalText = btn.textContent;
  btn.textContent = "⏳ Baixando...";
  btn.disabled = true;

  fetch(imageUrl)
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Restaura botão com feedback de sucesso
      btn.textContent = "✅ Baixado!";
      setTimeout(() => {
        btn.textContent = originalText;
        btn.disabled = false;
      }, 2000);
    })
    .catch((error) => {
      console.error("Erro ao baixar:", error);
      btn.textContent = "❌ Erro ao baixar";
      setTimeout(() => {
        btn.textContent = originalText;
        btn.disabled = false;
      }, 2000);
    });
}
