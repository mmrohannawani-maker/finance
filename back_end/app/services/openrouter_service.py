import httpx
import json
from typing import List, Dict, Any
from app.config import settings

class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
    
    async def analyze_data(self, data: List[Dict[str, Any]], query: str = None) -> Dict[str, Any]:
        """Send data to OpenRouter for analysis"""
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
        
        # Prepare prompt
        if not query:
            query = """
            Analyze this financial data and provide insights on:
            1. Key trends and patterns
            2. Anomalies or outliers
            3. Recommendations
            4. Summary statistics
            """
        
        # Format data for prompt
        data_str = json.dumps(data[:100], indent=2)  # Limit to first 100 rows
        
        prompt = f"""
        {query}
        
        Here is the data:
        {data_str}
        
        Provide your analysis in a structured format with clear sections.
        """
        
        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",  # Your site URL
                    "X-Title": "Financial Analysis Tool"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a financial data analyst expert. Analyze the given data and provide clear, actionable insights."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def generate_chart_suggestions(self, columns: List[str], data_sample: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Suggest best chart types for the data"""
        prompt = f"""
        Based on the following data columns and sample, suggest the best chart types for visualization:
        
        Columns: {columns}
        
        Sample data (first 5 rows):
        {json.dumps(data_sample[:5], indent=2)}
        
        For each suggested chart, provide:
        1. Chart type (bar, line, pie, scatter, etc.)
        2. X and Y axis columns
        3. Reason why this chart is suitable
        4. Any data transformations needed
        
        Respond in JSON format.
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 1000
                }
            )
            
            result = response.json()
            return json.loads(result["choices"][0]["message"]["content"])
