import torch
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.sdp_kernel(enable_math=False, enable_flash=False, enable_mem_efficient=True)
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CUDA Version: {torch.version.cuda}")
print(f"BF16 (Flash Attention) Support: {torch.cuda.is_bf16_supported()}")
print(f"SDP (Scaled Dot Product) Attention Enabled: {torch.backends.cuda.sdp_kernel(enable_math=False, enable_flash=True, enable_mem_efficient=False)}")