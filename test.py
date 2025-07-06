from llama_cpp import Llama

llm = Llama(
    model_path="models/llama-3-8b-Instruct.Q4_K_M.gguf",
    n_ctx=8192,
    n_gpu_layers=-1  # Demande à utiliser le GPU
)

output = llm("Test: Are you using CUDA?", max_tokens=10)
print(output["choices"][0]["text"])