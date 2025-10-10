from src.utils.generate_knowledge_graph import generate_knowledge_graph as generate_kg_util
from src.models.api_schemas import KnowledgeGraphRequest, KnowledgeGraphResponse
from src.common.custom_exception import CustomException

class KnowledgeGraphService:
    async def create_knowledge_graph(self, request: KnowledgeGraphRequest) -> KnowledgeGraphResponse:
        """Calls the utility function and returns the knowledge graph HTML content."""
        
        # The utility function handles the logic of content generation if only a topic is provided.
        html_content = await generate_kg_util(text=request.text, topic=request.topic)
        
        if "No graph data extracted" in html_content or "Could not generate content" in html_content:
            # Propagate error with a clearer message
            raise CustomException(f"Knowledge Graph generation failed: {html_content.replace('<html><body>', '').replace('</body></html>', '')}")
            
        return KnowledgeGraphResponse(html_content=html_content)