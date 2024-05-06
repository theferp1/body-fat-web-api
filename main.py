from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

app = FastAPI()

# Permitir requisições CORS (Cross-Origin Resource Sharing) para todos os origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para redimensionar a imagem
def resize_image(image_bytes, output_size=(224, 224)):
    image = Image.open(BytesIO(image_bytes))
    resized_image = image.resize(output_size)
    return resized_image

# Rota para upload de imagem
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Ler a imagem enviada
    contents = await file.read()
    # Redimensionar a imagem
    resized_image = resize_image(contents)
    # Salvar a imagem redimensionada
    resized_image_path = "resized_" + file.filename
    resized_image.save(resized_image_path)
    # Retornar a imagem redimensionada
    return FileResponse(resized_image_path, media_type="image/jpeg")

# Iniciar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
