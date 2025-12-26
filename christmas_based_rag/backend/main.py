"""
Christmas RAG Backend with FastAPI
Install: pip install fastapi uvicorn chromadb sentence-transformers python-multipart
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import re
from typing import List, Dict, Optional


app = FastAPI(
    title="Christmas RAG API",
    description="A RAG system that answers questions about Christmas",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    """Request model for search endpoint"""
    query: str
    n_results: int = 3

class ChunkResponse(BaseModel):
    """Single chunk in response"""
    id: int
    text: str
    section: str
    relevance: float

class SearchResponse(BaseModel):
    """Response model for search endpoint"""
    success: bool
    query: str
    chunks: List[ChunkResponse]
    total_chunks: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    backend: str = "FastAPI"


CHRISTMAS_DOC = """
# The Complete Guide to Christmas

## 1. History and Origins of Christmas

Christmas is an annual Christian festival celebrating the birth of Jesus Christ, observed primarily on December 25th as a religious holiday and cultural celebration among billions of people around the world. The word "Christmas" comes from the Old English term "Cristes maesse," meaning "Christ's mass." The exact date of Jesus's birth is historically uncertain, but the church fixed December 25th as the celebration date in the 4th century. The holiday has roots in both pagan winter festivals and early Christian traditions. The celebration of Christmas evolved over centuries, incorporating elements from Roman Saturnalia and Germanic winter festivals. By the 12th century, Christmas had become one of the most important festivals in the Christian calendar. The modern form of Christmas, as we know it today, developed during the Victorian era in the 19th century.

## 2. Christmas Traditions and Customs

Christmas traditions vary significantly across different cultures and families. Common traditions include decorating homes with Christmas trees, lights, and garland. Many families gather for Christmas dinner on December 25th. Gift-giving is a central tradition, with presents exchanged among family members and friends. The Christmas tree, typically an evergreen like a pine or spruce, is decorated with lights and ornaments and topped with a star or angel. Hanging stockings on the fireplace mantel is a tradition where small gifts are placed inside and revealed on Christmas morning. Caroling, or singing Christmas songs, is a tradition where groups visit homes and sing festive music. Attending church services is an important tradition for many Christian families. The Christmas season typically runs from early December through New Year's Day, with many people putting up decorations as early as November.

## 3. Christmas Decorations and Symbols

Christmas decorations serve to create a festive and joyful atmosphere in homes, streets, and public spaces. The Christmas tree is perhaps the most iconic decoration, usually decorated with ornaments, lights, and topped with a star representing the Star of Bethlehem. Lights are hung on houses, trees, and buildings, creating beautiful displays that brighten the dark winter nights. Wreaths, typically made from evergreen branches and decorated with ribbons and bells, are hung on doors. Garland, strings of intertwined leaves and branches, are draped around doorways and banisters. Ornaments come in countless designs, from traditional balls to character-shaped figurines. Stockings are decorative socks hung for each family member. The nativity scene or manger display depicts the birth of Jesus with figurines of Mary, Joseph, baby Jesus, animals, and the Wise Men. The Star of Bethlehem is a symbol representing the star that guided the Wise Men to Jesus's birthplace. Holly, with its red berries and prickly green leaves, is a traditional Christmas plant. Mistletoe is a plant hung in doorways, with a tradition that people should kiss when standing beneath it. Candy canes, with their red and white striped appearance, are traditional Christmas candies and decorations.

## 4. Christmas Food and Feasting

Christmas meals are central to the holiday celebration and vary greatly across different countries and cultures. In many Western countries, roasted turkey or ham is the main dish for Christmas dinner. Traditional side dishes include stuffing, roasted vegetables like carrots, parsnips, and Brussels sprouts, and cranberry sauce. Potatoes, either mashed or roasted, are common accompaniments. Christmas pudding is a traditional British dessert made with dried fruits, spices, and brandy, often prepared weeks in advance. Mince pies, small pastries filled with spiced fruit, are popular in the UK. Gingerbread cookies and cakes are traditional Christmas treats in many countries. Fruitcake, a dense cake filled with dried fruits and nuts, is a classic Christmas dessert. Hot chocolate and eggnog, a creamy drink made with eggs, cream, and sometimes alcohol, are popular Christmas beverages. In Mexico, tamales are a traditional Christmas food. In Italy, panettone is the traditional Christmas cake. In Germany, stollen and pfeffernüsse are favorites. In Sweden, Christmas Eve is celebrated with traditional foods like ham, meatballs, and herring. In Japan, Kentucky Fried Chicken has become a popular Christmas tradition since the 1970s. Many families prepare Christmas cookies and candy treats at home.

