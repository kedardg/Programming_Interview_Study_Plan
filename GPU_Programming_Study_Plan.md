# GPU_Programming_Study_Plan
This is a GPU Programming Study Plan built from the [GPU MODE lectures](https://github.com/gpu-mode/lectures). All the lectures are on [this](https://www.youtube.com/@GPUMODE) YouTube channel.

## Step 1 - Get set up

- Subscribe to the [GPU MODE YouTube channel](https://www.youtube.com/@GPUMODE)
- Join the [GPU MODE Discord](https://discord.gg/gpumode) to ask questions and find study partners
- Get the PMPP book: [Programming Massively Parallel Processors: A Hands-on Approach](https://a.co/d/2S2fVzt)
- Clone the [lectures repo](https://github.com/gpu-mode/lectures) so you have all the notebooks and code locally

###### How to Study Each Lecture
1. Read the matching PMPP chapter (if there is one)
2. Watch the lecture
3. Open the slides/notebook and re-run the code yourself
4. Rewrite the kernel from scratch without looking
5. Check it against the PyTorch version for correctness
6. Profile it and benchmark it against PyTorch
7. Try one optimization and measure again
8. Explain what you learned in English (notes, blog post, or README)

## Step 2 - Learn CUDA Basics

- Lecture 1: Profiling and Integrating CUDA kernels in PyTorch (Mark Saroufim) - [notebook & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_001)
- Lecture 2: Recap Ch. 1-3 from the PMPP book (Andreas Koepf) - [slides](https://github.com/gpu-mode/lectures/blob/main/lecture_002/cuda_mode_lecture2.pptx) or the [Google Slides version](https://docs.google.com/presentation/d/1deqvEHdqEC4LHUpStO6z3TT77Dt84fNAvTIAxBJgDck/edit#slide=id.g2b1444253e5_1_75)
- Lecture 3: Getting Started With CUDA (Jeremy Howard) - [notebook](https://github.com/gpu-mode/lectures/tree/main/lecture_003) or the [Colab version](https://colab.research.google.com/drive/180uk6frvMBeT4tywhhYXmz3PJaCIA_uk?usp=sharing)
- Lecture 5: Going Further with CUDA for Python Programmers (Jeremy Howard) - [notebook](https://github.com/gpu-mode/lectures/tree/main/lecture_005)

## Step 3 - Understand GPU Architecture & Performance

- Lecture 4: Intro to Compute and Memory Architecture (Thomas Viehmann) - [notebook & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_004)
- Lecture 8: CUDA Performance Checklist (Mark Saroufim) - [code](https://github.com/gpu-mode/lectures/tree/main/lecture_008), [slides](https://docs.google.com/presentation/d/1cvVpf3ChFFiY4Kf25S4e4sPY6Y5uRUO-X-A4nJ7IhFE/edit?usp=sharing)
- Lecture 16: Hands-on Profiling (Taylor Robie)
- Lecture 37: Introduction to SASS & GPU Microarchitecture (Arun Demeure) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_037)
- Lecture 41: CUDA Docs for Humans (Charles Frye) - [slides](https://docs.google.com/presentation/d/15lTG6aqf72Hyk5_lqH7iSrc8aP1ElEYxCxch-tD37PE/edit#slide=id.g326210b960f_0_42)

## Step 4 - Learn the Core Parallel Algorithms

- Lecture 9: Reductions (Mark Saroufim) - [code](https://github.com/gpu-mode/lectures/tree/main/lecture_009), [slides](https://docs.google.com/presentation/d/1s8lRU8xuDn-R05p1aSP6P7T5kk9VYnDOCyN5bWKeg3U/edit?usp=drive_link)
- Lecture 20: Scan Algorithm (Izzat El Hajj) - [slides](https://docs.google.com/presentation/d/1MEMsE5LKi6ush_60hlYu3-cz4DUCFzSL/edit?usp=sharing&ouid=106222972308395582904&rtpof=true&sd=true)
- Lecture 21: Scan Algorithm Part 2 (Izzat El Hajj) - same slides as Lecture 20
- Lecture 24: Scan at the Speed of Light (Jake Hemstad & Georgii Evtushenko)
- Lecture 19: Data Processing on GPUs (Devavret Makkar)

## Step 5 - Learn Triton

- Lecture 14: Practitioner's Guide to Triton (Umer Adil) - [notebook](https://github.com/gpu-mode/lectures/blob/main/lecture_014/A_Practitioners_Guide_to_Triton.ipynb)
- Lecture 29: Triton Internals (Kapil Sharma) - [code & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_029)
- Lecture 28: Liger Kernel (Byron Hsu) - [slides](https://docs.google.com/presentation/d/1CGTV-uKw9crrBo13q1jAzAFCFzlpZFjeL4bnK67pTd8/edit?usp=sharing)
  1. [RMSNorm: Verifying Correctness and Performance](https://colab.research.google.com/drive/1CQYhul7MVG5F0gmqTBbx1O1HgolPgF0M?usp=sharing)
  2. [FusedLinearCrossEntropy: Verifying Memory Reduction](https://colab.research.google.com/drive/1Z2QtvaIiLm5MWOs7X6ZPS1MN3hcIJFbj?usp=sharing)
  3. [Convergence Comparison: Triton Kernel Patched vs. Original Model Layer-by-Layer](https://colab.research.google.com/drive/1e52FH0BcE739GZaVp-3_Dv7mc4jF1aif?usp=sharing)
  4. [Contiguity is the hidden killer](https://colab.research.google.com/drive/1llnAdo0hc9FpxYRRnjih0l066NCp7Ylu?usp=sharing)
  5. [Address int32 overflow](https://colab.research.google.com/drive/1WgaU_cmaxVzx8PcdKB5P9yHB6_WyGd4T?usp=sharing)
- Lecture 104: Gluon: Tile-Based GPU Programming with Low-Level Control (Peter Bell, Mario Lezcano, Keren Zhou) - [slides & notes](https://github.com/gpu-mode/lectures/tree/main/lecture_104)

## Step 6 - Learn Tensor Cores, CUTLASS & CuTe

- Lecture 23: Tensor Cores (Vijay Thakkar & Pradeep Ramani) - [slides](https://drive.google.com/file/d/18sthk6IUOKbdtFphpm_jZNXoJenbWR8m/view)
- Lecture 15: CUTLASS (Eric Auld)
- Lecture 57: CuTe (Cris Cecka) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_057)
- Lecture 103: Fundamentals of CuTe Layout Algebra and Category-theoretic Interpretation (Jack Carlisle & Jay Shah) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_103)
- Lecture 114: PyCuTe (Cris Cecka) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_114), [code](https://github.com/NVlabs/CuTe)
- Lecture 86: Introduction to CuTeDSL (Vicki Wang) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_086)
- Lecture 75: GPU Programming Fundamentals + ThunderKittens (William Brandon & Simran Arora) - [slides 1](https://docs.google.com/presentation/d/1ypi4IjEF36PUZGOJSaFxjNzk7BpO61TicdTBBf77oqc/), [slides 2](https://github.com/gpu-mode/lectures/tree/main/lecture_075)

## Step 7 - Learn Attention & Fused Kernels

- Lecture 18: Fused Kernels (Kapil Sharma) - [code](https://github.com/gpu-mode/lectures/tree/main/lecture_018)
- Lecture 12: Flash Attention (Thomas Viehmann) - [code](https://github.com/gpu-mode/lectures/tree/main/lecture_012)
- Lecture 36: CUTLASS and Flash Attention 3 (Jay Shah) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_036)
- Lecture 13: Ring Attention (Andreas Koepf) - [slides](https://github.com/gpu-mode/lectures/blob/main/lecture_013/ring_attention.pptx)
- Lecture 40: FlashInfer (Zihao Ye)
- Lecture 72: Efficient & Effective Long-Context Modeling for Large Language Models (Guangxuan Xiao) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_072)
- Lecture 74: Positional Encodings and PaTH Attention (Songlin Yang) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_074)
- Lecture 79: Mirage (MPK): Compiling LLMs into Mega Kernels (Mengdi Wu & Xinhao Cheng) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_079)

## Step 8 - Learn Quantization, Sparsity & Numerics

- Lecture 84: Numerics and AI (Paulius Micikevicius) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_084)
- Lecture 7: Advanced Quantization (Charles Hernandez) - [slides](https://www.dropbox.com/scl/fi/hzfx1l267m8gwyhcjvfk4/Quantization-Cuda-vs-Triton.pdf?rlkey=s4j64ivi2kpp2l0uq8xjdwbab&dl=0)
- Lecture 11: Sparsity (Jesse Cai) - [slides](https://github.com/gpu-mode/lectures/blob/main/lecture_011/sparsity.pptx)
- Lecture 34: Low Bit Triton Kernels (Hicham Badri) - [slides](https://docs.google.com/presentation/d/1R9B6RLOlAblyVVFPk9FtAq6MXR1ufj1NaT0bjjib7Vc/edit)
- Lecture 33: BitBLAS (Wang Lei) - [code & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_033)
- Lecture 43: INT8 Matmul on Turing (Erik Schultheis) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_042)
- Lecture 38: Lowbit Kernels for ARM CPU (Scott Roy) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_038)
- Lecture 30: Quantized Training (Thien Tran) - [code & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_030)
- Lecture 69: Quartet 4-bit Training (Roberto Castro & Andrei Panferov) - [paper](https://arxiv.org/abs/2505.14669), code [here](https://github.com/IST-DASLab/Quartet) and [here](https://github.com/IST-DASLab/qutlass)

## Step 9 - Learn Multi-GPU & Distributed Programming

- Lecture 17: GPU Collective Communication (NCCL) (Dan Johnson) - [code](https://github.com/gpu-mode/lectures/tree/main/lecture_017)
- Lecture 67: NCCL & NVSHMEM (Jeff Hammond) - [slides](https://drive.google.com/file/d/1T8uHhFIeVa_g1oYb_O4d2Ltb8YQly1zK/view?usp=sharing), [code](https://github.com/ParRes/Kernels/tree/main/Cxx11)
- Lecture 70: Fault Tolerant Communication Collectives (mike64_t) - [slides](https://docs.google.com/presentation/d/1MKB51lhNOsV-Y_hscSaJk7wZskzxft2pFJQZKyvcMyo/edit?usp=sharing)
- Lecture 78: Iris: Multi-GPU Programming in Triton (Muhammad Awad, Muhammad Osama & Brandon Potter) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_078)
- Lecture 39: TorchTitan (Mark Saroufim & Tianyu Liu)

## Step 10 - Learn How Production Libraries & Inference Engines Work

- Lecture 6: Optimizing PyTorch Optimizers (Jane Xu) - [slides](https://docs.google.com/presentation/d/13WLCuxXzwu5JRZo0tAfW0hbKHQMvFw4O/edit#slide=id.p1)
- Lecture 10: Build a Prod Ready CUDA Library (Oscar Amoros Huguet) - [slides](https://drive.google.com/drive/folders/158V8BzGj-IkdXXDAdHPNwUzDLNmr971_?usp=drive_link)
- Bonus Lecture: CUDA C++ llm.cpp (Jake Hemstad & Georgii Evtushenko) - [slides](https://drive.google.com/drive/folders/1T-t0d_u0Xu8w_-1E5kAwmXNfF72x-HTA)
- Lecture 106: HF Kernels - [slides](https://docs.google.com/presentation/d/1RibAIrOJv0BcAx2QjNYHDZCrMfGYifTggtKT6uwv7CY/edit)
- Lecture 32: Unsloth - LLM Systems Engineering (Daniel Han) - [slides](https://docs.google.com/presentation/d/1BvgbDwvOY6Uy6jMuNXrmrz_6Km_CBW0f2espqeQaWfc/edit?usp=sharing)
- Lecture 22: Hacker's Guide to Speculative Decoding in vLLM (Cade Daniel) - [slides](https://docs.google.com/presentation/d/1p1xE-EbSAnXpTSiSI0gmy_wdwxN5XaULO3AnCWWoRe4/edit#slide=id.p)
- Lecture 35: SGLang Performance Optimization (Yineng Zhang) - [slides](https://github.com/zhyncs/lectures/blob/main/lecture_035/SGLang-Performance-Optimization-YinengZhang.pdf)
- Lecture 71: FlexOlmo: Open Language Models for Flexible Data Use (Sewon Min) - [slides](https://github.com/gpu-mode/lectures/tree/main/lecture_071)

## Step 11 - Go Beyond CUDA (Other Hardware & Languages)

- Lecture 25: Speaking Composable Kernel - AMD ROCm (Haocong Wang) - [slides](https://github.com/gpu-mode/lectures/blob/main/lecture_025/AMD_ROCm_Speaking_Composable_Kernel_July_20_2024.pdf)
- Lecture 26: SYCL MODE - Intel GPU (Patric Zhao) - [slides](https://docs.google.com/presentation/d/1SW4XKomAJhhJSH5-jpZI9Qlwp7TEunbV/edit?usp=sharing&ouid=106222972308395582904&rtpof=true&sd=true)
- Lecture 31: Beginners Guide to Metal Kernels (Nikita Shulga) - [code & slides](https://github.com/gpu-mode/lectures/tree/main/lecture_031)
- Lecture 27: gpu.cpp - WebGPU (Austin Huang) - [slides](https://gpucpp-presentation.answer.ai/)
- Lecture 42: Mosaic GPU (Adam Paszke)

## Step 12 - Build Your Kernel Portfolio

- Write & upload 3 kernels to your GitHub portfolio (e.g. a reduction, a fused softmax, and a tiled matmul)
- For each one, document correctness checks and benchmarks against PyTorch in the README
- Share your work and get feedback on the [GPU MODE Discord](https://discord.gg/gpumode)
