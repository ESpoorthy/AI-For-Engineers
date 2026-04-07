"""
Enhanced Mathematical Reasoning Model for AI for Engineers
Specialized for step-by-step mathematical problem solving
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import re
from typing import List, Dict, Tuple


class MathematicalReasoningLayer(layers.Layer):
    """
    Custom layer for mathematical reasoning patterns
    Helps the model understand mathematical structures and relationships
    """
    
    def __init__(self, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        
        # Mathematical pattern recognition
        self.equation_attention = layers.MultiHeadAttention(
            num_heads=4, key_dim=embed_dim // 4, name='equation_attention'
        )
        
        # Step sequence modeling
        self.step_lstm = layers.LSTM(embed_dim // 2, return_sequences=True, name='step_lstm')
        
        # Mathematical operation classification
        self.operation_classifier = layers.Dense(32, activation='relu', name='operation_classifier')
        
        # Layer normalization
        self.layer_norm = layers.LayerNormalization(epsilon=1e-6)
        
    def call(self, x, training=False):
        # Apply mathematical pattern attention
        math_attention = self.equation_attention(x, x, training=training)
        
        # Process step sequences
        step_features = self.step_lstm(x, training=training)
        
        # Combine features
        combined = x + math_attention + step_features
        
        # Apply operation classification
        operation_features = self.operation_classifier(combined)
        
        # Normalize and return
        return self.layer_norm(combined + operation_features)
    
    def get_config(self):
        config = super().get_config()
        config.update({'embed_dim': self.embed_dim})
        return config


class EnhancedMathTransformer(keras.Model):
    """
    Enhanced transformer model specifically designed for mathematical reasoning
    Provides superior step-by-step explanations compared to general models
    """
    
    def __init__(self, vocab_size, max_length=1024, embed_dim=512, 
                 num_heads=16, ff_dim=2048, num_layers=12, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        
        # Enhanced token embedding with mathematical symbols
        self.token_embedding = layers.Embedding(
            input_dim=vocab_size,
            output_dim=embed_dim,
            embeddings_initializer='glorot_uniform',
            mask_zero=True,
            name='token_embedding'
        )
        
        # Positional encoding for longer sequences
        self.pos_encoding = self._create_positional_encoding()
        
        # Mathematical reasoning layers
        self.math_reasoning_layers = [
            MathematicalReasoningLayer(embed_dim, name=f'math_reasoning_{i}')
            for i in range(2)  # Add 2 specialized math layers
        ]
        
        # Enhanced transformer blocks
        self.transformer_blocks = [
            self._create_transformer_block(i) for i in range(num_layers)
        ]
        
        # Step-by-step generation head
        self.step_generator = layers.Dense(embed_dim, activation='gelu', name='step_generator')
        
        # Mathematical concept classifier
        self.concept_classifier = layers.Dense(64, activation='relu', name='concept_classifier')
        
        # Final output layer
        self.output_layer = layers.Dense(vocab_size, name='output_layer')
        
        # Dropout for regularization
        self.dropout = layers.Dropout(dropout_rate)
        
    def _create_positional_encoding(self):
        """Create enhanced positional encoding for mathematical sequences"""
        position = np.arange(self.max_length)[:, np.newaxis]
        div_term = np.exp(np.arange(0, self.embed_dim, 2) * -(np.log(10000.0) / self.embed_dim))
        
        pos_encoding = np.zeros((self.max_length, self.embed_dim))
        pos_encoding[:, 0::2] = np.sin(position * div_term)
        pos_encoding[:, 1::2] = np.cos(position * div_term)
        
        return tf.constant(pos_encoding[np.newaxis, :, :], dtype=tf.float32)
    
    def _create_transformer_block(self, block_id):
        """Create enhanced transformer block with mathematical reasoning"""
        return keras.Sequential([
            layers.MultiHeadAttention(
                num_heads=self.num_heads,
                key_dim=self.embed_dim // self.num_heads,
                dropout=0.1,
                name=f'attention_{block_id}'
            ),
            layers.LayerNormalization(epsilon=1e-6, name=f'norm1_{block_id}'),
            layers.Dense(self.ff_dim, activation='gelu', name=f'ffn1_{block_id}'),
            layers.Dropout(0.1, name=f'dropout1_{block_id}'),
            layers.Dense(self.embed_dim, name=f'ffn2_{block_id}'),
            layers.LayerNormalization(epsilon=1e-6, name=f'norm2_{block_id}'),
        ], name=f'transformer_block_{block_id}')
    
    def call(self, x, training=False):
        seq_len = tf.shape(x)[1]
        
        # Token embedding with scaling
        x = self.token_embedding(x)
        x = x * tf.math.sqrt(tf.cast(self.embed_dim, tf.float32))
        
        # Add positional encoding
        x = x + self.pos_encoding[:, :seq_len, :]
        x = self.dropout(x, training=training)
        
        # Apply mathematical reasoning layers
        for math_layer in self.math_reasoning_layers:
            x = math_layer(x, training=training)
        
        # Apply transformer blocks with residual connections
        for i, transformer_block in enumerate(self.transformer_blocks):
            # Multi-head attention
            attn_output = transformer_block.layers[0](x, x, training=training)
            x = transformer_block.layers[1](x + attn_output)
            
            # Feed-forward network
            ffn_output = transformer_block.layers[2](x)
            ffn_output = transformer_block.layers[3](ffn_output, training=training)
            ffn_output = transformer_block.layers[4](ffn_output)
            x = transformer_block.layers[5](x + ffn_output)
        
        # Apply step generation enhancement
        x = self.step_generator(x)
        
        # Apply concept classification
        concept_features = self.concept_classifier(x)
        x = x + concept_features
        
        # Generate final logits
        return self.output_layer(x)
    
    def get_config(self):
        return {
            'vocab_size': self.vocab_size,
            'max_length': self.max_length,
            'embed_dim': self.embed_dim,
            'num_heads': self.num_heads,
            'ff_dim': self.ff_dim,
            'num_layers': self.num_layers
        }


class MathematicalInferenceEngine:
    """
    Advanced inference engine for mathematical problem solving
    Provides structured, step-by-step solutions with explanations
    """
    
    def __init__(self, model, tokenizer, max_length=1024):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Mathematical operation patterns
        self.math_patterns = {
            'integration': r'∫|integrate|integral',
            'differentiation': r'd/dx|derivative|differentiate',
            'equation': r'solve|equation|=',
            'matrix': r'matrix|determinant|eigenvalue',
            'probability': r'probability|P\(|statistics',
            'geometry': r'triangle|circle|angle|area|volume',
            'algebra': r'factor|expand|simplify|polynomial'
        }
        
        # Step indicators
        self.step_indicators = [
            "First, let's identify",
            "Step 1:",
            "Next, we",
            "Then, we",
            "Now, let's",
            "Finally,",
            "Therefore,",
            "In conclusion,"
        ]
    
    def identify_problem_type(self, question: str) -> str:
        """Identify the type of mathematical problem"""
        question_lower = question.lower()
        
        for problem_type, pattern in self.math_patterns.items():
            if re.search(pattern, question_lower):
                return problem_type
        
        return 'general'
    
    def generate_structured_solution(self, question: str, max_steps: int = 10) -> Dict:
        """
        Generate a structured, step-by-step mathematical solution
        
        Args:
            question: Mathematical question to solve
            max_steps: Maximum number of steps to generate
            
        Returns:
            Dictionary with structured solution
        """
        try:
            # Identify problem type
            problem_type = self.identify_problem_type(question)
            
            # Create enhanced prompt for mathematical reasoning
            enhanced_prompt = self._create_math_prompt(question, problem_type)
            
            # Generate solution
            solution = self._generate_with_reasoning(enhanced_prompt, max_steps)
            
            # Structure the response
            structured_solution = self._structure_solution(solution, problem_type)
            
            return {
                'success': True,
                'question': question,
                'problem_type': problem_type,
                'solution': structured_solution['explanation'],
                'steps': structured_solution['steps'],
                'mathematical_concepts': structured_solution['concepts'],
                'verification': structured_solution.get('verification', None)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error generating solution: {str(e)}",
                'question': question
            }
    
    def _create_math_prompt(self, question: str, problem_type: str) -> str:
        """Create an enhanced prompt for mathematical reasoning"""
        
        type_specific_prompts = {
            'integration': "Solve this integration problem step by step, showing all work:",
            'differentiation': "Find the derivative step by step, explaining each rule used:",
            'equation': "Solve this equation systematically, showing each algebraic step:",
            'matrix': "Solve this matrix problem step by step, showing all calculations:",
            'probability': "Solve this probability problem step by step, explaining the reasoning:",
            'geometry': "Solve this geometry problem step by step, showing all measurements and formulas:",
            'algebra': "Solve this algebra problem step by step, showing all algebraic manipulations:",
            'general': "Solve this mathematical problem step by step, providing clear explanations:"
        }
        
        prompt = type_specific_prompts.get(problem_type, type_specific_prompts['general'])
        
        return f"""
{prompt}