## 5. Santa Claus and Gift-Giving

Santa Claus, also known as Saint Nick, Father Christmas, or Kris Kringle, is a legendary figure in Western Christmas tradition who brings gifts to well-behaved children on Christmas Eve. The modern image of Santa Claus is based on Saint Nicholas, a 4th-century Christian bishop known for his generosity. The Dutch brought their tradition of Sint Nikolaas to America, which evolved into the English "Santa Claus." Santa is typically depicted as a jolly, rotund man with a white beard, wearing a red suit with white fur trim and a red hat. According to tradition, Santa lives at the North Pole with his wife and elves who help make toys. Santa keeps lists of children who have been "naughty or nice." On Christmas Eve, Santa travels the world in a sleigh pulled by flying reindeer, delivering presents through chimneys. The reindeer are named Dasher, Dancer, Prancer, Vixen, Comet, Cupid, Donner, Blitzen, and Rudolph. Children leave cookies and milk for Santa on Christmas Eve. The practice of gift-giving represents the gifts brought by the Wise Men to baby Jesus.

## 6. Christmas Music and Carols

Christmas music plays a central role in creating the festive atmosphere. Traditional Christmas carols include "Silent Night," "Jingle Bells," "We Wish You a Merry Christmas," and "O Come All Ye Faithful." "Silent Night" is a gentle hymn about peace during Christ's birth. "Jingle Bells" is a secular song about sleigh racing and winter fun. "Deck the Halls" is about decorating homes for Christmas. Modern Christmas songs like "All I Want for Christmas Is You" by Mariah Carey have become very popular. Christmas caroling is the tradition of singing songs in neighborhoods. Many communities host Christmas concerts and tree-lighting ceremonies. Schools, orchestras, and choirs perform special Christmas concerts. Radio stations switch to all-Christmas music formats starting in November.

## 7. Christmas Around the World

Christmas is celebrated in many countries worldwide with different traditions. In the United States, Christmas is celebrated on December 25th with family gatherings and gift exchanges. In the United Kingdom, Christmas crackers are a unique tradition. In Canada, celebrations are similar to the US with outdoor winter activities. In Australia, December is summer, so Christmas includes beach activities and barbecues. In Mexico, Las Posadas is a nine-day celebration before Christmas. In France, Christmas dinner features seafood and a special cake called bûche de Noël. In Germany, Christmas markets are popular gathering places. In Italy, Epiphany (January 6th) celebrates the arrival of the Wise Men. In Sweden, Christmas Eve is the main celebration. In Japan, Christmas is a secular holiday with gift-giving and KFC. In many African countries, Christmas includes church services and special meals.

## 8. Christmas Symbols and Their Meanings

Christmas symbols carry deep religious and cultural meanings. The Star of Bethlehem represents the star guiding the Wise Men to Jesus's birthplace. Holly symbolizes the crown of thorns with its red berries representing Jesus's blood. Mistletoe is hung in doorways with the tradition of kissing beneath it. Bells are rung to celebrate and announce the holiday. The Candy Cane has a curved shape like a shepherd's crook and red and white colors representing purity and sacrifice. Evergreen plants represent eternal life and spring's return. The number three is significant, representing the Trinity and the three Wise Men. Angels are symbols of heavenly messengers announcing Jesus's birth. The Nativity Scene depicts the birth of Jesus with figurines of Mary, Joseph, baby Jesus, animals, and the Wise Men. Candles represent Christ as "the light of the world."

## 9. Modern Christmas Celebrations

Contemporary Christmas celebrations have evolved with modern technology. Christmas shopping is a major commercial activity with retailers offering substantial discounts. Black Friday marks the beginning of the Christmas shopping season. Cyber Monday focuses on online shopping deals. Christmas movies and TV specials are widely watched. Streaming services offer extensive Christmas movie libraries. Social media plays a significant role with people sharing photos of decorations and gifts. Christmas-themed decorations have become increasingly elaborate. Video calls allow separated families to celebrate together remotely. Christmas charity and giving have expanded. Virtual Christmas parties have become more prevalent. Environmental consciousness influences modern celebrations with sustainable choices.

