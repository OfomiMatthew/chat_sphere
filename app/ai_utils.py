"""
AI Utilities for ChatSphere
Handles all Groq API integrations for AI features
"""
from groq import Groq
from flask import current_app
import json
import re

def get_groq_client():
    """Initialize and return Groq client"""
    api_key = current_app.config.get('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY not configured")
    return Groq(api_key=api_key)

def chat_with_ai(messages, model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=1024):
    """
    Send messages to Groq AI and get response
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Groq model to use
        temperature: Response randomness (0-2)
        max_tokens: Max response length
    Returns:
        AI response text
    """
    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_smart_replies(message_history, num_replies=3):
    """
    Generate smart reply suggestions based on conversation history
    Args:
        message_history: List of recent messages
        num_replies: Number of suggestions to generate
    Returns:
        List of suggested replies
    """
    context = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in message_history[-10:]])
    
    prompt = f"""Based on this conversation, generate {num_replies} short, natural reply suggestions (max 10 words each).
Return ONLY a JSON array of strings, nothing else.

Conversation:
{context}

Reply suggestions:"""
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates short, contextual reply suggestions."},
            {"role": "user", "content": prompt}
        ]
        response = chat_with_ai(messages, temperature=0.8, max_tokens=200)
        
        # Extract JSON array from response
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            replies = json.loads(json_match.group())
            return replies[:num_replies]
        return ["Thanks!", "Got it!", "Sure thing!"]
    except Exception as e:
        print(f"Smart reply error: {e}")
        return ["Thanks!", "Got it!", "Sure thing!"]

def translate_message(text, target_language):
    """
    Translate message to target language
    Args:
        text: Message to translate
        target_language: Target language name or code
    Returns:
        Translated text
    """
    try:
        messages = [
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}. Return ONLY the translation, nothing else."},
            {"role": "user", "content": text}
        ]
        return chat_with_ai(messages, temperature=0.3, max_tokens=500)
    except Exception as e:
        return f"Translation error: {str(e)}"

def enhance_message(text, tone="professional"):
    """
    Improve message with specified tone
    Args:
        text: Original message
        tone: Desired tone (professional, casual, friendly, formal)
    Returns:
        Enhanced message
    """
    tone_instructions = {
        "professional": "Make this message more professional and polished while keeping the same meaning.",
        "casual": "Make this message more casual and relaxed while keeping the same meaning.",
        "friendly": "Make this message more warm and friendly while keeping the same meaning.",
        "formal": "Make this message more formal and respectful while keeping the same meaning.",
        "concise": "Make this message shorter and more concise while keeping the key points."
    }
    
    instruction = tone_instructions.get(tone, tone_instructions["professional"])
    
    try:
        messages = [
            {"role": "system", "content": f"{instruction} Return ONLY the improved message, nothing else."},
            {"role": "user", "content": text}
        ]
        return chat_with_ai(messages, temperature=0.7, max_tokens=500)
    except Exception as e:
        return f"Enhancement error: {str(e)}"

def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using Groq Whisper
    Args:
        audio_file_path: Path to audio file
    Returns:
        Transcription text
    """
    try:
        client = get_groq_client()
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
                language="en"
            )
        return transcription.text
    except Exception as e:
        return f"Transcription error: {str(e)}"

def moderate_content(text):
    """
    Check if message content is appropriate
    Args:
        text: Message to moderate
    Returns:
        Dict with 'is_safe' (bool), 'reason' (str), and 'filtered_text' (str)
    """
    try:
        messages = [
            {"role": "system", "content": """You are a content moderator. Analyze if the text contains:
- Hate speech or discrimination
- Explicit sexual content
- Violence or threats
- Spam or scams
- Personal attacks

