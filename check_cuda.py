import llama_cpp

try:
    # Attempt to create a Llama object, specifying GPU usage (n_gpu_layers > 0)
    # We use a dummy model path as we only want to check CUDA detection, not load a model.
    # Set verbose=True to see detailed loading information.
    model = llama_cpp.Llama(model_path="non_existent_model.gguf", n_gpu_layers=1, verbose=True)
    print("\n**CUDA (GPU) support is likely enabled!**")
    print("This message appears if Llama attempts to use GPU layers without error.")
    # print(f"Number of GPU layers configured: {model.n_gpu_layers}") # Optional: uncomment if you want to see the number

except Exception as e:
    print(f"\n**CUDA (GPU) support might NOT be enabled or failed to initialize.**")
    print(f"Error: {e}")
    print("This could happen if CUDA wasn't built correctly, or if there's no suitable GPU detected.")