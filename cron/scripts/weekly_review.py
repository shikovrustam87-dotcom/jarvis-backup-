#!/usr/bin/env python3
"""Недельный обзор правил: консолидация, удаление дублей, архивация устаревшего."""

import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

def consolidate_rules():
    """Консолидирует правила, ищет дубликаты, удаляет устаревшие."""
    skills_dir = Path(r"C:\Users\Пользователь\AppData\Local\hermes\skills")
    
    if not skills_dir.exists():
        print("Папка с навыками не найдена")
        return
    
    # Считаем все навыки и их даты обновления
    skill_stats = {}
    for skill_file in skills_dir.glob("**/SKILL.md"):
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # Извлекаем дату из frontmatter
            if "version:" in content:
                version_line = [l for l in content.split('\n') if 'version:' in l]
                if version_line:
                    try:
                        version = version_line[0].split('version:')[1].strip()
                        # Простая эвристика для даты (можно улучшить)
                        date_str = f"2026-{datetime.now().month}-{datetime.now().day}"
                    except:
                        date_str = "unknown"
            
            skill_name = skill_file.stem.replace('-', '_')
            skill_stats[skill_name] = {
                'file': skill_file,
                'size_mb': len(content) / (1024 * 1024),
                'last_modified': datetime.fromtimestamp(skill_file.stat().st_mtime) if skill_file.exists() else None
            }
        except Exception as e:
            continue
    
    print("=" * 60)
    print(f"Недельный обзор правил - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Статистика навыков
    total_skills = len(skill_stats)
    total_size = sum(s['size_mb'] for s in skill_stats.values())
    
    print(f"\n📚 Всего навыков: {total_skills}")
    print(f"💾 Общий размер: {total_size:.2f} MB")
    
    # Поиск дубликатов по описанию
    descriptions = []
    for name, stats in skill_stats.items():
        try:
            desc = [l for l in stats['file'].read_text(encoding='utf-8').split('\n') if 'description:' in l]
            if desc:
                descriptions.append((name, desc[0].strip()))
        except:
            pass
    
    # Группировка по схожести (простая эвристика - одинаковые ключевые слова)
    similar_skills = []
    for name1, desc1 in descriptions:
        for name2, desc2 in descriptions:
            if name1 != name2 and len(set(desc1.lower()) & set(desc2.lower())) > 5:
                if (name1, name2) not in [(s[0], s[1]) for s in similar_skills] and \
                   (name2, name1) not in [(s[0], s[1]) for s in similar_skills]:
                    similar_skills.append((name1, name2))
    
    if similar_skills:
        print(f"\n⚠️  Найденные потенциальные дубликаты ({len(similar_skills)}):")
        for n1, n2 in set(similar_skills):
            print(f"• {n1} ↔ {n2}")
    
    # Архивация старых правил (более 30 дней)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    old_rules = []
    for name, stats in skill_stats.items():
        if stats['last_modified'] and stats['last_modified'] < thirty_days_ago:
            old_rules.append(name)
    
    if old_rules:
        print(f"\n📦 Старые правила для архивации ({len(old_rules)}):")
        for rule in set(old_rules):
            print(f"• {rule}")
    
    print("\n✅ Обзор завершен")

if __name__ == "__main__":
    consolidate_rules()