Return ONLY a JSON object with this exact format:
{"is_safe": true/false, "reason": "brief reason or empty string", "filtered_text": "text with filtered words or original text"}"""},
            {"role": "user", "content": text}
        ]
        response = chat_with_ai(messages, temperature=0.3, max_tokens=300)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        return {"is_safe": True, "reason": "", "filtered_text": text}
    except Exception as e:
        print(f"Moderation error: {e}")
        return {"is_safe": True, "reason": "", "filtered_text": text}

def analyze_sentiment(text):
    """
    Analyze message sentiment
    Args:
        text: Message to analyze
    Returns:
        Dict with 'sentiment' (positive/negative/neutral), 'confidence' (0-1), 'emoji' (str)
    """
    try:
        messages = [
            {"role": "system", "content": """Analyze the sentiment of the text. Return ONLY a JSON object:
{"sentiment": "positive/negative/neutral", "confidence": 0.0-1.0, "emoji": "appropriate emoji"}"""},
            {"role": "user", "content": text}
        ]
        response = chat_with_ai(messages, temperature=0.3, max_tokens=100)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        return {"sentiment": "neutral", "confidence": 0.5, "emoji": "😐"}
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"sentiment": "neutral", "confidence": 0.5, "emoji": "😐"}

def summarize_conversation(messages, max_length=200):
    """
    Generate conversation summary
    Args:
        messages: List of message dicts
        max_length: Max summary length in words
    Returns:
        Summary text
    """
    conversation = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in messages])
    
    try:
        prompt_messages = [
            {"role": "system", "content": f"Summarize this conversation in {max_length} words or less. Include key points and action items."},
            {"role": "user", "content": conversation}
        ]
        return chat_with_ai(prompt_messages, temperature=0.5, max_tokens=500)
    except Exception as e:
        return f"Summary error: {str(e)}"

def smart_search(query, messages):
    """
    Semantic search through messages
    Args:
        query: Search query
        messages: List of message dicts to search
    Returns:
        List of relevant messages with scores
    """
    conversation = "\n".join([f"[{i}] {msg['sender']}: {msg['content']}" for i, msg in enumerate(messages)])
    
    try:
        prompt_messages = [
            {"role": "system", "content": """Find messages relevant to the query. Return ONLY a JSON array of message indices (numbers), ordered by relevance.
Example: [5, 12, 3, 8]"""},
            {"role": "user", "content": f"Query: {query}\n\nMessages:\n{conversation}"}
        ]
        response = chat_with_ai(prompt_messages, temperature=0.3, max_tokens=200)
        
        # Extract JSON array
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            indices = json.loads(json_match.group())
            return [messages[i] for i in indices if 0 <= i < len(messages)]
        return []
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_ai_response(user_message, conversation_history=None):
    """
    Get AI assistant response for chat bot
    Args:
        user_message: User's message
        conversation_history: Previous messages for context
    Returns:
        AI response
    """
    messages = [
        {"role": "system", "content": """You are ChatSphere AI, a helpful and friendly AI assistant integrated into a chat application. 
You can help with:
- Answering questions
- Providing recommendations
- Explaining concepts
- Creative writing
- Problem solving
- And general conversation

Be conversational, helpful, and concise. Use emojis occasionally to be friendly."""}
    ]
    
    if conversation_history:
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            role = "assistant" if msg.get('is_ai') else "user"
            messages.append({"role": role, "content": msg['content']})
    
    messages.append({"role": "user", "content": user_message})
    
    return chat_with_ai(messages, temperature=0.8, max_tokens=1000)

def autocomplete_text(partial_text, context=""):
    """
    Generate text completion suggestions
    Args:
        partial_text: Incomplete text to complete
        context: Previous conversation context
    Returns:
        List of completion suggestions
    """
    try:
        messages = [
            {"role": "system", "content": "Complete the partial message naturally. Return ONLY a JSON array of 3 completion suggestions (complete sentences)."},
            {"role": "user", "content": f"Context: {context}\n\nPartial message: {partial_text}\n\nCompletions:"}
        ]
        response = chat_with_ai(messages, temperature=0.8, max_tokens=200)
        
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            completions = json.loads(json_match.group())
            return completions[:3]
        return []
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return []
