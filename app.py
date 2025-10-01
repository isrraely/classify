import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from google import genai
from google.genai import types

load_dotenv()

try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(
        f"Aviso: Chave Gemini não carregada corretamente ou erro de inicialização: {e}"
    )

app = Flask(__name__)


def classificar_e_responder_ia(email_content):
    """
    Função que chama a API do Gemini para classificação e geração de resposta em JSON.
    """
    if not email_content.strip():
        return {
            "categoria": "Atenção",
            "resposta_sugerida": "Conteúdo do e-mail vazio.",
        }

    system_prompt = f"""
    Você é um assistente de classificação e resposta de emails para The BatCoin. 
    Sua tarefa é analisar o email abaixo e classificá-lo estritamente em uma das duas categorias: 
    'Produtivo' ( Emails que requerem uma ação ou resposta específica: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema) ou 'Improdutivo' (Emails que não necessitam de uma ação imediata: mensagens de felicitações, agradecimentos).

    **Instruções de Saída:** Sua resposta DEVE ser um bloco JSON estrito com as chaves:
    - resumo_executivo: (Um resumo conciso de 1 a 2 frases sobre o conteúdo principal do e-mail.)
    - categoria: ('Produtivo' ou 'Improdutivo')
    - resposta_sugerida: (A resposta automática completa e profissional em português. Se 'Produtivo', prometa acompanhamento. Se 'Improdutivo', apenas agradeça.)

    **EMAIL PARA ANÁLISE:**
    ---
    {email_content}
    ---
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        json_output = json.loads(response.text)
        return {
            "resumo_executivo": json_output.get(
                "resumo_executivo", "Falha ao gerar resumo."
            ),
            "categoria": json_output.get("categoria", "Falha de Classificação"),
            "resposta_sugerida": json_output.get(
                "resposta_sugerida", "Não foi possível gerar a resposta."
            ),
        }, email_content

    except Exception as e:
        return {
            "resumo_executivo": "Erro de processamento.",
            "categoria": "Erro de API Gemini",
            "resposta_sugerida": f"Erro ao processar com IA: {e}",
        }, email_content


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", resultado=None)


@app.route("/upload", methods=["POST"])
def upload():
    email_content = ""

    email_content = request.form.get("mail_body", "")

    uploaded_file = request.files.get("file")

    if uploaded_file and uploaded_file.filename != "":
        filename = uploaded_file.filename

        try:
            if filename.lower().endswith(".pdf"):
                reader = PdfReader(uploaded_file.stream)
                text = ""
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"

                email_content = text if text.strip() else "PDF vazio ou ilegível."

            else:
                file_contents = uploaded_file.read()

                try:
                    email_content = file_contents.decode("utf-8")
                except UnicodeDecodeError:
                    email_content = file_contents.decode("latin-1")

        except Exception as e:
            return render_template(
                "index.html",
                resultado={
                    "categoria": "Erro de Leitura",
                    "resposta_sugerida": f"Não foi possível processar o arquivo. Detalhes: {e}",
                    "conteudo_enviado": "Erro ao ler dados binários, não foi possível exibir o conteúdo.",
                },
            )

    resultado_ia, conteudo_original = classificar_e_responder_ia(email_content)

    resultado_ia["conteudo_enviado"] = conteudo_original

    return render_template("index.html", resultado=resultado_ia)


if __name__ == "__main__":
    app.run(debug=True)
