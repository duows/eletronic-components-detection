import os
import json
# import random # No longer needed for simulation
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import cv2 # OpenCV for image processing
from ultralytics import YOLO # Import YOLO from ultralytics

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
COMPONENT_DATA_FILE = 'components.json'
# !!! IMPORTANTE: Coloque o caminho para o seu arquivo de modelo .pt aqui !!!
# Caminho atualizado conforme fornecido pelo usuário, relativo à pasta do app.py
MODEL_PATH = 'treino_integrador_v4_yolov10s2/weights/best.pt' 
CONFIDENCE_THRESHOLD = 0.7 # Definir o limite de confiança aqui

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.secret_key = "supersecretkey"

# --- Load YOLO Model ---
# Carregue o modelo uma vez quando o aplicativo iniciar para melhor desempenho
try:
    model = YOLO(MODEL_PATH)
    print(f"Modelo YOLO carregado de: {MODEL_PATH}")
except Exception as e:
    print(f"Erro ao carregar o modelo YOLO de {MODEL_PATH}: {e}")
    print("Certifique-se de que o MODEL_PATH está correto e o arquivo do modelo existe.")
    model = None # Defina como None se não puder carregar

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_component_data():
    """Loads component data from the JSON file."""
    try:
        with open(COMPONENT_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {COMPONENT_DATA_FILE} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {COMPONENT_DATA_FILE}.")
        return {}

# --- YOLO Real Processing & Image Drawing ---
def process_image_with_yolo(image_path, output_path):
    """
    Processes an image using the loaded YOLO model, draws bounding boxes for detections
    above the confidence threshold, and returns detected component keys and the path
    to the processed image (or original path if processing/saving fails).
    """
    if model is None:
        print("Modelo YOLO não está carregado. Retornando imagem original.")
        return [], image_path 

    try:
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            print(f"Erro: Não foi possível ler a imagem em {image_path}")
            return [], image_path

        img_to_save = img_cv.copy()
        detected_keys = []

        results = model(image_path) 
        
        if results and results[0].boxes:
            boxes = results[0].boxes.xyxy.cpu().numpy() 
            confs = results[0].boxes.conf.cpu().numpy()  
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int) 
            class_names_map = model.names

            for i in range(len(boxes)):
                confidence = confs[i]
                
                if confidence >= CONFIDENCE_THRESHOLD:
                    x1, y1, x2, y2 = map(int, boxes[i])
                    class_id = class_ids[i]
                    component_key = class_names_map.get(class_id, f"Classe_{class_id}")
                    
                    detected_keys.append(component_key) 

                    label = f"{component_key}: {confidence:.2f}"
                    cv2.rectangle(img_to_save, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                    text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20 
                    cv2.putText(img_to_save, label, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        write_success = cv2.imwrite(output_path, img_to_save)
        if not write_success:
            print(f"Erro: Falha ao salvar a imagem processada em {output_path}. Retornando original.")
            return list(set(detected_keys)), image_path
        
        return list(set(detected_keys)), output_path

    except Exception as e:
        print(f"Erro durante o processamento YOLO ou desenho: {e}")
        return [], image_path

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
            
            file.save(original_image_path)

            processed_filename = "processed_" + filename
            processed_image_output_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)

            detected_keys, returned_file_location = process_image_with_yolo(original_image_path, processed_image_output_path)
            
            display_image_static_path = None

            if returned_file_location == processed_image_output_path:
                if os.path.exists(processed_image_output_path):
                    folder_name_for_url = os.path.basename(app.config['PROCESSED_FOLDER']) 
                    display_image_static_path = f"{folder_name_for_url}/{processed_filename}"
                else:
                    print(f"Aviso: Imagem processada ({processed_image_output_path}) não encontrada no disco, embora o processamento tenha indicado sucesso. Exibindo original.")
                    if os.path.exists(original_image_path):
                        folder_name_for_url = os.path.basename(app.config['UPLOAD_FOLDER']) 
                        display_image_static_path = f"{folder_name_for_url}/{filename}"
                    else:
                        flash("Erro crítico: Imagem original também não encontrada.")
            elif returned_file_location == original_image_path: 
                print("Aviso: Processamento YOLO retornou caminho da imagem original. Exibindo imagem original.")
                if os.path.exists(original_image_path):
                    folder_name_for_url = os.path.basename(app.config['UPLOAD_FOLDER']) 
                    display_image_static_path = f"{folder_name_for_url}/{filename}"
                else:
                    flash("Erro crítico: Imagem original não encontrada.")
            else: 
                flash("Erro inesperado ao determinar o caminho da imagem para exibição.")


            all_component_data = load_component_data()
            detected_components_info = []
            
            if display_image_static_path and display_image_static_path.startswith(os.path.basename(app.config['PROCESSED_FOLDER']) + '/'):
                if all_component_data:
                    for key in detected_keys: 
                        if key in all_component_data:
                            detected_components_info.append(all_component_data[key])
                        else:
                            print(f"Aviso: Chave '{key}' (confiança >= {CONFIDENCE_THRESHOLD}) detectada pelo modelo YOLO mas não encontrada em {COMPONENT_DATA_FILE}.")
            
            # LINHA DE DEPURAÇÃO ADICIONADA ABAIXO
            print(f"DEBUG: Tentando renderizar com processed_image_path = '{display_image_static_path}'") 
            
            return render_template('index.html', 
                                   processed_image_path=display_image_static_path,
                                   detected_components_info=detected_components_info)
        else:
            flash('Tipo de arquivo não permitido. Use PNG, JPG ou JPEG.')
            return redirect(request.url)

    return render_template('index.html', processed_image_path=None, detected_components_info=None)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
