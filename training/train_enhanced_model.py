"""
Enhanced Training Script for Mathematical Reasoning Model
Trains the model specifically for superior step-by-step mathematical explanations
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import os
from pathlib import Path
import pickle
from datetime import datetime

from enhanced_math_model import EnhancedMathTransformer
from data_pipeline import EngineeringDataPipeline


class EnhancedMathTrainer:
    """Enhanced trainer for mathematical reasoning model"""
    
    def __init__(self, config=None):
        self.config = config or self._get_default_config()
        self.model = None
        self.data_pipeline = None
        self.tokenizer = None
        
    def _get_default_config(self):
        """Get enhanced configuration for mathematical reasoning"""
        return {
            'vocab_size': 15000,      # Larger vocabulary for mathematical terms
            'max_length': 1024,       # Longer sequences for detailed explanations
            'embed_dim': 512,         # Larger embedding dimension
            'num_heads': 16,          # More attention heads
            'ff_dim': 2048,           # Larger feed-forward dimension
            'num_layers': 12,         # More transformer layers
            'dropout_rate': 0.1,
            'learning_rate': 0.0001,
            'batch_size': 4,          # Smaller batch size due to longer sequences
            'epochs': 50,             # More epochs for better learning
            'patience': 10,           # Early stopping patience
            'save_dir': 'models/enhanced_models'
        }
    
    def prepare_enhanced_dataset(self):
        """Prepare enhanced mathematical dataset"""
        print("Preparing enhanced mathematical dataset...")
        
        # Load comprehensive dataset
        dataset_path = Path('data/processed/comprehensive_math_dataset.json')
        if not dataset_path.exists():
            print("Comprehensive dataset not found. Creating it...")
            # Import and run the dataset generator
            import sys
            sys.path.append('data')
            from enhanced_math_dataset import MathDatasetGenerator
            
            generator = MathDatasetGenerator()
            dataset = generator.save_dataset(str(dataset_path))
        else:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
        
        print(f"Loaded {len(dataset)} mathematical problems")
        
        # Combine with existing datasets for more diversity
        existing_datasets = [
            'data/processed/engineering_math_dataset.json',
            'data/processed/training_data.json',
            'data/processed/calculus_problems.json',
            'data/processed/linear_algebra_problems.json'
        ]
        
        for dataset_file in existing_datasets:
            if Path(dataset_file).exists():
                with open(dataset_file, 'r', encoding='utf-8') as f:
                    additional_data = json.load(f)
                    dataset.extend(additional_data)
                    print(f"Added {len(additional_data)} problems from {dataset_file}")
        
        print(f"Total dataset size: {len(dataset)} problems")
        
        # Initialize data pipeline with enhanced configuration
        self.data_pipeline = EngineeringDataPipeline(
            vocab_size=self.config['vocab_size'],
            max_length=self.config['max_length']
        )
        
        # Prepare training data with enhanced formatting
        enhanced_dataset = self._enhance_training_format(dataset)
        
        # Process the data
        X, y, self.tokenizer = self.data_pipeline.prepare_training_data(enhanced_dataset)
        
        print(f"Processed training data shape: X={X.shape}, y={y.shape}")
        print(f"Vocabulary size: {len(self.tokenizer.word_index)}")
        
        return X, y
    
    def _enhance_training_format(self, dataset):
        """Enhance the training data format for better mathematical reasoning"""
        enhanced_data = []
        
        for item in dataset:
            question = item['question']
            answer = item['answer']
            
            # Create enhanced training format with mathematical context
            enhanced_text = f"""Mathematical Problem: {question}

Step-by-Step Solution:
{answer}

