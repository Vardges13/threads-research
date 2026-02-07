#!/usr/bin/env python3
"""
Task classifier for model router.

Analyzes task description and recommends optimal model.
"""

import argparse
import json
import sys
from typing import Dict, Optional


# Keywords and triggers for each model
MODEL_RULES = {
    "llama": {
        "keywords": [
            "простой", "простая", "простые", "быстро", "кратко", "сколько", "что такое",
            "quick", "simple", "basic", "easy", "fast",
            "weather", "погода", "время", "date", "calculate", "посчитай",
            "summarize short", "кратко", "extract from", "extract",
            "check", "verify", "confirm", "проверь",
            "list", "find", "get", "найди", "список",
            "translate", "convert", "переведи", "конвертируй"
        ],
        "cost": "free",
        "speed": "fastest",
        "reasoning": "minimal"
    },
    "sonnet": {
        "keywords": [
            "research", "analyze", "compare", "comparison", "исследуй", "анализируй", "сравни",
            "explain", "describe in detail", "detail", "объясни", "подробно",
            "moderate complexity", "multi-step", "several steps", "несколько шагов",
            "requires reasoning", "think through", "подумай", "рассуждение",
            "email", "письмо", "план", "plan", "strategy", "стратегия"
        ],
        "cost": "medium",
        "speed": "balanced",
        "reasoning": "strong"
    },
    "opus": {
        "keywords": [
            "creative", "write story", "creative writing", "креатив", "напиши историю",
            "brainstorm", "ideate", "imagine", "придумай", "воображение", "мозговой штурм",
            "maximum quality", "best possible", "highest quality", "максимальное качество",
            "nuanced", "subtle", "deep understanding", "глубокое понимание",
            "important", "critical", "production", "важно", "критично", "продакшн",
            "code", "coding", "program", "develop", "development", "код", "разработка",
            "debug", "fix bug", "debugging", "architecture", "архитектура",
            "build", "implement", "integrate", "integration", "создай", "построй",
            "refactor", "optimize code", "optimization", "оптимизация",
            "complex", "difficult", "challenging", "сложный", "трудный",
            "api", "database", "backend", "frontend", "база данных"
        ],
        "cost": "highest",
        "speed": "slowest",
        "reasoning": "maximum"
    }
}


def classify_task(task: str) -> Dict[str, Optional[str]]:
    """
    Classify task and recommend model.

    Returns dict with model, confidence, reasoning.
    """
    task_lower = task.lower()

    scores = {}

    for model, rules in MODEL_RULES.items():
        score = 0
        matched_keywords = []

        for keyword in rules["keywords"]:
            if keyword.lower() in task_lower:
                score += 1
                matched_keywords.append(keyword)

        if score > 0:
            scores[model] = {
                "score": score,
                "matched_keywords": matched_keywords,
                "cost": rules["cost"],
                "speed": rules["speed"],
                "reasoning": rules["reasoning"]
            }

    if not scores:
        return {
            "model": "llama",
            "confidence": 0,
            "reasoning": "No specific keywords matched. Use default model (llama - free and fast)."
        }

    # Cost priority for tie-breaking (lower is preferred)
    cost_priority = {
        "llama": 0,
        "sonnet": 1,
        "opus": 2
    }

    # Sort by score, then by cost (prefer cheaper models for equal scores)
    sorted_models = sorted(
        scores.items(),
        key=lambda x: (-x[1]["score"], cost_priority.get(x[0], 4))
    )

    best_model = sorted_models[0][0]
    best_info = sorted_models[0][1]

    return {
        "model": best_model,
        "confidence": best_info["score"] / len(MODEL_RULES[best_model]["keywords"]),
        "matched_keywords": best_info["matched_keywords"],
        "cost": best_info["cost"],
        "speed": best_info["speed"],
        "reasoning": f"Matched {best_info['score']} keywords: {', '.join(best_info['matched_keywords'][:3])}"
    }


def format_output(classification: Dict, format: str = "text") -> str:
    """Format classification output."""
    if format == "json":
        return json.dumps({
            "model": classification["model"],
            "confidence": classification["confidence"],
            "matched_keywords": classification.get("matched_keywords", []),
            "cost": classification.get("cost"),
            "speed": classification.get("speed"),
            "reasoning": classification.get("reasoning")
        }, indent=2)
    else:
        # Text format
        lines = []
        model = classification["model"] or "llama"
        model_names = {
            "llama": "🟢 Llama (бесплатно)",
            "sonnet": "🟡 Sonnet (средний)",
            "opus": "🔴 Opus (максимум)"
        }
        display_name = model_names.get(model, model)
        lines.append(f"🎯 Рекомендуемая модель: {display_name}")

        if classification["confidence"] > 0:
            lines.append(f"Confidence: {classification['confidence']:.1%}")

        if classification.get("matched_keywords"):
            keywords = ', '.join(classification['matched_keywords'][:3])
            if len(classification['matched_keywords']) > 3:
                keywords += "..."
            lines.append(f"Matched: {keywords}")

        if classification.get("cost"):
            lines.append(f"Cost Level: {classification['cost']}")
        if classification.get("speed"):
            lines.append(f"Speed: {classification['speed']}")
        if classification.get("reasoning"):
            lines.append(f"Reasoning: {classification['reasoning']}")

        lines.append("")
        lines.append("🚀 Команда для запуска:")
        task = classification.get('task', 'your task')
        model = classification['model'] or 'llama'
        lines.append(f"  /model {model}")
        lines.append(f"  или")  
        lines.append(f"  sessions_spawn --task \"{task}\" --model {model}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Classify task and recommend optimal model"
    )
    parser.add_argument(
        "task",
        help="Task description to classify"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    args = parser.parse_args()

    classification = classify_task(args.task)
    classification["task"] = args.task

    print(format_output(classification, args.format))


if __name__ == "__main__":
    main()
