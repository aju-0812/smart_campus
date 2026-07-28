from huggingface_hub import hf_hub_download

print("Starting download of Qwen2.5-7B-Instruct-Q4_K_M.gguf...")
hf_hub_download(
    repo_id="bartowski/Qwen2.5-7B-Instruct-GGUF",
    filename="Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    local_dir="models",
    local_dir_use_symlinks=False
)
print("Download complete!")
