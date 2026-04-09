from typing import List, Dict
import json

class RAGEvaluator:
    def __init__(self, generator_client):
        self.llm = generator_client.llm

    def evaluate_faithfulness(self, question: str, answer: str, context: List[str]) -> Dict:
        """Evaluates if the answer is grounded in the context."""
        context_text = "\n\n".join(context)
        prompt = f"""
        Evaluate the following answer for 'Faithfulness' based on the provided context.
        An answer is faithful if all its claims can be inferred from the context.
        
        Context: {context_text}
        Question: {question}
        Answer: {answer}
        
        Provide a JSON response with:
        - score: 1 (faithful) or 0 (unfaithful)
        - reasoning: Short explanation
        """
        response = self.llm.invoke(prompt)
        # Simple extraction logic for JSON from raw output
        try:
            # Look for JSON pattern
            json_str = response.content[response.content.find("{"):response.content.rfind("}")+1]
            return json.loads(json_str)
        except:
            return {"score": 0.5, "reasoning": "Could not parse evaluation response"}

    def evaluate_relevance(self, question: str, answer: str) -> Dict:
        """Evaluates if the answer addresses the question intent."""
        prompt = f"""
        Evaluate the following answer for 'Relevance' to the question.
        
        Question: {question}
        Answer: {answer}
        
        Provide a JSON response with:
        - score: 1 (relevant) or 0 (irrelevant)
        - reasoning: Short explanation
        """
        response = self.llm.invoke(prompt)
        try:
            json_str = response.content[response.content.find("{"):response.content.rfind("}")+1]
            return json.loads(json_str)
        except:
            return {"score": 0.5, "reasoning": "Could not parse evaluation response"}

    def run_full_eval(self, question: str, answer: str, context: List[str]) -> Dict:
        return {
            "faithfulness": self.evaluate_faithfulness(question, answer, context),
            "relevance": self.evaluate_relevance(question, answer)
        }
