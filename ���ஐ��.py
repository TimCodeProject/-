from flask import Flask, request, jsonify
import g4f
import g4f.Provider
import base64
import re
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def analyze_image_with_ai(image_data, name, description):
    # Улучшенный промпт для анализа изображения
    prompt = f"""
    Ты - профессиональный психолог, анализирующий рисунки несуществующих животных. 
    Перед тобой рисунок животного "{name}" с описанием: "{description}".
    
    Проведи детальный анализ по следующим критериям:
    
    1. Внешний вид (на что похоже животное):
    - На какие реальные или фантастические существа оно похоже
    - Основные визуальные характеристики
    - Уникальные особенности
    
    2. Психологический анализ:
    а) Расположение на листе:
    - Где расположен рисунок (центр, верх, низ, лево, право)
    - Животное расположено ближе к левому или правому краю?
    Если к правому - взгляд в будущее, надежда на лучшее(в зависимости от контекста), Если к левому - зацикленность на прошлом, неуверенность. 
    - Интерпретация расположения
    
    б) Размер и пропорции:
    - Размер относительно листа
    Крупное - уверенность или эгоцентричность, Мелкое - неуверенность, мелочность. Выходит за рамки - Когнитивный диссонанс, неуровновешенность, отсутствие самоконтроля
    - Пропорции тела
    Голова больше туловища - Тревожность или сосредоточенность на себе. Туловище больше - желание быть сильным.
    - Интерпретация размера
    
    в) Детализация:
    - Уровень проработки деталей
    - Какие элементы особенно выделены
    Украшения - желание выделиться, Предметы - указания на увлечение, творческие способности.
    - Интерпретация детализации
    
    г) Особенности:
    - Наличие агрессивных элементов (острые зубы, когти)
    Желание напасть или защитится
    - Защитные элементы (панцирь, шипы)
    Защитные элементы
    - Компенсаторные элементы (крылья, рога)
    Крылья - желание свободы и независимости, рога - оборона.
    - Эмоциональные признаки (глаза, рот)
    Закрытый рот - антисоциальность, замкнутость, открытый рот - болтливость, нету рта - полное нежелание общаться
    
    3. Анализ названия и описания:
    - Лингвистические особенности названия
    - Ключевые слова в описании
    - Соответствие между рисунком и описанием
    
    4. Психологический портрет:
    - Самооценка и уровень притязаний
    - Эмоциональное состояние
    - Социальные установки
    - Механизмы психологической защиты
    - Когнитивные особенности
    
    Выводы:
    - Основные психологические характеристики
    - Рекомендации (если уместно)
    
    Анализ должен быть конкретным, опираться на визуальные признаки рисунка и данные описания. 
    Избегай общих фраз, делай акцент на уникальных особенностях данного рисунка.
    """
    
    try:
        # Декодируем base64 и сохраняем временное изображение
        image_data = re.sub('^data:image/.+;base64,', '', image_data)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image.save("temp_animal.png", "PNG")
        
        # Основной анализ (Blackbox)
        client = g4f.Client(provider=g4f.Provider.Blackbox)
        images = [[open("temp_animal.png", "rb"), "animal.png"]]
        response = client.chat.completions.create(
            [{"content": prompt, "role": "user"}], 
            "", 
            images=images
        )
        return {'analysis': response.choices[0].message.content}
    except Exception as e:
        return {'error': f"Произошла ошибка при анализе: {str(e)}"}

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data['image']
    name = data['name']
    description = data['description']
    
    result = analyze_image_with_ai(image_data, name, description)
    return jsonify(result)

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НейроРНЖ - Анализ рисунков несуществующих животных</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {
            --primary-color: #e0f7fa;
            --secondary-color: #b2ebf2;
            --accent-color: #80deea;
            --dark-accent: #4dd0e1;
            --text-color: #006064;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--text-color);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(90deg, rgba(224,247,250,0.8), rgba(178,235,242,0.8));
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,96,100,0.1);
        }
        
        h1 {
            margin: 0;
            font-size: 2.5em;
            color: var(--text-color);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
        }
        
        .subtitle {
            font-style: italic;
            margin-top: 10px;
            font-size: 1.2em;
        }
        
        .main-content {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            justify-content: center;
        }
        
        .drawing-section, .info-section {
            flex: 1;
            min-width: 300px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,96,100,0.1);
        }
        
        .canvas-container {
            position: relative;
            margin-bottom: 20px;
        }
        
        #drawingCanvas {
            border: 2px solid var(--dark-accent);
            border-radius: 10px;
            background-color: white;
            cursor: crosshair;
            width: 100%;
            touch-action: none;
        }
        
        .canvas-tools {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .canvas-tools button, #analyzeBtn {
            padding: 8px 15px;
            background: linear-gradient(to bottom, var(--accent-color), var(--dark-accent));
            border: none;
            border-radius: 5px;
            color: var(--text-color);
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,96,100,0.1);
        }
        
        .canvas-tools button:hover, #analyzeBtn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,96,100,0.2);
        }
        
        .canvas-tools button:active, #analyzeBtn:active {
            transform: translateY(0);
        }
        
        input, textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 2px solid var(--accent-color);
            border-radius: 5px;
            font-family: inherit;
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        #resultContainer {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            display: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid var(--dark-accent);
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            font-size: 0.9em;
        }
        
        .camera-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .camera-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            max-width: 90%;
            max-height: 90%;
        }
        
        #cameraPreview {
            max-width: 100%;
            max-height: 60vh;
            margin-bottom: 15px;
        }
        
        .camera-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        
        @media (max-width: 768px) {
            .main-content {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>НейроРНЖ</h1>
            <div class="subtitle">Психологический анализ рисунков несуществующих животных</div>
        </header>
        
        <div class="main-content">
            <section class="drawing-section">
                <h2>Нарисуйте или загрузите животное</h2>
                <div class="canvas-tools">
                    <button id="clearBtn">Очистить</button>
                    <button id="undoBtn">Отменить</button>
                    <input type="color" id="colorPicker" value="#006064">
                    <input type="range" id="brushSize" min="1" max="20" value="5">
                    <button id="cameraBtn">Камера</button>
                    <button id="uploadBtn">Загрузить</button>
                    <button id="saveImageBtn">Сохранить</button>
                    <input type="file" id="fileInput" accept="image/*" style="display:none">
                </div>
                <div class="canvas-container">
                    <canvas id="drawingCanvas" width="500" height="400"></canvas>
                </div>
                <button id="analyzeBtn" style="width: 100%; padding: 12px;">Анализировать рисунок</button>
            </section>
            
            <section class="info-section">
                <h2>Информация о животном</h2>
                <label for="animalName">Название животного:</label>
                <input type="text" id="animalName" placeholder="Придумайте уникальное название">
                
                <label for="animalDescription">Описание животного:</label>
                <textarea id="animalDescription" placeholder="Опишите его образ жизни, привычки, среду обитания..."></textarea>
                
                <div class="loading" id="loadingIndicator">
                    <div class="spinner"></div>
                    <p>Анализируем ваш рисунок...</p>
                </div>
                
                <div id="resultContainer">
                    <h3>Результаты анализа:</h3>
                    <div id="analysisResult"></div>
                </div>
            </section>
        </div>
        
        <!-- Модальное окно камеры -->
        <div class="camera-modal" id="cameraModal">
            <div class="camera-content">
                <video id="cameraPreview" autoplay playsinline></video>
                <div class="camera-buttons">
                    <button id="captureBtn">Сделать снимок</button>
                    <button id="cancelCameraBtn">Отмена</button>
                </div>
                <canvas id="cameraCanvas" style="display:none;"></canvas>
            </div>
        </div>
        
        <footer>
            НейроРНЖ &copy; 2025 | Психологический анализ рисунков. Не стоит доверять своё здоровье сервису. Обращайтесь к психологу.
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Инициализация canvas
            const canvas = document.getElementById('drawingCanvas');
            const ctx = canvas.getContext('2d');
            let isDrawing = false;
            let lastX = 0;
            let lastY = 0;
            let drawingHistory = [];
            let historyIndex = -1;
            
            // Настройки рисования
            let currentColor = document.getElementById('colorPicker').value;
            let currentBrushSize = document.getElementById('brushSize').value;
            
            // Элементы интерфейса
            const clearBtn = document.getElementById('clearBtn');
            const undoBtn = document.getElementById('undoBtn');
            const colorPicker = document.getElementById('colorPicker');
            const brushSize = document.getElementById('brushSize');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const resultContainer = document.getElementById('resultContainer');
            const analysisResult = document.getElementById('analysisResult');
            const cameraBtn = document.getElementById('cameraBtn');
            const uploadBtn = document.getElementById('uploadBtn');
            const fileInput = document.getElementById('fileInput');
            const saveImageBtn = document.getElementById('saveImageBtn');
            const cameraModal = document.getElementById('cameraModal');
            const cameraPreview = document.getElementById('cameraPreview');
            const captureBtn = document.getElementById('captureBtn');
            const cancelCameraBtn = document.getElementById('cancelCameraBtn');
            const cameraCanvas = document.getElementById('cameraCanvas');
            
            // Переменные для работы с камерой
            let stream = null;
            
            // Адаптация canvas под размер экрана
            function resizeCanvas() {
                const container = canvas.parentElement;
                canvas.width = container.offsetWidth - 4;
                canvas.height = canvas.width * 0.8;
                redrawCanvas();
            }
            
            // Перерисовка canvas из истории
            function redrawCanvas() {
                if (historyIndex >= 0 && historyIndex < drawingHistory.length) {
                    const image = new Image();
                    image.onload = function() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
                    };
                    image.src = drawingHistory[historyIndex];
                } else {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            }
            
            // Сохранение состояния canvas
            function saveCanvasState() {
                if (historyIndex < drawingHistory.length - 1) {
                    drawingHistory = drawingHistory.slice(0, historyIndex + 1);
                }
                
                drawingHistory.push(canvas.toDataURL());
                historyIndex = drawingHistory.length - 1;
                
                if (drawingHistory.length > 20) {
                    drawingHistory.shift();
                    historyIndex--;
                }
            }
            
            // Обработчики событий для рисования
            canvas.addEventListener('mousedown', startDrawing);
            canvas.addEventListener('touchstart', handleTouchStart);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchmove', handleTouchMove);
            canvas.addEventListener('mouseup', stopDrawing);
            canvas.addEventListener('touchend', stopDrawing);
            canvas.addEventListener('mouseout', stopDrawing);
            
            function startDrawing(e) {
                isDrawing = true;
                const pos = getPosition(e);
                [lastX, lastY] = [pos.x, pos.y];
                saveCanvasState();
            }
            
            function handleTouchStart(e) {
                e.preventDefault();
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent('mousedown', {
                    clientX: touch.clientX,
                    clientY: touch.clientY
                });
                startDrawing(mouseEvent);
            }
            
            function draw(e) {
                if (!isDrawing) return;
                
                const pos = getPosition(e);
                
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(pos.x, pos.y);
                ctx.strokeStyle = currentColor;
                ctx.lineWidth = currentBrushSize;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.stroke();
                
                [lastX, lastY] = [pos.x, pos.y];
            }
            
            function handleTouchMove(e) {
                e.preventDefault();
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent('mousemove', {
                    clientX: touch.clientX,
                    clientY: touch.clientY
                });
                draw(mouseEvent);
            }
            
            function stopDrawing() {
                isDrawing = false;
            }
            
            function getPosition(e) {
                const rect = canvas.getBoundingClientRect();
                return {
                    x: (e.clientX - rect.left) * (canvas.width / rect.width),
                    y: (e.clientY - rect.top) * (canvas.height / rect.height)
                };
            }
            
            // Обработчики кнопок
            clearBtn.addEventListener('click', function() {
                if (confirm('Вы уверены, что хотите очистить холст?')) {
                    saveCanvasState();
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            });
            
            undoBtn.addEventListener('click', function() {
                if (historyIndex > 0) {
                    historyIndex--;
                    redrawCanvas();
                }
            });
            
            colorPicker.addEventListener('input', function() {
                currentColor = this.value;
            });
            
            brushSize.addEventListener('input', function() {
                currentBrushSize = this.value;
            });
            
            // Загрузка изображения
            uploadBtn.addEventListener('click', function() {
                fileInput.click();
            });
            
            fileInput.addEventListener('change', function(e) {
                if (e.target.files && e.target.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(event) {
                        const img = new Image();
                        img.onload = function() {
                            // Сохраняем текущее состояние
                            saveCanvasState();
                            
                            // Очищаем холст и рисуем новое изображение
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                        };
                        img.src = event.target.result;
                    };
                    
                    reader.readAsDataURL(e.target.files[0]);
                }
            });
            
            // Работа с камерой
            cameraBtn.addEventListener('click', function() {
                cameraModal.style.display = 'flex';
                
                // Запрашиваем доступ к камере
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function(s) {
                        stream = s;
                        cameraPreview.srcObject = stream;
                    })
                    .catch(function(err) {
                        console.error("Ошибка доступа к камере: ", err);
                        alert("Не удалось получить доступ к камере. Пожалуйста, проверьте разрешения.");
                        cameraModal.style.display = 'none';
                    });
            });
            
            // Снимок с камеры
            captureBtn.addEventListener('click', function() {
                if (stream) {
                    // Создаем временный canvas для снимка
                    cameraCanvas.width = cameraPreview.videoWidth;
                    cameraCanvas.height = cameraPreview.videoHeight;
                    const context = cameraCanvas.getContext('2d');
                    context.drawImage(cameraPreview, 0, 0, cameraCanvas.width, cameraCanvas.height);
                    
                    // Закрываем камеру
                    stream.getTracks().forEach(track => track.stop());
                    cameraModal.style.display = 'none';
                    
                    // Сохраняем снимок на основном холсте
                    const img = new Image();
                    img.onload = function() {
                        saveCanvasState();
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    };
                    img.src = cameraCanvas.toDataURL();
                }
            });
            
            // Отмена съемки
            cancelCameraBtn.addEventListener('click', function() {
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                }
                cameraModal.style.display = 'none';
            });
            
            // Сохранение изображения (для использования в программе)
            saveImageBtn.addEventListener('click', function() {
                saveCanvasState();
                alert("Изображение сохранено для анализа!");
            });
            
            // Анализ рисунка
            analyzeBtn.addEventListener('click', function() {
                const name = document.getElementById('animalName').value.trim();
                const description = document.getElementById('animalDescription').value.trim();
                
                if (!name || !description) {
                    alert('Пожалуйста, укажите название и описание животного');
                    return;
                }
                
                const isEmpty = !canvas.toDataURL().replace(canvas.toDataURL('image/png', 0.1).split(',')[1], '');
                if (isEmpty) {
                    alert('Пожалуйста, нарисуйте или загрузите животное перед анализом');
                    return;
                }
                
                loadingIndicator.style.display = 'block';
                resultContainer.style.display = 'none';
                
                // Отправка данных на сервер
                fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image: canvas.toDataURL(),
                        name: name,
                        description: description
                    })
                })
                .then(response => response.json())
                .then(data => {
                    loadingIndicator.style.display = 'none';
                    
                    if (data.error) {
                        analysisResult.innerHTML = `<p>${data.error}</p>`;
                    } else {
                        analysisResult.innerHTML = marked.parse(data.analysis);
                    }
                    
                    resultContainer.style.display = 'block';
                    
                    if (window.MathJax) {
                        MathJax.typesetPromise();
                    }
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none';
                    analysisResult.innerHTML = `<p>Ошибка при анализе: ${error.message}</p>`;
                    resultContainer.style.display = 'block';
                });
            });
            
            // Инициализация
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);
            saveCanvasState();
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
