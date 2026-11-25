#!/usr/bin/env python3
"""Ежедневный анализ сессий на предмет паттернов и улучшений."""

import os
from datetime import datetime, timedelta
from pathlib import Path

def analyze_sessions():
    """Анализирует последние 7 дней сессий."""
    workspace = Path(r"C:\Users\Пользователь\AppData\Local\hermes")
    
    # Ищем файлы логов сессий
    log_files = list(workspace.glob("**/log.md"))[:10]
    
    if not log_files:
        print("Нет доступных логов для анализа")
        return
    
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    
    patterns_found = []
    improvements_suggested = []
    
    for log_file in log_files:
        try:
            content = log_file.read_text(encoding='utf-8')
            
            # Ищем паттерны успешных задач
            if "Успешно завершено" in content:
                patterns_found.append("Высокая успешность задач")
            
            # Ищем повторяющиеся запросы
            if "Повторяющийся запрос" in content:
                improvements_suggested.append("Оптимизировать подход к повторяющимся задачам")
        except Exception as e:
            continue
    
    print("=" * 60)
    print(f"Ежедневный анализ сессий - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    if patterns_found:
        print("\n📊 Найденные паттерны:")
        for pattern in set(patterns_found):
            print(f"• {pattern}")
    
    if improvements_suggested:
        print("\n💡 Предложения по улучшению:")
        for improvement in set(improvements_suggested):
            print(f"• {improvement}")
    
    print("\n✅ Анализ завершен")

if __name__ == "__main__":
    analyze_sessions()
