from huggingface_hub import hf_hub_download
import os

def download_model():
    model_id = "bartowski/Qwen2.5-7B-Instruct-GGUF"
    filename = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"
    local_dir = "models"
    
    os.makedirs(local_dir, exist_ok=True)
    
    print(f"Downloading {filename} from {model_id}...")
    print("This may take several minutes (approx 4.3 GB). Please wait...")
    
    file_path = hf_hub_download(
        repo_id=model_id, 
        filename=filename, 
        local_dir=local_dir
    )
    
    print(f"\nSuccessfully downloaded model to: {file_path}")

if __name__ == "__main__":
    download_model()
