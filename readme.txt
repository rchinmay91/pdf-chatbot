flowchart TD
    %% Global Styling Configurations
    classDef source fill:#f5f6fa,stroke:#7f8c8d,stroke-width:2px,stroke-dasharray: 2;
    classDef processing fill:#dff9fb,stroke:#0984e3,stroke-width:1px;
    classDef storage fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px;
    classDef engine fill:#fff3e0,stroke:#f39c12,stroke-width:2px;
    classDef output fill:#f1f2f6,stroke:#2f3542,stroke-width:2px;

    %% Data Ingestion Phase
    subgraph INGESTION & DOCUMENT PIPELINE
        A[Target PDF Document]:::source --> B[PyPDF Ingestion Loader]:::processing
        B --> C[Recursive Character Text Segmentation]:::processing
        C --> D[Sentence-Transformers Vector Compiler]:::processing
        D --> E[(Chroma DB Structural Matrix)]:::storage
    end

    %% Inference Phase
    subgraph INFERENCE & STATE ROUTING
        F[Multi-Turn Chat Input]:::source --> G[Intent & History Context Condenser]:::engine
        G --> H[Vector Similarity Matrix Query]:::processing
        E -.->|Semantic Extraction| H
        H --> I[Qwen-2.5-7B Chat Model Endpoint]:::engine
        I --> J[Gradio 6.0 Presentation Interface]:::output
    end


## 🖼️ Application Workspace Preview

<p align="center">
  <img src="https://amazonaws.com" width="12%"/>
</p>

| Module View | Interface Capabilities |
| :--- | :--- |
| **Document Ingestion Hub** | Single-click file processing pipeline equipped with real-time status feedback tracking logs. |
| **Conversational Matrix Space** | Streaming response panels optimized with multi-turn intent tracking using robust Gradio 6 standard tokens. |


├── app.py                # Core interface definition & LangChain LCEL pipeline 
├── requirements.txt      # Structural software dependency landscape requirements
├── .gitignore            # Security rules blocking secret and cache tracking leakage
└── README.md             # Aesthetic architectural documentation 


git clone https://github.com/rchinmay91/pdf-chatbot.git
cd pdf-chatbot


MIT License

Copyright (c) 2026 rchinmay91

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
