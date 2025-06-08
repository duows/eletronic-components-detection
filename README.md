# 🤖 Reconhecimento de Componentes Eletrônicos em Imagens

## 📖 Sobre o Projeto

Este é um projeto de visão computacional desenvolvido como Trabalho de Projeto Integrador II para o curso de Engenharia da Computação do Instituto Federal de São Paulo (IFSP) - Câmpus Birigui.

A aplicação web permite a detecção e identificação de componentes eletrônicos em imagens. O principal objetivo é servir como uma ferramenta educacional interativa, auxiliando estudantes e entusiastas a aprenderem sobre eletrônica de forma prática e visual. Os usuários podem submeter uma imagem através de upload ou captura direta pela webcam. O sistema então processa a imagem usando um modelo **YOLOv10s** pré-treinado, destaca os componentes detectados e exibe informações detalhadas sobre eles, como nome, função e fórmulas relevantes.

## ✨ Funcionalidades Principais

* **Detecção de Componentes:** Identifica diversos componentes eletrônicos em imagens paradas.
* **Upload de Imagem:** Permite que o usuário envie um arquivo de imagem (JPG, PNG, JPEG) para análise.
* **Captura via Webcam:** Oferece a funcionalidade de capturar uma foto diretamente pela câmera do dispositivo para análise em tempo real.
* **Visualização de Resultados:** Exibe a imagem processada com caixas delimitadoras (*bounding boxes*) e rótulos sobre os componentes identificados.
* **Informações Detalhadas:** Apresenta uma ficha informativa para cada componente detectado com confiança acima de 65%, contendo nome, explicação e fórmulas.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias:

* **Backend:**
    * Python 3.8+
    * Flask
* **Visão Computacional:**
    * YOLOv10s
    * PyTorch
    * OpenCV
* **Gerenciamento de Dados e Anotação:**
    * Roboflow
    * Arquivo `components.json` para dados dos componentes
* **Infraestrutura e Implantação:**
    * Render (para hospedagem da aplicação)
    * Supabase (para banco de dados e autenticação)

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### Pré-requisitos

* Python 3.8 ou superior
* Git

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * No Linux/macOS:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    O projeto utiliza as bibliotecas listadas abaixo. Crie um arquivo `requirements.txt` com o conteúdo a seguir e execute o comando de instalação.

    *Conteúdo do `requirements.txt`:*
    ```
    Flask
    Werkzeug
    opencv-python
    ultralytics
    torch
    torchvision
    torchaudio
    python-dotenv
    supabase-py
    numpy
    ```

    *Comando de instalação:*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Modelo:**
    * Faça o download do arquivo de pesos do modelo treinado (`best.pt`).
    * Assegure-se de que o caminho para o modelo no arquivo `app.py` esteja correto. A variável `MODEL_PATH` deve apontar para o local do seu arquivo `.pt`.
    * Garanta que o arquivo `components.json` esteja na raiz do projeto.

### Execução

1.  **Inicie o servidor Flask:**
    ```bash
    python app.py
    ```

2.  **Acesse a aplicação:**
    Abra seu navegador e acesse o endereço `http://127.0.0.1:5000/`.

## 📈 Status do Projeto

O projeto é uma prova de conceito funcional e foi concluído como requisito acadêmico. O desempenho do modelo de detecção atingiu uma precisão média (mAP50) de **44,80%** no conjunto de validação.

Existem oportunidades para melhorias futuras, como:
* Aumentar a diversidade do dataset com mais imagens únicas.
* Aplicar técnicas de aumento de dados mais avançadas.
* Otimizar as configurações do YOLO para detecção de objetos pequenos.
* Realizar testes de usabilidade com estudantes e professores para validar a eficácia pedagógica.

## 👥 Autores

* **Camila Albieri Mattos**
* **Henrique José de Souza**

O projeto foi desenvolvido sob a orientação do corpo docente do [**Instituto Federal de Educação, Ciência e Tecnologia de São Paulo - Câmpus Birigui**](https://bir.ifsp.edu.br/).
