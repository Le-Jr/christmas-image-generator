# 🎅 Gerador de Fotos com Papai Noel

Uma aplicação web mágica que permite criar fotos personalizadas ao lado do Papai Noel usando Inteligência Artificial! Perfeito para criar lembranças especiais de Natal.

## ✨ Funcionalidades

- 📸 **Upload de Foto**: Envie sua foto para aparecer ao lado do Papai Noel
- 🎨 **Geração com IA**: Usa Replicate AI Avatars para criar imagens realistas
- 💬 **Mensagem Personalizada**: Recebe uma mensagem única do Papai Noel via Groq (Llama 3.1)
- 🎁 **Personalização**: Informe seu nome, sentimento e presente desejado
- 👤 **Seleção de Gênero**: Escolha sua representação (masculino/feminino)
- 📥 **Download**: Baixe sua foto de Natal personalizada
- ⏳ **Loading Animado**: Mensagens festivas enquanto a IA trabalha

## 🛠️ Tecnologias Utilizadas

### Backend

- **Flask** - Framework web Python
- **Groq API** - Geração de mensagens com Llama 3.1
- **Replicate API** - Geração de imagens (modelo: easel/ai-avatars)
- **Python 3.x**

### Frontend

- HTML5
- CSS3 com animações
- JavaScript (Vanilla)
- Font: Mountains of Christmas (Google Fonts)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no [Groq](https://groq.com/) (para API key)
- Conta no [Replicate](https://replicate.com/) (para API token)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd projeto-papai-noel
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install flask groq replicate python-dotenv
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_groq_aqui
REPLICATE_API_TOKEN=seu_token_replicate_aqui
```

**Como obter as chaves:**

- **Groq API Key**: Cadastre-se em [console.groq.com](https://console.groq.com/)
- **Replicate Token**: Cadastre-se em [replicate.com](https://replicate.com/) e acesse Account Settings

### 5. Estrutura de pastas

```
projeto-papai-noel/
│
├── app.py                 # Aplicação Flask principal
├── .env                   # Variáveis de ambiente (não commitar!)
├── requirements.txt       # Dependências Python
│
├── templates/
│   └── index.html        # Template HTML
│
└── static/
    ├── style.css         # Estilos CSS
    └── script.js         # JavaScript do frontend
```

## ▶️ Como Executar

1. Ative o ambiente virtual (se não estiver ativo)
2. Execute a aplicação:

```bash
python app.py
```

3. Acesse no navegador:

```
http://localhost:5000
```

## 📝 Como Usar

1. **Envie sua foto** - Escolha uma foto clara do seu rosto
2. **Preencha os dados**:
   - Nome
   - Gênero (masculino/feminino/prefiro não informar)
   - Como você está se sentindo
   - Qual presente você deseja
3. **Clique em "Gerar minha foto 🎄"**
4. **Aguarde a mágica acontecer** (pode levar 30-60 segundos)
5. **Baixe sua foto** e compartilhe! 🎅

## 🎨 Personalização

### Modificar o Prompt de Geração

No arquivo `app.py`, localize a variável `image_prompt` (linha ~153):

```python
image_prompt = f"""
A realistic Christmas photo with two people.
# Personalize aqui...
"""
```

### Ajustar Mensagens do Papai Noel

Modifique o `system prompt` na função `generate_message()` (linha ~113):

```python
"content": "You are Santa Claus. Write warm, short Christmas messages..."
```

### Alterar Animações de Loading

No arquivo `static/script.js`, edite o array `loadingMessages` (linha ~12):

```javascript
const loadingMessages = [
  "🎅 O Papai Noel está preparando tudo...",
  // Adicione mais mensagens aqui
];
```

## ⚙️ Configurações Avançadas

### Modelo de IA (Replicate)

O projeto usa `easel/ai-avatars` por padrão. Para usar outro modelo:

```python
output = replicate.run(
    "seu-modelo-aqui",
    input={...}
)
```

### Parâmetros de Geração

Ajuste no código:

- `workflow_type`: "HyperRealistic-likeness" para mais realismo
- `user_gender`: Controla a representação de gênero

## 🐛 Solução de Problemas

### Erro: "API Key não encontrada"

- Verifique se o arquivo `.env` existe e contém as chaves corretas
- Reinicie a aplicação após criar/modificar o `.env`

### Erro: "Erro ao gerar imagem"

- Verifique se seu token Replicate tem créditos
- Confirme que a API está acessível
- Veja os logs no console para detalhes

### Imagem demora muito

- A geração pode levar 30-60 segundos (é normal!)
- Modelos de IA precisam de tempo para processar

### Foto não fica boa

- Use fotos claras, bem iluminadas
- Evite fotos com múltiplas pessoas
- Prefira fotos frontais do rosto

## 📦 Dependências

```txt
flask
groq
replicate
python-dotenv
```

Crie um arquivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## 🔒 Segurança

- **Nunca commite** o arquivo `.env` com suas chaves
- Adicione `.env` ao `.gitignore`
- Use variáveis de ambiente em produção
- Considere rate limiting para APIs públicas

## 📄 Licença

Este projeto é de código aberto para fins educacionais e pessoais.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📧 Contato

Se tiver dúvidas ou sugestões, abra uma issue no repositório!

---

**Feito com ❤️ e magia de Natal 🎄**

_Ho ho ho! Feliz Natal! 🎅_
