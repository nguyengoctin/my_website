#!/usr/bin/env python3
"""
Fetch all AI Engineer Roadmap lesson data from roadmap.sh API.
Saves raw JSON for each node to a local directory.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://roadmap.sh"
ROADMAP_SLUG = "ai-engineer"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", ".roadmap-data")

# Mapping of node labels to directory categories
CATEGORY_MAP = {
    # 01-introduction
    "Introduction": "01-introduction",
    "What is an AI Engineer?": "01-introduction",
    "AI Engineer vs ML Engineer": "01-introduction",
    "Roles and Responsiblities": "01-introduction",
    "Impact on Product Development": "01-introduction",
    # 02-llm-fundamentals
    "How LLMs Work": "02-llm-fundamentals",
    "Large Language Model (LLM)": "02-llm-fundamentals",
    "AI vs AGI": "02-llm-fundamentals",
    "Inference": "02-llm-fundamentals",
    "Training": "02-llm-fundamentals",
    "Tokens": "02-llm-fundamentals",
    "Context": "02-llm-fundamentals",
    "Pre-trained Models": "02-llm-fundamentals",
    "Closed vs Open Source Models": "02-llm-fundamentals",
    "Type of Models": "02-llm-fundamentals",
    "Self-Hosted Models": "02-llm-fundamentals",
    # 03-prompt-engineering
    "Prompt Engineering": "03-prompt-engineering",
    "Zero-Shot": "03-prompt-engineering",
    "Few-Shot": "03-prompt-engineering",
    "CoT": "03-prompt-engineering",
    "ReAct": "03-prompt-engineering",
    "Input Format": "03-prompt-engineering",
    "System Prompting": "03-prompt-engineering",
    "Role & Behavior": "03-prompt-engineering",
    "Constraints": "03-prompt-engineering",
    "Structured Output": "03-prompt-engineering",
    "Function Calling": "03-prompt-engineering",
    "Prompt Caching": "03-prompt-engineering",
    "Streaming Responses": "03-prompt-engineering",
    "Sampling Parameters": "03-prompt-engineering",
    "Temperature": "03-prompt-engineering",
    "Top-K": "03-prompt-engineering",
    "Top-P": "03-prompt-engineering",
    "Repetition Penalties": "03-prompt-engineering",
    # 04-rag-and-vector-databases
    "What are Embeddings": "04-rag-and-vector-databases",
    "Embedding Models": "04-rag-and-vector-databases",
    "Embeddings": "04-rag-and-vector-databases",
    "Semantic Search": "04-rag-and-vector-databases",
    "Data Classification": "04-rag-and-vector-databases",
    "Recommendation Systems": "04-rag-and-vector-databases",
    "Anomaly Detection": "04-rag-and-vector-databases",
    "Open AI Embeddings API": "04-rag-and-vector-databases",
    "Gemini Embedding": "04-rag-and-vector-databases",
    "Sentence Transformers": "04-rag-and-vector-databases",
    "Models on Hugging Face": "04-rag-and-vector-databases",
    "Jina": "04-rag-and-vector-databases",
    "Vector Databases": "04-rag-and-vector-databases",
    "Purpose and Functionality": "04-rag-and-vector-databases",
    "Chroma": "04-rag-and-vector-databases",
    "Pinecone": "04-rag-and-vector-databases",
    "Weaviate": "04-rag-and-vector-databases",
    "FAISS": "04-rag-and-vector-databases",
    "LanceDB": "04-rag-and-vector-databases",
    "Qdrant": "04-rag-and-vector-databases",
    "Supabase": "04-rag-and-vector-databases",
    "MongoDB Atlas": "04-rag-and-vector-databases",
    "Indexing Embeddings": "04-rag-and-vector-databases",
    "Performing Similarity Search": "04-rag-and-vector-databases",
    "What are RAGs?": "04-rag-and-vector-databases",
    "RAG Usecases": "04-rag-and-vector-databases",
    "RAG vs Fine-tuning": "04-rag-and-vector-databases",
    "Chunking": "04-rag-and-vector-databases",
    "Embedding": "04-rag-and-vector-databases",
    "Vector Database": "04-rag-and-vector-databases",
    "Retrieval Process": "04-rag-and-vector-databases",
    "Generation": "04-rag-and-vector-databases",
    "Using SDKs Directly": "04-rag-and-vector-databases",
    "Langchain": "04-rag-and-vector-databases",
    "Llama Index": "04-rag-and-vector-databases",
    # 05-fine-tuning
    "Fine-tuning": "05-fine-tuning",
    # 06-ai-agents
    "AI Agents": "06-ai-agents",
    "Agents Usecases": "06-ai-agents",
    "ReAct Prompting": "06-ai-agents",
    "Manual Implementation": "06-ai-agents",
    "Tools & Function Calling": "06-ai-agents",
    "OpenAI AgentKit & Agent SDK": "06-ai-agents",
    "Claude Agent SDK": "06-ai-agents",
    "Multi-agents": "06-ai-agents",
    # 07-model-context-protocol-mcp
    "Model Context Protocol (MCP)": "07-model-context-protocol-mcp",
    "MCP Host": "07-model-context-protocol-mcp",
    "MCP Server": "07-model-context-protocol-mcp",
    "MCP Client": "07-model-context-protocol-mcp",
    "Data Layer": "07-model-context-protocol-mcp",
    "Transport Layer": "07-model-context-protocol-mcp",
    "Building an MCP Server": "07-model-context-protocol-mcp",
    "Building an MCP Client": "07-model-context-protocol-mcp",
    "Connect to Local Server": "07-model-context-protocol-mcp",
    "Connect to Remote Server": "07-model-context-protocol-mcp",
    # 08-multimodal-ai
    "Multimodal AI": "08-multimodal-ai",
    "Multimodal AI Usecases": "08-multimodal-ai",
    "Image Understanding": "08-multimodal-ai",
    "Image Generation": "08-multimodal-ai",
    "Video Understanding": "08-multimodal-ai",
    "Audio Processing": "08-multimodal-ai",
    "Text-to-Speech": "08-multimodal-ai",
    "Speech-to-Text": "08-multimodal-ai",
    "OpenAI Vision API": "08-multimodal-ai",
    "DALL-E API": "08-multimodal-ai",
    "Whisper API": "08-multimodal-ai",
    "Hugging Face Models": "08-multimodal-ai",
    "LangChain for Multimodal Apps": "08-multimodal-ai",
    "LlamaIndex for Multimodal Apps": "08-multimodal-ai",
    # 09-frameworks-and-tools
    "Hugging Face": "09-frameworks-and-tools",
    "Hugging Face Hub": "09-frameworks-and-tools",
    "Hugging Face Inference SDK": "09-frameworks-and-tools",
    "Transformers.js": "09-frameworks-and-tools",
    "Hugging Face Tasks": "09-frameworks-and-tools",
    "Ollama": "09-frameworks-and-tools",
    "LM Studio": "09-frameworks-and-tools",
    "Development Tools": "09-frameworks-and-tools",
    "Haystack": "09-frameworks-and-tools",
    "RAGFlow": "09-frameworks-and-tools",
    # 10-models-and-apis
    "Anthropic Claude": "10-models-and-apis",
    "Google Gemini": "10-models-and-apis",
    "OpenAI (GPT, o-series)": "10-models-and-apis",
    "Meta Llama": "10-models-and-apis",
    "Mistral": "10-models-and-apis",
    "Cohere": "10-models-and-apis",
    "DeepSeek": "10-models-and-apis",
    "Choosing the Right Model": "10-models-and-apis",
    "Gemma": "10-models-and-apis",
    "Qwen": "10-models-and-apis",
    "OpenRouter": "10-models-and-apis",
    "OpenAI Response API": "10-models-and-apis",
    "Google Gemini APi": "10-models-and-apis",
    "Claude Messages API": "10-models-and-apis",
    "OpenAI-compatible APIs": "10-models-and-apis",
    "NanoBanana API": "10-models-and-apis",
    "Vertex AI Agent Builder": "10-models-and-apis",
    "Google ADK": "10-models-and-apis",
    # 11-evaluation-safety-and-ethics
    "AI Safety and Ethics": "11-evaluation-safety-and-ethics",
    "Prompt Injection Attacks": "11-evaluation-safety-and-ethics",
    "Bias and Fairness": "11-evaluation-safety-and-ethics",
    "Security and Privacy Concerns": "11-evaluation-safety-and-ethics",
    "Conducting adversarial testing": "11-evaluation-safety-and-ethics",
    "Content Moderation APIs": "11-evaluation-safety-and-ethics",
    "Adding end-user IDs in prompts": "11-evaluation-safety-and-ethics",
    "Robust prompt engineering": "11-evaluation-safety-and-ethics",
    "Know your Customers / Usecases": "11-evaluation-safety-and-ethics",
    "Constraining outputs and inputs": "11-evaluation-safety-and-ethics",
    "LLM Observability": "11-evaluation-safety-and-ethics",
    "Tracing & logging": "11-evaluation-safety-and-ethics",
    "Cost/latency monitoring": "11-evaluation-safety-and-ethics",
    "Production monitoring": "11-evaluation-safety-and-ethics",
    "LangSmith": "11-evaluation-safety-and-ethics",
    "Langfuse": "11-evaluation-safety-and-ethics",
    "Helicone": "11-evaluation-safety-and-ethics",
    "Arize AI": "11-evaluation-safety-and-ethics",
    "LLM Evaluations": "11-evaluation-safety-and-ethics",
    "Deterministic Evals": "11-evaluation-safety-and-ethics",
    "Model-Based Evals": "11-evaluation-safety-and-ethics",
    "Human Evals": "11-evaluation-safety-and-ethics",
    "Evaluation Metrics": "11-evaluation-safety-and-ethics",
    "Regression Testing": "11-evaluation-safety-and-ethics",
    "DeepEval": "11-evaluation-safety-and-ethics",
    "RAGAS": "11-evaluation-safety-and-ethics",
    # 12-applications-and-usecases
    "Claude Code": "12-applications-and-usecases",
    "Gemini": "12-applications-and-usecases",
    "Codex": "12-applications-and-usecases",
    "Windsurf": "12-applications-and-usecases",
    "Cursor": "12-applications-and-usecases",
    "Replit": "12-applications-and-usecases",
    # Context engineering
    "Context Engineering": "03-prompt-engineering",
    "External Memory": "03-prompt-engineering",
    " RAG & Dynamic Filters": "03-prompt-engineering",
    "Context Compaction": "03-prompt-engineering",
    "Context Isolation": "03-prompt-engineering",
}


def slugify(text):
    """Convert text to URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def fetch_json(url, retries=3, delay=1.5):
    """Fetch JSON from URL with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; roadmap-fetcher/1.0)',
                'Accept': 'application/json',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None


def get_all_nodes():
    """Fetch roadmap JSON and extract all topic/subtopic nodes."""
    print("Fetching roadmap JSON...")
    data = fetch_json(f"{BASE_URL}/{ROADMAP_SLUG}.json")
    if not data:
        print("ERROR: Failed to fetch roadmap JSON")
        sys.exit(1)

    nodes = []
    for n in data.get('nodes', []):
        ntype = n.get('type', '')
        label = n.get('data', {}).get('label', '').strip()
        nid = n.get('id', '')
        if ntype in ('topic', 'subtopic') and label and nid:
            category = CATEGORY_MAP.get(label, "99-uncategorized")
            nodes.append({
                'id': nid,
                'type': ntype,
                'label': label,
                'slug': slugify(label),
                'category': category,
            })

    print(f"Found {len(nodes)} nodes ({sum(1 for n in nodes if n['type']=='topic')} topics, {sum(1 for n in nodes if n['type']=='subtopic')} subtopics)")
    return nodes


def fetch_node_content(node):
    """Fetch content for a single node."""
    url = f"{BASE_URL}/{ROADMAP_SLUG}/{node['id']}.json"
    data = fetch_json(url)
    if data:
        node['description'] = data.get('description', '')
        node['resources'] = data.get('resources', [])
        node['lesson_packs'] = data.get('lessonPacks', [])
        node['paid_resources'] = data.get('paidResources', [])
        node['updated_at'] = data.get('updatedAt', '')
        node['contribution_url'] = data.get('contribution', '')
    else:
        node['description'] = ''
        node['resources'] = []
        node['lesson_packs'] = []
        node['paid_resources'] = []
        node['updated_at'] = ''
        node['contribution_url'] = ''
    return node


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Get all nodes
    nodes = get_all_nodes()

    # Step 2: Fetch content for each node
    print(f"\nFetching content for {len(nodes)} nodes...")
    for i, node in enumerate(nodes):
        print(f"  [{i+1}/{len(nodes)}] {node['label']}...", end=" ")
        fetch_node_content(node)
        has_content = bool(node['description'].strip())
        print(f"{'OK' if has_content else 'EMPTY'} ({len(node['description'])} chars)")
        time.sleep(1.0)  # Rate limiting

    # Step 3: Save all data
    output_file = os.path.join(OUTPUT_DIR, "all_nodes.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(nodes)} nodes to {output_file}")

    # Summary
    with_content = sum(1 for n in nodes if n['description'].strip())
    empty = len(nodes) - with_content
    print(f"  With content: {with_content}")
    print(f"  Empty: {empty}")

    # List categories
    cats = {}
    for n in nodes:
        c = n['category']
        cats[c] = cats.get(c, 0) + 1
    print("\nCategory distribution:")
    for c in sorted(cats.keys()):
        print(f"  {c}: {cats[c]} lessons")


if __name__ == '__main__':
    main()
