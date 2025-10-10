from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from pyvis.network import Network
from src.llm.groq_client import get_groq_llm
from src.utils.content_generator import generate_content_for_topic
from src.common.logger import get_logger
import base64

logger = get_logger("KnowledgeGraphGenerator")

import re

def clean_html_for_json(html_content: str) -> str:
    """
    Cleans HTML content to make it safe for JSON serialization.
    Removes or escapes problematic control characters.
    """
    # Replace problematic control characters
    html_content = html_content.replace('\n', '\\n')
    html_content = html_content.replace('\r', '\\r')
    html_content = html_content.replace('\t', '\\t')
    
    # Alternative: Remove control characters entirely
    # html_content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', html_content)
    
    return html_content

async def extract_graph_data(text: str):
    """Asynchronously extracts graph data from input text."""
    # Use a low temperature for fact extraction
    llm = get_groq_llm(temperature=0)
    graph_transformer = LLMGraphTransformer(llm=llm)
    documents = [Document(page_content=text)]
    # This is the async call now fully compatible with FastAPI's event loop
    graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_documents


def visualize_graph(graph_documents):
    """
    Visualizes a knowledge graph using PyVis and returns the HTML content.
    """
    if not graph_documents or not graph_documents[0].nodes:
        return "<html><body>No graph data extracted.</body></html>"

    net = Network(height="750px", width="100%", directed=True,
                      notebook=False, bgcolor="#222222", font_color="white", filter_menu=True, cdn_resources='remote')

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    node_dict = {node.id: node for node in nodes}

    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    for node_id in valid_node_ids:
        node = node_dict[node_id]
        label = node.id if len(node.id) < 30 else f"{node.id[:27]}..."
        try:
            net.add_node(node.id, label=label, title=f"Type: {node.type}\nID: {node.id}", group=node.type)
        except Exception as e:
            logger.warning(f"Failed to add node {node.id}: {str(e)}")
            continue

    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except Exception as e:
            logger.warning(f"Failed to add edge from {rel.source.id} to {rel.target.id}: {str(e)}")
            continue

    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            },
            "nodes": {
                "font": { "color": "white" }
            },
            "configure": {
                "enabled": true
            }
        }
    """)

    # Generate HTML to a temporary file
    import tempfile
    import os as os_module
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as tmp_file:
        tmp_path = tmp_file.name
        net.save_graph(tmp_path)

    # Read the HTML content
    with open(tmp_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Clean up the temporary file
    try:
        os_module.unlink(tmp_path)
    except Exception as e:
        logger.warning(f"Failed to delete temporary file {tmp_path}: {str(e)}")

    # Base64 encode to avoid JSON serialization issues
    html_bytes = html_content.encode('utf-8')
    html_base64 = base64.b64encode(html_bytes).decode('utf-8')
    
    return html_base64

async def generate_knowledge_graph(text: str = None, topic: str = None) -> str:
    """Generates and visualizes a knowledge graph from input text or a topic."""
    if not text and not topic:
        return "<html><body>Please provide a topic or text to generate the knowledge graph.</body></html>"

    source_text = text
    if not source_text and topic:
        logger.info(f"No text provided, generating content for topic: {topic}")
        source_text = await generate_content_for_topic(topic)

    if not source_text:
        return "<html><body>Could not generate content for the given topic.</body></html>"

    graph_documents = await extract_graph_data(source_text)
    html_content = visualize_graph(graph_documents)
    return html_content