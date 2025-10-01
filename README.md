# 📧 Classificador Inteligente de E-mails com IA

## 📌 Desafio Técnico
Desenvolver uma solução de software para automatizar a classificação de e-mails recebidos em alto volume para uma empresa do setor financeiro, sugerindo **categorias** e **respostas automáticas**.

---

## 🎯 Objetivo da Solução
O objetivo principal desta aplicação é liberar o tempo da equipe humana através da **automação inteligente**:

1. **Classificação Rígida**: Categorizar e-mails como:
   - **Produtivo** → requer ação/suporte  
   - **Improdutivo** → cortesia/informativo  

2. **Eficiência**: Gerar um **Resumo Executivo** para leitura rápida e uma **Resposta Automática** adequada à categoria.  

3. **Transparência**: Permitir o upload flexível de arquivos (`.txt`, `.pdf`) e exibir o conteúdo analisado.  

---

## 🏛 Arquitetura do Projeto
O projeto utiliza uma arquitetura **Full Stack leve e moderna**, focada em **eficiência** e **IA de ponta**:

| Componente       | Tecnologia                 | Função Principal |
|------------------|----------------------------|------------------|
| **Frontend (UI)** | HTML5, CSS3, JavaScript   | Formulário de entrada, feedback visual (cores dinâmicas, upload) e exibição dos resultados |
| **Backend**       | Python (Flask)            | Roteamento de requisições, upload de arquivos e orquestração da lógica de IA |
| **Pré-processamento** | PyPDF2                 | Extração de texto limpo de PDFs |
| **IA**            | Google Gemini API         | Classificação, resumo e resposta em **uma única chamada de API** |

---

## 💡 Destaques da Implementação
1. **Prompt Engineering e Saída Estruturada**  
   - A comunicação com o Gemini é feita com `system_prompt` rígido (Assistente Financeiro).  
   - Saída em **JSON estruturado**, garantindo confiabilidade.  

2. **Eficiência de Chamada da API**  
   - Classificação, resumo e resposta em **uma só chamada** → menos latência e menor custo.  

3. **Usabilidade (UX)**  
   - Feedback visual imediato no upload.  
   - **Cores dinâmicas**:  
     - 🔴 Vermelho → Produtivo  
     - 🟢 Verde → Improdutivo  

---

## ⚙️ Instruções de Execução

### Pré-requisitos
- Python **3.8+**
- Conta no **Google AI Studio** (para chave Gemini API)

## 1. Configurar o Ambiente

### Navegue até a pasta raiz do projeto
python -m venv venv  

### Ativar ambiente virtual
source venv/bin/activate     # macOS/Linux  
.\venv\Scripts\activate      # Windows  

### Instalar dependências
pip install Flask google-genai python-dotenv PyPDF2  

## 2. Configurar a Chave da API 
Crie o arquivo .env na raiz do projeto e insira:  
GEMINI_API_KEY="SUA_CHAVE_AQUI"  
⚠️ Atenção: nunca suba este arquivo em repositórios públicos.  

# 3. Rodar a Aplicação
python app.py  
O servidor estará acessível em: http://127.0.0.1:5000/

## 🧪 Sugestões de Teste

| Cenário              | Entrada                                                 | Categoria Esperada |
| -------------------- | ------------------------------------------------------- | ------------------ |
| **Ação Crítica**     | E-mail solicitando suporte urgente, bloqueio de sistema | Produtivo 🔴       |
| **Cortesia**         | E-mail de agradecimento ou Feliz Natal                  | Improdutivo 🟢     |
| **Teste de Arquivo** | Upload de `.pdf` ou `.txt` com conteúdo produtivo       | Produtivo 🔴       |

## 👨‍💻 Por Isrraely Curtiz
Desenvolvido como parte de um Desafio Técnico para automação de e-mails no setor financeiro.
