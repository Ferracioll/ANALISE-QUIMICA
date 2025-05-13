from flask import Flask, request, jsonify, render_template  # Adicionando o render_template aqui
from flask_cors import CORS
import google.generativeai as genai
import os
import cv2

app = Flask(__name__)
CORS(app)

# Substitua pela chave real da API do Gemini
GOOGLE_API_KEY = "AIzaSyCtcWSk4cdtJAfaJYUB8grGg3lqzxtTfRc"
genai.configure(api_key=GOOGLE_API_KEY)

gemini_disponivel = True if GOOGLE_API_KEY else False
if not gemini_disponivel:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
else:
    print("Chave de API do Gemini configurada com sucesso.")

# Função para analisar a imagem e reconhecer a estrutura (usando OpenCV, por exemplo)
def reconhecer_estrutura_quimica(imagem):
    # Aqui você pode usar alguma técnica ou modelo para detectar a estrutura química na imagem.
    # Este exemplo está simplificado, pois a detecção de moléculas em imagens é uma tarefa avançada.
    
    # Exemplo de nome fictício de molécula (substitua pela lógica real de processamento de imagem)
    nome_molecula = "Benzeno"
    
    return nome_molecula

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o arquivo index.html

@app.route('/identificar_estrutura', methods=['POST'])
def identificar_estrutura_endpoint():
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem fornecida'}), 400
    
    imagem = request.files['imagem']
    if imagem.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400

    if gemini_disponivel:
        try:
            # Passo 1: Reconhecer a estrutura química a partir da imagem
            nome_molecula = reconhecer_estrutura_quimica(imagem)
            print(f"Molécula reconhecida: {nome_molecula}")
            
            # Passo 2: Enviar o nome da molécula para o modelo Gemini para mais informações
            prompt = f"Qual é a molécula '{nome_molecula}'? Forneça o nome completo da molécula, sua fórmula molecular e outros detalhes importantes."

            response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
            texto_gerado = response.text.strip()

            # Passo 3: Retornar a resposta para o usuário
            return jsonify({'resultado': texto_gerado})

        except Exception as e:
            erro = f"Erro ao identificar a estrutura ou gerar a resposta com o Gemini: {e}"
            print(f"Detalhes do erro: {e}")
            return jsonify({'erro': 'Ocorreu um erro ao identificar a estrutura química ou gerar a resposta.'}), 500
    else:
        return jsonify({'erro': 'Gemini não está disponível.'}), 503

if __name__ == "__main__":
    app.run(debug=True)
