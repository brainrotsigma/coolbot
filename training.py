import os
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPT2Config,
    AdamW,
    get_linear_schedule_with_warmup,
)
from tqdm import tqdm
from typing import List, Dict, Any

from config import JasonConfig


class RedditDataset(Dataset):
    def __init__(self, data_file: str, tokenizer, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = []
        
        print(f"\nLoading data from {data_file}...")
        
        with open(data_file, 'r') as f:
            for line in tqdm(f, desc="Processing data"):
                try:
                    item = json.loads(line)
                    text = self._format_item(item)
                    if text:
                        self.examples.append(text)
                except Exception:
                    pass
        
        print(f"Loaded {len(self.examples):,} examples")
    
    def _format_item(self, item: Dict[str, Any]) -> str:
        if item["type"] == "post":
            title = item.get("title", "")
            text = item.get("text", "")
            if title and text:
                return f"[POST] r/{item['subreddit']}: {title}\n{text}"
            elif title:
                return f"[POST] r/{item['subreddit']}: {title}"
        elif item["type"] == "comment":
            text = item.get("text", "")
            if text:
                return f"[COMMENT] r/{item['subreddit']}: {text}"
        return ""
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        text = self.examples[idx]
        
        encoded = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        
        input_ids = encoded["input_ids"].squeeze()
        attention_mask = encoded["attention_mask"].squeeze()
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": input_ids.clone(),
        }


class ModelTrainer:
    def __init__(self, config: JasonConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"\nUsing device: {self.device}")
        
    def train(self, data_file: str) -> str:
        print("\n" + "=" * 60)
        print("PHASE 3: TRAINING")
        print("=" * 60)
        
        print("\nInitializing tokenizer...")
        tokenizer = GPT2Tokenizer.from_pretrained(self.config.training.model_name)
        tokenizer.pad_token = tokenizer.eos_token
        
        print("\nCreating model...")
        model_config = GPT2Config.from_pretrained(self.config.training.model_name)
        
        target_params = self.config.training.num_parameters
        n_layer = 12
        n_head = 12
        n_embd = 768
        
        estimated_params = self._estimate_params(n_layer, n_head, n_embd, len(tokenizer))
        
        if estimated_params < target_params * 0.8:
            n_layer = 16
            n_head = 16
            n_embd = 1024
        elif estimated_params > target_params * 1.5:
            n_layer = 8
            n_head = 8
            n_embd = 512
        
        model_config.n_layer = n_layer
        model_config.n_head = n_head
        model_config.n_embd = n_embd
        model_config.vocab_size = len(tokenizer)
        
        model = GPT2LMHeadModel(model_config)
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"Model configuration:")
        print(f"  Layers: {n_layer}")
        print(f"  Heads: {n_head}")
        print(f"  Embedding dim: {n_embd}")
        print(f"  Total parameters: {total_params:,}")
        print(f"  Trainable parameters: {trainable_params:,}")
        
        model.to(self.device)
        
        print("\nLoading dataset...")
        dataset = RedditDataset(data_file, tokenizer, self.config.training.max_length)
        dataloader = DataLoader(
            dataset,
            batch_size=self.config.training.batch_size,
            shuffle=True,
            num_workers=0,
        )
        
        optimizer = AdamW(model.parameters(), lr=self.config.training.learning_rate)
        
        total_steps = len(dataloader) * self.config.training.num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.config.training.warmup_steps,
            num_training_steps=total_steps,
        )
        
        print(f"\nTraining configuration:")
        print(f"  Epochs: {self.config.training.num_epochs}")
        print(f"  Batch size: {self.config.training.batch_size}")
        print(f"  Learning rate: {self.config.training.learning_rate}")
        print(f"  Total steps: {total_steps:,}")
        print(f"  Warmup steps: {self.config.training.warmup_steps}")
        
        print("\nStarting training...")
        
        model.train()
        global_step = 0
        
        for epoch in range(self.config.training.num_epochs):
            print(f"\nEpoch {epoch + 1}/{self.config.training.num_epochs}")
            epoch_loss = 0
            
            progress_bar = tqdm(dataloader, desc=f"Training")
            
            for batch in progress_bar:
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["labels"].to(self.device)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels,
                )
                
                loss = outputs.loss
                loss.backward()
                
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                
                epoch_loss += loss.item()
                global_step += 1
                
                progress_bar.set_postfix({"loss": f"{loss.item():.4f}"})
                
                if global_step % self.config.training.save_steps == 0:
                    self._save_checkpoint(model, tokenizer, global_step)
            
            avg_loss = epoch_loss / len(dataloader)
            print(f"  Average loss: {avg_loss:.4f}")
        
        print("\n✓ Training complete!")
        
        output_dir = self._save_final_model(model, tokenizer)
        
        return output_dir
    
    def _estimate_params(self, n_layer: int, n_head: int, n_embd: int, vocab_size: int) -> int:
        params = vocab_size * n_embd
        params += n_embd
        params += n_layer * (4 * n_embd * n_embd + 5 * n_embd)
        params += n_embd * vocab_size
        return params
    
    def _save_checkpoint(self, model, tokenizer, step: int):
        checkpoint_dir = os.path.join(
            self.config.training.output_dir,
            f"checkpoint-{step}"
        )
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        model.save_pretrained(checkpoint_dir)
        tokenizer.save_pretrained(checkpoint_dir)
    
    def _save_final_model(self, model, tokenizer) -> str:
        output_dir = self.config.training.output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving final model to {output_dir}...")
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        print(f"  Model saved to: {output_dir}")
        
        return output_dir
