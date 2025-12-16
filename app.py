from flask import Flask, render_template, request, jsonify
import os
import base64
from groq import Groq
import replicate
import tempfile
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configura token do Replicate explicitamente
replicate_token = os.environ.get("REPLICATE_API_TOKEN")
if replicate_token:
    os.environ["REPLICATE_API_TOKEN"] = replicate_token

# Inicializa clientes
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_image(photo_bytes, prompt):
    """
    Gera imagem usando Replicate com Stable Diffusion
    """
    try:
        print("🎨 Iniciando geração de imagem...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Configura cliente Replicate com token explícito
        api_token = os.environ.get("REPLICATE_API_TOKEN")
        print(f"🔑 Token presente: {bool(api_token)}")
        
        replicate_client = replicate.Client(api_token=api_token)
        
        # Salva imagem temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(photo_bytes)
            tmp_path = tmp_file.name
        
        print(f"📁 Imagem temporária salva em: {tmp_path}")
        
        # Abre e converte para base64
        with open(tmp_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode()
        
        print(f"📦 Imagem convertida para base64 ({len(image_data)} chars)")
        print("🚀 Enviando para Replicate...")
        
        # Chama Replicate SDXL com image-to-image usando o cliente
        # output = replicate_client.run(
        #     # "instantx/instantid",
        #     # "fermatresearch/sdxl-controlnet-lora:3bb13fe1c33c35987b33792b01b71ed6529d03f165d1c2416375859f09ca9fef",
        #     "runwayml/gen4-image",
        #     input={
        #         "image": f"data:image/jpeg;base64,{image_data}",
        #         "prompt": prompt,
        #         "strength": 0.3,
        #         "num_inference_steps": 30,
        #         "guidance_scale": 7.5,
        #         "negative_prompt": "distorted face, deformed face, extra limbs, bad anatomy,blurry, abstract, ugly, cartoon, low quality, mutation",
        #         "width": 1024,
        #         "height": 1024
        #     }
        # )
        
        gender_map = {
            "masculino": "male",
            "feminino": "female",
            "nao_informar": "male"  # default neutro
        }

        user_gender = gender_map.get(request.form.get("gender"), "male")
        
        output = replicate.run(
            "easel/ai-avatars",
            input={
                "prompt": prompt,
                "face_image": f"data:image/jpeg;base64,{image_data}",
                "face_image_b": f"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRl46U3rcLFrUTeVNfbN8ZeE4jKiE4psQWoNg&s",
                "user_gender": user_gender,  # ou "female"
                # "user_gender": "male",
                "user_b_gender": "male",
                "workflow_type": "HyperRealistic-likeness"
            }
        )

        
        print("✅ Imagem gerada com sucesso!")
        
        # Remove arquivo temporário
        os.unlink(tmp_path)
        
        # Converte output para string (URL)
        # O Replicate pode retornar FileOutput, lista ou string
        if isinstance(output, list):
            result = str(output[0])
        else:
            result = str(output)
        
        print(f"🖼️ URL da imagem: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {type(e).__name__}")
        print(f"📋 Detalhes: {e}")
        import traceback
        traceback.print_exc()
        # Retorna imagem placeholder em caso de erro
        return "https://via.placeholder.com/512x512/c41e3a/ffffff?text=Erro+ao+gerar+imagem"

def generate_message(name, feeling, gift):
    """
    Gera mensagem do Papai Noel usando Groq (Llama)
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Santa Claus. Write warm, short Christmas messages in Portuguese (Brazil). Be cozy, kind, and slightly playful. Use 2-3 sentences maximum. No emojis."
                },
                {
                    "role": "user",
                    "content": f"Escreva uma mensagem curta de Natal para {name}. A pessoa está se sentindo {feeling} e pediu de presente {gift}."
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.8,
            max_tokens=150
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Erro ao gerar mensagem: {e}")
        return f"Ho ho ho, {name}! O Papai Noel está muito feliz em saber que você pediu {gift}. Continue sendo uma pessoa maravilhosa! Feliz Natal! 🎅"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Recebe dados do formulário
        name = request.form.get('name', 'amigo(a)')
        feeling = request.form.get('feeling', 'feliz')
        gift = request.form.get('gift', 'algo especial')
        photo = request.files.get('photo')
        
        if not photo:
            return jsonify({'error': 'Por favor, envie uma foto'}), 400
        
        # Lê bytes da foto
        photo_bytes = photo.read()
        
        gift = request.form.get("gift", "something special")

        image_prompt = f"""
        A realistic Christmas photo with two people.

        Person A:
        A regular person with an average body type.
        Natural proportions, realistic posture.
        Body proportions consistent with the face.
        Wearing casual winter clothes that fit naturally.
        No model-like body, no exaggerated muscles.

        Person B:
        Santa Claus wearing a classic red Santa suit.
        Friendly and smiling.
        Santa Claus is holding a festive Christmas gift box that represents: {gift}.

        They are standing side by side in a cozy Christmas environment.
        Warm Christmas lights, decorated Christmas tree.
        Natural lighting, photorealistic.
        Full body shot.
        """

        
        # Prompt para geração de imagem (exatamente como especificado)
        # image_prompt = (
        #     f"A cozy Christmas photo, warm and festive atmosphere. with {name} "
        #     f"Standing next to Santa Claus, who is friendly and smiling. "
        #     f"The mood is {feeling}. "
        #     f"The scene subtly reflects the idea of a Christmas gift: {gift}. "
        #     "Soft warm Christmas lights, decorated Christmas tree in the background. "
        #     "Realistic photography, natural lighting, high detail. "
        #     "Full body shot."
        # )
        
        # image_prompt = (
        # "A realistic Christmas photo with two people."

        # "Person A:"
        # "A regular person wearing normal winter clothes, modern casual style."

        # "Person B:"
        # "Santa Claus wearing a classic red Santa suit, white beard, friendly and smiling."

        # "They are standing side by side in a cozy Christmas environment."
        # "Warm Christmas lights, decorated Christmas tree."
        # "Natural lighting, photorealistic, high detail."
        # "Full body shot."
        # )
            

    
        # Gera imagem (pode demorar 10-30 segundos)
        generated_image_url = generate_image(photo_bytes, image_prompt)
        
        # Gera mensagem do Papai Noel (rápido, ~1 segundo)
        santa_message = generate_message(name, feeling, gift)
        
        return jsonify({
            'image': generated_image_url,
            'message': santa_message,
            'success': True
        })
        
    except Exception as e:
        print(f"Erro no endpoint /generate: {e}")
        return jsonify({
            'error': f'Erro ao processar: {str(e)}',
            'success': False
        }), 500
        
@app.route("/debug-env")
def debug_env():
    return {
        "replicate_present": bool(os.environ.get("REPLICATE_API_TOKEN")),
        "groq_present": bool(os.environ.get("GROQ_API_KEY")),
        "env_keys": list(os.environ.keys())
    }


if __name__ == '__main__':
    # Verifica se as chaves estão configuradas
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  AVISO: GROQ_API_KEY não encontrada nas variáveis de ambiente")
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("⚠️  AVISO: REPLICATE_API_TOKEN não encontrada nas variáveis de ambiente")
    
    # app.run(debug=True, port=5000)
    app.run(port=5000)