**Product Search with Text and Image Embeddings**

Here is the preview of the final app:


**Steps to Run**
1) Replicate the docker containers. The yaml file has the mongodb and gradio containers
```docker-compose up --build -d```

2) The final dataset is included in the file `dataset\textual\complete\final_products.csv` containing 10,200 items
However, to reproduce this dataset or increase it further run these 2 files  
  i) ```dataset_generate.ipynb``` The dataset is the "Amazon Products Dataset (+1M Products)" from Kaggle
  ii) To build an efficient embeddings search, we need product descriptions which were missing. The title contains some descriptions, however this project supplements that by generating product image captions by llava-1.5-13b-hf. The code is available in the file ```Llava Caption Generator.ipynb```

3) Build the Nvidia Triton Server
This project uses the "RTX A5000" Runpod instance. However, a smaller instance can also be used.
i) Load the Triton official Docker image "nvcr.io/nvidia/tritonserver:24.01-py3"
ii) Run the following commands once the image loads up:
- ```apt-get update && apt-get install -y pkg-config libcairo2-dev python3-dev git```
- pip install --no-cache-dir gdown
- git clone --single-branch --branch endpoint-creation https://github.com/Shahrukh95/Product-Search-With-Text-and-Image-Embeddings.git (the triton server and the flask app that converts the models into an API are vaialble this branch)
- cd Product-Search-With-Text-and-Image-Embeddings
- gdown --folder https://drive.google.com/drive/folders/1E2D2ekxGa4uQ2mu9zrURKb3f8l85fFjS -O model_repository; (this downloads the optimized ONNX models for text and image embeddings. More details for this sepcific part are described in the next section.)
- pip install --no-cache-dir -r requirements.txt;
- chmod +x start.sh;
- bash start.sh

The triton server and the flask app should be running now. Make sure the port 8000 (for triton server) and 5000 (for flask) are open.


4) Run the Gradio App locally
Once the containers have loaded up from step 1, the app should run automatically as defined in the Dockerfile. However, the endpoint API must be changed to point to your triton server. For Runpod this will be of the format: ```https://{YOUR-RUNPOD-ID}-5000.proxy.runpod.net/```


**ONNX Model Creation**
For this project, the following models were used:
1) WhereIsAI/UAE-Large-V1 (for text embeddings)
2) nomic-ai/nomic-embed-vision-v1.5 (for Image embeddings)

While both models are available as ONNX at HuggingFace, the UAE-Large-V1 model was converted into ONNX manually using the 'ORTModelForFeatureExtraction' library. The code is available in ```Product-Search-With-Text-and-Image-Embeddings/ONNX Resources/UAE-Large-V1.ipynb``` in the "endpoint-creation" branch.

The nomic-embed-vision-v1.5 ONNX model was downloaded from HuggingFace but downgraded from ONNX IR version 10 to 9 because the Triton image that we use in this project does not supprort ONNX version 10. The code is available at ```Product-Search-With-Text-and-Image-Embeddings/ONNX Resources/nomic-embed-vision-v1.5.ipynb``` in the "endpoint-creation" branch.