## 10. Christmas Values and Significance

Beyond commercial aspects, Christmas carries deep spiritual and human values. For Christians, Christmas represents the birth of Jesus Christ and God's love. Hope is central, representing salvation and new beginnings. Generosity is emphasized throughout the season. Family unity brings families together regardless of distance. Peace on Earth is a central message promoting harmony and goodwill. Love is expressed through gift-giving and spending time with loved ones. Gratitude is reflected in celebrations and giving thanks. Forgiveness is encouraged during the season. Joy and celebration lift spirits during dark winter months. Reflection on the past year and setting intentions are important aspects. The Christmas season promotes charitable giving and community service.
"""



class ChristmasRAG:
    """Christmas RAG system using ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.Client()
        
        # Use sentence transformers for embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create collection
        self.collection = self.client.get_or_create_collection(
            name="christmas_knowledge",
            embedding_function=self.embedding_function
        )
        
        # Initialize with documents
        self._initialize_documents()
    
    def _initialize_documents(self):
        """Initialize documents if collection is empty"""
        if self.collection.count() == 0:
            print(" Loading Christmas documents into ChromaDB...")
            chunks = self.chunk_document(CHRISTMAS_DOC)
            self.add_documents(chunks)
            print(f" Loaded {len(chunks)} chunks")
    
    def chunk_document(self, text: str, sentences_per_chunk: int = 3, overlap_sentences: int = 1) -> List[Dict]:
        """Split document into chunks"""
        chunks = []
        
        # Split by sections (##)
        sections = re.split(r'\n##\s+', text)
        
        for section in sections:
            if not section.strip():
                continue
            
            # Extract section title
            lines = section.split('\n', 1)
            section_title = lines[0].strip()
            section_content = lines[1] if len(lines) > 1 else ""
            
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', section_content)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Create chunks with overlap
            for i in range(0, len(sentences), sentences_per_chunk - overlap_sentences):
                chunk_sentences = sentences[i:i + sentences_per_chunk]
                
                if not chunk_sentences:
                    continue
                
                chunk_text = ' '.join(chunk_sentences)
                
                chunks.append({
                    'text': chunk_text,
                    'section': section_title,
                    'sentence_count': len(chunk_sentences),
                    'length': len(chunk_text),
                })
        
        return chunks
    
    def add_documents(self, chunks: List[Dict]):
        """Add chunks to ChromaDB"""
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [
            {
                'section': chunk['section'], 
                'length': chunk['length'],
                'sentence_count': chunk['sentence_count']
            } 
            for chunk in chunks
        ]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 3) -> Dict:
        """Search for relevant chunks"""
        if not query.strip():
            raise ValueError("Query cannot be empty")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }



rag = ChristmasRAG()



@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": " Welcome to Christmas RAG API!",
        "endpoints": {
            "health": "GET /health",
            "search": "POST /search",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Christmas RAG API is running!",
        backend="FastAPI with ChromaDB"
    )

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for Christmas information
    
    Request body:
    - query: str - Your question about Christmas
    - n_results: int - Number of results (default: 3)
    """
    try:
        # Validate query
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Validate n_results
        if request.n_results < 1 or request.n_results > 10:
            raise HTTPException(status_code=400, detail="n_results must be between 1 and 10")
        
        # Search
        results = rag.search(request.query, n_results=request.n_results)
        
        # Format response
        chunks = [
            ChunkResponse(
                id=i,
                text=results['documents'][i],
                section=results['metadatas'][i].get('section', 'Unknown'),
                relevance=round(1 - results['distances'][i], 2)
            )
            for i in range(len(results['documents']))
        ]
        
        return SearchResponse(
            success=True,
            query=request.query,
            chunks=chunks,
            total_chunks=len(chunks)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info")
async def get_info():
    """Get API information"""
    return {
        "api_name": "Christmas RAG API",
        "version": "1.0.0",
        "description": "RAG system for Christmas information",
        "total_chunks": rag.collection.count(),
        "embedding_model": "all-MiniLM-L6-v2",
        "vector_dimension": 384
    }


if __name__ == "__main__":
    import uvicorn
    print("\n Starting Christmas RAG API...")
    print(" Server running at http://localhost:8000")
    print(" API docs at http://localhost:8000/docs")
    print(" Swagger UI at http://localhost:8000/docs\n")
    
    uvicorn.run(app, port=8000)