This solution demonstrates clear mathematical reasoning with detailed explanations for educational purposes."""
            
            enhanced_data.append({
                'question': question,
                'answer': enhanced_text
            })
        
        return enhanced_data
    
    def build_enhanced_model(self):
        """Build the enhanced mathematical reasoning model"""
        print("Building enhanced mathematical transformer model...")
        
        self.model = EnhancedMathTransformer(
            vocab_size=self.config['vocab_size'],
            max_length=self.config['max_length'],
            embed_dim=self.config['embed_dim'],
            num_heads=self.config['num_heads'],
            ff_dim=self.config['ff_dim'],
            num_layers=self.config['num_layers'],
            dropout_rate=self.config['dropout_rate']
        )
        
        # Build the model
        dummy_input = tf.ones((1, 10), dtype=tf.int32)
        _ = self.model(dummy_input)
        
        print(f"Model built with {self.model.count_params():,} parameters")
        
        # Compile with enhanced optimizer
        optimizer = keras.optimizers.AdamW(
            learning_rate=self.config['learning_rate'],
            weight_decay=0.01,  # L2 regularization
            clipnorm=1.0        # Gradient clipping
        )
        
        self.model.compile(
            optimizer=optimizer,
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy', 'sparse_top_k_categorical_accuracy']
        )
        
        return self.model
    
    def create_enhanced_callbacks(self):
        """Create enhanced callbacks for training"""
        
        # Create save directory
        save_dir = Path(self.config['save_dir'])
        save_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        callbacks = [
            # Model checkpointing with enhanced monitoring
            keras.callbacks.ModelCheckpoint(
                filepath=save_dir / f'enhanced_model_checkpoint_{timestamp}.weights.h5',
                monitor='val_loss',
                save_best_only=True,
                save_weights_only=True,
                verbose=1
            ),
            
            # Early stopping with patience
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config['patience'],
                restore_best_weights=True,
                verbose=1
            ),
            
            # Learning rate reduction
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            
            # TensorBoard logging
            keras.callbacks.TensorBoard(
                log_dir=f'logs/enhanced_training_{timestamp}',
                histogram_freq=1,
                write_graph=True,
                update_freq='epoch'
            ),
            
            # CSV logging
            keras.callbacks.CSVLogger(
                filename=save_dir / f'enhanced_training_log_{timestamp}.csv',
                append=True
            )
        ]
        
        return callbacks
    
    def train_enhanced_model(self):
        """Train the enhanced mathematical reasoning model"""
        print("Starting enhanced mathematical model training...")
        
        # Prepare dataset
        X, y = self.prepare_enhanced_dataset()
        
        # Build model
        self.build_enhanced_model()
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Validation set: {X_val.shape[0]} samples")
        
        # Create callbacks
        callbacks = self.create_enhanced_callbacks()
        
        # Train the model
        print("Training enhanced mathematical reasoning model...")
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=self.config['epochs'],
            batch_size=self.config['batch_size'],
            callbacks=callbacks,
            verbose=1
        )
        
        # Save the final model
        self.save_enhanced_model()
        
        print("Enhanced mathematical model training completed!")
        return history
    
    def save_enhanced_model(self):
        """Save the enhanced model and configuration"""
        save_dir = Path(self.config['save_dir'])
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model weights
        weights_path = save_dir / 'enhanced_model_weights.weights.h5'
        self.model.save_weights(str(weights_path))
        print(f"Model weights saved to {weights_path}")
        
        # Save model configuration
        config_path = save_dir / 'enhanced_model_config.json'
        model_config = {
            'vocab_size': self.config['vocab_size'],
            'max_length': self.config['max_length'],
            'embed_dim': self.config['embed_dim'],
            'num_heads': self.config['num_heads'],
            'ff_dim': self.config['ff_dim'],
            'num_layers': self.config['num_layers'],
            'dropout_rate': self.config['dropout_rate'],
            'model_type': 'EnhancedMathTransformer',
            'training_date': datetime.now().isoformat(),
            'total_parameters': self.model.count_params()
        }
        
        with open(config_path, 'w') as f:
            json.dump(model_config, f, indent=2)
        print(f"Model configuration saved to {config_path}")
        
        # Save tokenizer
        tokenizer_path = save_dir / 'enhanced_tokenizer.pkl'
        with open(tokenizer_path, 'wb') as f:
            pickle.dump(self.tokenizer, f)
        print(f"Tokenizer saved to {tokenizer_path}")
        
        # Copy to main models directory for API compatibility
        main_models_dir = Path('models/saved_models')
        main_models_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files to main directory
        import shutil
        shutil.copy2(weights_path, main_models_dir / 'model_weights.weights.h5')
        shutil.copy2(config_path, main_models_dir / 'enhanced_model_config.json')
        shutil.copy2(tokenizer_path, main_models_dir / 'tokenizer.pkl')
        
        print("Enhanced model files copied to main models directory for API use")
    
    def evaluate_model(self, test_questions=None):
        """Evaluate the enhanced model on test questions"""
        if test_questions is None:
            test_questions = [
                "Find the integral of x² + 3x - 2 dx",
                "Solve the quadratic equation 2x² - 5x + 2 = 0",
                "Find the derivative of sin(x²) using the chain rule",
                "Calculate the determinant of the 2x2 matrix [[3, 1], [2, 4]]"
            ]
        
        print("\nEvaluating enhanced mathematical model:")
        print("=" * 50)
        
        from enhanced_math_model import MathematicalInferenceEngine
        
        inference_engine = MathematicalInferenceEngine(
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=self.config['max_length']
        )
        
        for i, question in enumerate(test_questions, 1):
            print(f"\nTest {i}: {question}")
            print("-" * 40)
            
            try:
                result = inference_engine.generate_structured_solution(question)
                
                if result['success']:
                    print(f"Problem Type: {result['problem_type']}")
                    print(f"Solution: {result['solution'][:200]}...")
                    print(f"Steps: {len(result['steps'])} steps identified")
                else:
                    print(f"Error: {result['error']}")
                    
            except Exception as e:
                print(f"Evaluation error: {e}")


def main():
    """Main training function"""
    print("Enhanced Mathematical Reasoning Model Training")
    print("=" * 50)
    
    # Enhanced configuration for superior mathematical reasoning
    config = {
        'vocab_size': 15000,
        'max_length': 1024,
        'embed_dim': 512,
        'num_heads': 16,
        'ff_dim': 2048,
        'num_layers': 12,
        'dropout_rate': 0.1,
        'learning_rate': 0.0001,
        'batch_size': 4,
        'epochs': 50,
        'patience': 10,
        'save_dir': 'models/enhanced_models'
    }
    
    # Initialize trainer
    trainer = EnhancedMathTrainer(config)
    
    # Train the model
    history = trainer.train_enhanced_model()
    
    # Evaluate the model
    trainer.evaluate_model()
    
    print("\n🎉 Enhanced Mathematical AI Assistant training completed!")
    print("🧮 Your model is now ready to provide superior step-by-step mathematical explanations!")
    print("🚀 Start the enhanced API with: python api/enhanced_math_api.py")


if __name__ == "__main__":
    main()