Question: {question}

Solution:
Step 1: Let me analyze what we're asked to find and identify the key information.
"""
    
    def _generate_with_reasoning(self, prompt: str, max_steps: int) -> str:
        """Generate solution with enhanced mathematical reasoning"""
        
        # Tokenize the prompt
        input_sequence = self.tokenizer.texts_to_sequences([prompt])[0]
        
        # Pad sequence
        input_padded = keras.preprocessing.sequence.pad_sequences(
            [input_sequence], maxlen=self.max_length, padding='post'
        )
        
        # Generate tokens with enhanced sampling
        generated_tokens = input_padded[0].tolist()
        
        step_count = 0
        for _ in range(500):  # Maximum generation length
            # Prepare current input
            current_input = np.array([generated_tokens[-self.max_length:]])
            
            # Get model predictions
            predictions = self.model(current_input, training=False)
            next_token_logits = predictions[0, -1, :]
            
            # Enhanced sampling for mathematical coherence
            next_token = self._sample_mathematical_token(next_token_logits)
            
            if next_token == 0:  # End token
                break
                
            generated_tokens.append(int(next_token))
            
            # Count steps and limit generation
            decoded_text = self._decode_tokens(generated_tokens)
            current_steps = decoded_text.lower().count('step ')
            
            if current_steps >= max_steps:
                break
        
        return self._decode_tokens(generated_tokens)
    
    def _sample_mathematical_token(self, logits: tf.Tensor, temperature: float = 0.8) -> int:
        """Enhanced sampling for mathematical coherence"""
        
        # Apply temperature
        logits = logits / temperature
        
        # Top-k sampling with mathematical bias
        top_k = 40
        top_k_indices = tf.math.top_k(logits, k=top_k).indices
        top_k_logits = tf.gather(logits, top_k_indices)
        
        # Apply softmax
        probabilities = tf.nn.softmax(top_k_logits)
        
        # Sample
        next_token_idx = np.random.choice(top_k, p=probabilities.numpy())
        return top_k_indices[next_token_idx].numpy()
    
    def _decode_tokens(self, tokens: List[int]) -> str:
        """Decode tokens back to text"""
        reverse_word_index = {v: k for k, v in self.tokenizer.word_index.items()}
        
        words = []
        for token in tokens:
            if token != 0:
                word = reverse_word_index.get(token, '<UNK>')
                words.append(word)
        
        return ' '.join(words)
    
    def _structure_solution(self, solution: str, problem_type: str) -> Dict:
        """Structure the generated solution into organized components"""
        
        # Extract steps
        steps = self._extract_steps(solution)
        
        # Extract mathematical concepts
        concepts = self._extract_concepts(solution, problem_type)
        
        # Clean up the explanation
        explanation = self._clean_explanation(solution)
        
        return {
            'explanation': explanation,
            'steps': steps,
            'concepts': concepts,
            'verification': self._generate_verification(solution, problem_type)
        }
    
    def _extract_steps(self, solution: str) -> List[str]:
        """Extract numbered steps from the solution"""
        steps = []
        
        # Split by step indicators
        lines = solution.split('\n')
        current_step = ""
        
        for line in lines:
            line = line.strip()
            
            # Check if this line starts a new step
            if re.match(r'^Step \d+:', line) or any(indicator in line for indicator in self.step_indicators):
                if current_step:
                    steps.append(current_step.strip())
                current_step = line
            elif current_step and line:
                current_step += " " + line
        
        # Add the last step
        if current_step:
            steps.append(current_step.strip())
        
        return steps[:10]  # Limit to 10 steps for clarity
    
    def _extract_concepts(self, solution: str, problem_type: str) -> List[str]:
        """Extract mathematical concepts mentioned in the solution"""
        concepts = []
        
        concept_keywords = {
            'integration': ['integration by parts', 'substitution', 'partial fractions', 'definite integral'],
            'differentiation': ['chain rule', 'product rule', 'quotient rule', 'implicit differentiation'],
            'equation': ['linear equation', 'quadratic formula', 'factoring', 'substitution method'],
            'matrix': ['determinant', 'inverse matrix', 'eigenvalues', 'matrix multiplication'],
            'probability': ['conditional probability', 'bayes theorem', 'independence', 'distribution'],
            'geometry': ['pythagorean theorem', 'area formula', 'volume formula', 'trigonometry'],
            'algebra': ['factoring', 'expanding', 'simplifying', 'polynomial division']
        }
        
        solution_lower = solution.lower()
        
        for concept in concept_keywords.get(problem_type, []):
            if concept in solution_lower:
                concepts.append(concept.title())
        
        return concepts
    
    def _clean_explanation(self, solution: str) -> str:
        """Clean and format the explanation"""
        # Remove the prompt part
        if "Solution:" in solution:
            solution = solution.split("Solution:")[1]
        
        # Clean up formatting
        solution = re.sub(r'\s+', ' ', solution)  # Multiple spaces to single
        solution = solution.strip()
        
        return solution
    
    def _generate_verification(self, solution: str, problem_type: str) -> str:
        """Generate a verification step for the solution"""
        verification_templates = {
            'integration': "To verify: Differentiate the result to check if we get the original integrand.",
            'differentiation': "To verify: Check the derivative using the definition or alternative methods.",
            'equation': "To verify: Substitute the solution back into the original equation.",
            'matrix': "To verify: Check the calculations using matrix properties and definitions.",
            'probability': "To verify: Ensure probabilities sum to 1 and satisfy probability axioms.",
            'geometry': "To verify: Check that the solution satisfies geometric constraints and formulas.",
            'algebra': "To verify: Substitute values back into the original expression to confirm."
        }
        
        return verification_templates.get(problem_type, "To verify: Check the solution using alternative methods or substitution.")