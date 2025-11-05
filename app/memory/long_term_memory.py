"""
Long-term semantic memory using ChromaDB with embeddings
Retrieves semantically similar past conversations, summaries, and profile facts
"""

import os
import uuid
import hashlib
import math
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

import chromadb
from chromadb.config import Settings
from utils.timezone_utils import now_central
from app.database.crud import ConversationCRUD

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Manages long-term semantic memory using ChromaDB embeddings"""
    
    def __init__(self, storage_path: str = "data/vectors", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize long-term memory system with ChromaDB
        
        Args:
            storage_path: Path to store vector database
            embedding_model: SentenceTransformers model name (default: all-MiniLM-L6-v2)
        """
        self.storage_path = storage_path
        self.embedding_model = embedding_model
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=storage_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Try to use SentenceTransformer embedding function
        # Falls back to ChromaDB default if sentence-transformers is unavailable
        try:
            from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
            embedding_function = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        except (ImportError, ValueError):
            # Fallback to default embedding function
            embedding_function = None
            logger.info("Using ChromaDB default embedding (sentence-transformers not available)")
        
        # Get or create collection with configured embedding function
        self.collection = self.client.get_or_create_collection(
            name="carely_memory",
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_function
        )
        
        self.last_update = None
        self.max_raw_per_user = 200  # Hygiene: cap raw conversations per user
    
    def _compute_content_hash(self, text: str) -> str:
        """Compute hash for deduplication"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def add_conversation(self, user_id: int, conversation_id: int, 
                        user_message: str, assistant_response: str, 
                        timestamp: datetime, title: str = None, tags: List[str] = None) -> None:
        """
        Add a single conversation to the vector store (incremental update)
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID from database
            user_message: User's message
            assistant_response: Assistant's response
            timestamp: Timestamp of conversation
            title: Optional title/summary for the conversation
            tags: Optional tags for categorization
        """
        try:
            # Combine user message and response for richer context
            combined_text = f"{user_message} {assistant_response}"
            
            # Compute content hash for deduplication
            content_hash = self._compute_content_hash(combined_text)
            
            # Create unique ID for this entry
            doc_id = f"user_{user_id}_conv_{conversation_id}"
            
            # Standardized metadata
            metadata = {
                "user_id": str(user_id),  # Store as string for ChromaDB consistency
                "type": "conversation",
                "timestamp_utc": timestamp.isoformat(),
                "title": title or f"Conversation {conversation_id}",
                "tags": ",".join(tags) if tags else "",
                "content_hash": content_hash,
                "source_id": conversation_id,
                "user_message": user_message[:200],
                "assistant_response": assistant_response[:200]
            }
            
            # Add to collection
            self.collection.upsert(
                ids=[doc_id],
                documents=[combined_text],
                metadatas=[metadata]
            )
            
        except Exception as e:
            logger.error(f"Error adding conversation to vector store: {e}")
    
    def add_summary(self, user_id: int, summary_text: str, date: datetime, 
                   key_topics: List[str] = None) -> None:
        """
        Add or update a daily summary in the vector store
        
        Args:
            user_id: User ID
            summary_text: Summary text (3-6 lines)
            date: Date of the summary
            key_topics: Optional list of key topics from the summary
        """
        try:
            # Keep summaries concise (≤2 sentences for retrieval)
            sentences = summary_text.split('.')[:2]
            concise_summary = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
            
            doc_id = f"user_{user_id}_summary_{date.strftime('%Y%m%d')}"
            
            # Standardized metadata for summaries
            metadata = {
                "user_id": str(user_id),  # Store as string for ChromaDB consistency
                "type": "summary",
                "timestamp_utc": date.isoformat(),
                "title": f"Daily Summary {date.strftime('%Y-%m-%d')}",
                "tags": ",".join(key_topics) if key_topics else "",
                "date": date.strftime('%Y-%m-%d'),
                "content_hash": self._compute_content_hash(concise_summary)
            }
            
            self.collection.upsert(
                ids=[doc_id],
                documents=[concise_summary],
                metadatas=[metadata]
            )
            
        except Exception as e:
            logger.error(f"Error adding summary to vector store: {e}")
    
    def add_profile_fact(self, user_id: int, fact: str, fact_type: str = "general", 
                        tags: List[str] = None) -> None:
        """
        Add a profile fact (preferences, meal times, etc.) to the vector store
        
        Args:
            user_id: User ID
            fact: One-liner fact about the user
            fact_type: Type of fact (e.g., "meal_time", "preference")
            tags: Optional tags for categorization
        """
        try:
            doc_id = f"user_{user_id}_fact_{fact_type}_{uuid.uuid4().hex[:8]}"
            
            # Standardized metadata
            metadata = {
                "user_id": str(user_id),  # Store as string for ChromaDB consistency
                "type": "profile_fact",
                "timestamp_utc": now_central().isoformat(),
                "title": f"{fact_type.replace('_', ' ').title()} fact",
                "tags": ",".join(tags) if tags else fact_type,
                "fact_type": fact_type,
                "content_hash": self._compute_content_hash(fact)
            }
            
            self.collection.upsert(
                ids=[doc_id],
                documents=[fact],
                metadatas=[metadata]
            )
            
        except Exception as e:
            logger.error(f"Error adding profile fact to vector store: {e}")
    
    def _calculate_recency_score(self, timestamp_str: str, half_life_days: float = 30.0) -> float:
        """
        Calculate recency score with exponential decay
        
        Args:
            timestamp_str: ISO timestamp string
            half_life_days: Number of days for 50% decay (default 30)
        
        Returns:
            Recency score between 0 and 1
        """
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            age_days = (now_central() - timestamp).total_seconds() / 86400.0
            decay_rate = math.log(2) / half_life_days
            return math.exp(-decay_rate * age_days)
        except:
            return 0.5  # Default mid-range score if parsing fails
    
    def retrieve_similar_conversations(self, query: str, user_id: int, 
                                      top_k: int = 7, exclude_query: str = None) -> List[Dict]:
        """
        Retrieve semantically similar past conversations with recency re-ranking
        Returns mix of 2 summaries + 3-5 raw snippets
        
        Args:
            query: User's current query
            user_id: User ID
            top_k: Total number of items to retrieve (default 7 for 2 summaries + 5 snippets)
            exclude_query: Query text to exclude from results
        
        Returns:
            List of similar items (conversations, summaries, facts) with recency re-ranking
        """
        try:
            # Query the collection - get more candidates for filtering
            results = self.collection.query(
                query_texts=[query],
                n_results=min(top_k * 3, 30),
                where={"user_id": str(user_id)}  # Ensure string for ChromaDB filtering
            )
            
            if not results or not results['ids'] or not results['ids'][0]:
                return []
            
            # First pass: collect and score all items
            candidates = []
            exclude_lower = exclude_query.lower().strip() if exclude_query else ""
            
            for idx, doc_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][idx]
                document = results['documents'][0][idx]
                distance = results['distances'][0][idx] if 'distances' in results else 0.5
                
                # Skip if too similar to current query (avoid echoing)
                if exclude_query and metadata.get('user_message', '').lower().strip() == exclude_lower:
                    continue
                if distance < 0.05:  # Very low distance = near duplicate
                    continue
                
                # Get timestamp for recency scoring
                timestamp_str = metadata.get('timestamp_utc') or metadata.get('timestamp', '')
                recency_score = self._calculate_recency_score(timestamp_str)
                
                # Semantic relevance (inverse of distance)
                semantic_score = 1.0 - distance
                
                # Combined score: 70% semantic, 30% recency
                combined_score = (semantic_score * 0.7) + (recency_score * 0.3)
                
                item_type = metadata.get('type', 'conversation')
                
                # Truncate to ≤2 sentences
                sentences = document.split('.')[:2]
                concise_text = '. '.join(s.strip() for s in sentences if s.strip())
                if concise_text and not concise_text.endswith('.'):
                    concise_text += '.'
                
                candidate = {
                    "type": item_type,
                    "text": concise_text,
                    "metadata": metadata,
                    "relevance": semantic_score,
                    "recency": recency_score,
                    "combined_score": combined_score,
                    "timestamp_str": timestamp_str
                }
                
                # Add type-specific fields
                if item_type == 'conversation':
                    candidate['user_message'] = metadata.get('user_message', '')
                    candidate['assistant_response'] = metadata.get('assistant_response', '')
                
                candidates.append(candidate)
            
            # Sort by combined score
            candidates.sort(key=lambda x: x['combined_score'], reverse=True)
            
            # Second pass: enforce mix ratio (2 summaries + 3-5 snippets)
            summaries = [c for c in candidates if c['type'] == 'summary'][:2]
            non_summaries = [c for c in candidates if c['type'] != 'summary'][:5]
            
            # Combine and re-sort
            final_items = summaries + non_summaries
            final_items.sort(key=lambda x: x['combined_score'], reverse=True)
            
            # Add timestamp objects for compatibility
            for item in final_items:
                if item['timestamp_str']:
                    try:
                        item['timestamp'] = datetime.fromisoformat(item['timestamp_str'])
                    except:
                        pass
            
            return final_items[:top_k]
            
        except Exception as e:
            logger.error(f"Error retrieving similar conversations: {e}")
            return []
    
    def get_formatted_similar_context(self, query: str, user_id: int, 
                                     top_k: int = 3) -> str:
        """
        Get formatted string of similar past context
        
        Args:
            query: Current user query
            user_id: User ID
            top_k: Number of items to retrieve (max 3)
        
        Returns:
            Formatted context string
        """
        similar_items = self.retrieve_similar_conversations(query, user_id, top_k)
        
        if not similar_items:
            return ""
        
        context_parts = []
        
        for item in similar_items:
            if item['type'] == 'conversation' and 'timestamp' in item:
                time_str = item['timestamp'].strftime('%B %d')
                context_parts.append(f"[{time_str}] {item['text']}")
            elif item['type'] == 'summary':
                date_str = item['metadata'].get('date', 'Recent')
                context_parts.append(f"[Summary {date_str}] {item['text']}")
            elif item['type'] == 'profile_fact':
                context_parts.append(f"[Profile] {item['text']}")
            else:
                context_parts.append(item['text'])
        
        return "\n".join(context_parts)
    
    def build_memory_index(self, user_id: int, limit: int = 100):
        """
        Build or rebuild the memory index from conversation history
        (For initial migration or full rebuild only)
        
        Args:
            user_id: User ID to build memory for
            limit: Maximum number of conversations to index
        """
        try:
            # Get recent conversations from database
            conversations = ConversationCRUD.get_user_conversations(user_id, limit=limit)
            
            if not conversations:
                return
            
            # Add each conversation to the vector store
            for conv in conversations:
                self.add_conversation(
                    user_id=user_id,
                    conversation_id=conv.id,
                    user_message=conv.message,
                    assistant_response=conv.response,
                    timestamp=conv.timestamp
                )
            
            self.last_update = now_central()
            logger.info(f"Indexed {len(conversations)} conversations for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error building memory index: {e}")
    
    def deduplicate_by_hash(self, user_id: int) -> int:
        """
        Remove duplicate entries based on content hash
        
        Args:
            user_id: User ID
        
        Returns:
            Number of duplicates removed
        """
        try:
            # Get all items for this user
            results = self.collection.get(
                where={"user_id": str(user_id)}  # Ensure string for ChromaDB filtering
            )
            
            if not results or not results['ids']:
                return 0
            
            # Track seen hashes
            seen_hashes = {}
            duplicates = []
            
            for idx, doc_id in enumerate(results['ids']):
                metadata = results['metadatas'][idx]
                content_hash = metadata.get('content_hash')
                
                if content_hash:
                    if content_hash in seen_hashes:
                        # This is a duplicate
                        duplicates.append(doc_id)
                    else:
                        seen_hashes[content_hash] = doc_id
            
            # Delete duplicates
            if duplicates:
                self.collection.delete(ids=duplicates)
                logger.info(f"Removed {len(duplicates)} duplicate entries for user {user_id}")
            
            return len(duplicates)
            
        except Exception as e:
            logger.error(f"Error deduplicating memory: {e}")
            return 0
    
    def cleanup_old_conversations(self, user_id: int, max_conversations: int = 200) -> int:
        """
        Keep only the most recent N raw conversations per user
        Preserves summaries and profile facts
        
        Args:
            user_id: User ID
            max_conversations: Maximum number of raw conversations to keep (default 200)
        
        Returns:
            Number of old conversations removed
        """
        try:
            # Get all conversations for this user
            results = self.collection.get(
                where={
                    "user_id": str(user_id),  # Ensure string for ChromaDB filtering
                    "type": "conversation"
                }
            )
            
            if not results or not results['ids']:
                return 0
            
            # Sort by timestamp (newest first)
            conversations = []
            for idx, doc_id in enumerate(results['ids']):
                metadata = results['metadatas'][idx]
                timestamp_str = metadata.get('timestamp_utc') or metadata.get('timestamp', '')
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except:
                    timestamp = datetime.min
                
                conversations.append({
                    'id': doc_id,
                    'timestamp': timestamp
                })
            
            conversations.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Keep only the most recent max_conversations
            if len(conversations) > max_conversations:
                old_conversations = conversations[max_conversations:]
                old_ids = [c['id'] for c in old_conversations]
                
                self.collection.delete(ids=old_ids)
                logger.info(f"Removed {len(old_ids)} old conversations for user {user_id}")
                return len(old_ids)
            
            return 0
            
        except Exception as e:
            logger.error(f"Error cleaning up old conversations: {e}")
            return 0
    
    def get_user_memory_items(self, user_id: int, memory_type: str = None, 
                             limit: int = 100) -> List[Dict]:
        """
        List memory items for a user (for management UI)
        
        Args:
            user_id: User ID
            memory_type: Filter by type (conversation, summary, profile_fact) or None for all
            limit: Maximum number of items to return
        
        Returns:
            List of memory items with metadata
        """
        try:
            where_clause = {"user_id": str(user_id)}  # Ensure string for ChromaDB filtering
            if memory_type:
                where_clause["type"] = memory_type
            
            results = self.collection.get(
                where=where_clause,
                limit=limit
            )
            
            if not results or not results['ids']:
                return []
            
            items = []
            for idx, doc_id in enumerate(results['ids']):
                metadata = results['metadatas'][idx]
                document = results['documents'][idx]
                
                items.append({
                    'id': doc_id,
                    'type': metadata.get('type', 'unknown'),
                    'title': metadata.get('title', 'Untitled'),
                    'text': document[:200] + '...' if len(document) > 200 else document,
                    'timestamp': metadata.get('timestamp_utc') or metadata.get('timestamp', ''),
                    'tags': metadata.get('tags', '')
                })
            
            # Sort by timestamp (newest first)
            items.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return items
            
        except Exception as e:
            logger.error(f"Error listing memory items: {e}")
            return []
    
    def delete_memory_item(self, doc_id: str) -> bool:
        """
        Delete a specific memory item by ID
        
        Args:
            doc_id: Document ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            logger.error(f"Error deleting memory item: {e}")
            return False
    
    def clear_user_memory(self, user_id: int):
        """
        Clear all memory for a specific user
        
        Args:
            user_id: User ID
        """
        try:
            # Query all documents for this user
            results = self.collection.get(
                where={"user_id": str(user_id)}  # Ensure string for ChromaDB filtering
            )
            
            if results and results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Cleared {len(results['ids'])} memory items for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error clearing user memory: {e}")
