import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum

# -*- coding: utf-8 -*-
"""
Скрипт генерации Альтернативной Периодической Системы
основанной на энергетической модели Межзвёздного Союза.
Классификация по доминирующей энергии на внешнем уровне.
"""

# 1. Определение перечислений (Enum) для типов энергий и видов элементов
class EnergyType(Enum):
    """9 фундаментальных энергий по модели МС"""
    HEAT = "Тепло"
    LIGHT = "Свет"
    MAGNETISM = "Магнетизм"
    ELECTRICITY = "Электричество"
    RADIOWAVES = "Радиоволны"
    MICRO_GRAVITY = "Микрогравитация"
    MACRO_GRAVITY = "Макрогравитация"
    THERMONUCLEAR = "Термоядерная энергия"
    RADIOACTIVITY = "Радиоактивность"

class ElementType(Enum):
    """5 видов элементов по преобладающей энергии на 1-м уровне"""
    ACTIVE_METALS = "Активные металлы"
    MEDIUM_METALS = "Средние металлы"
    SEMI_METALS = "Полуметаллы"
    NON_METALS = "Неметаллы"
    INERT_GASES = "Инертные газы"

# 2. Соответствие между доминирующей энергией и видом элемента
DOMINANT_ENERGY_TO_TYPE = {
    EnergyType.MAGNETISM: ElementType.ACTIVE_METALS,
    EnergyType.ELECTRICITY: ElementType.MEDIUM_METALS,
    EnergyType.RADIOWAVES: ElementType.SEMI_METALS,
    EnergyType.HEAT: ElementType.NON_METALS,
    EnergyType.LIGHT: ElementType.INERT_GASES
}

# 3. Формула распределения энергий на первом уровне (ступенчатая пирамида)
FIRST_LEVEL_ENERGY_RATIO = {
    EnergyType.HEAT: 0.40,
    EnergyType.LIGHT: 0.30,
    EnergyType.MAGNETISM: 0.20,
    EnergyType.ELECTRICITY: 0.06,
    EnergyType.RADIOWAVES: 0.04
}

# 4. Процентное распределение энергий по уровням атома
LEVEL_ENERGY_DISTRIBUTION = {
    3: 0.55,  # 55% энергий на третьем уровне
    2: 0.33,  # 33% на втором
    1: 0.12   # 12% на первом (внешнем)
}

@dataclass
class AlternativeElement:
    """Класс, описывающий элемент в альтернативной системе"""
    name: str
    symbol: str
    base_quanta: int = 1600  # Квантовый эквивалент водорода
    atomic_mass: float = 1.0  # Относительная атомная масса
    
    # Вычисляемые свойства
    def __post_init__(self):
        self.total_quanta = int(self.base_quanta * self.atomic_mass)
        self.dominant_energy = self._determine_dominant_energy()
        self.element_type = DOMINANT_ENERGY_TO_TYPE[self.dominant_energy]
        self.energy_profile = self._calculate_energy_distribution()
    
    def _determine_dominant_energy(self) -> EnergyType:
        """
        Определяет доминирующую энергию на основе атомной массы и символа.
        В реальной модели это определялось бы частотными характеристиками.
        Здесь - упрощенная логика на основе положения в земной таблице.
        """
        # Упрощенная логика для демонстрации
        if self.symbol in ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']:
            return EnergyType.MAGNETISM
        elif self.symbol in ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']:
            return EnergyType.ELECTRICITY
        elif self.symbol in ['B', 'Si', 'Ge', 'As', 'Sb', 'Te']:
            return EnergyType.RADIOWAVES
        elif self.symbol in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']:
            return EnergyType.LIGHT
        else:
            return EnergyType.HEAT  # По умолчанию для неметаллов
    
    def _calculate_energy_distribution(self) -> Dict[EnergyType, int]:
        """Рассчитывает распределение квантов по типам энергий"""
        # Расчет для первого уровня
        first_level_quanta = int(self.total_quanta * LEVEL_ENERGY_DISTRIBUTION[1])
        
        energy_distribution = {}
        for energy, ratio in FIRST_LEVEL_ENERGY_RATIO.items():
            energy_distribution[energy] = int(first_level_quanta * ratio)
        
        # Заполнение энергий других уровней (упрощенно)
        for energy in [EnergyType.MICRO_GRAVITY, EnergyType.MACRO_GRAVITY, 
                      EnergyType.THERMONUCLEAR, EnergyType.RADIOACTIVITY]:
            energy_distribution[energy] = int(self.total_quanta * 0.1)  # Упрощение
        
        return energy_distribution
    
    def print_info(self):
        """Выводит информацию об элементе"""
        print(f"\n=== {self.name} ({self.symbol}) ===")
        print(f"Вид элемента: {self.element_type.value}")
        print(f"Доминирующая энергия: {self.dominant_energy.value}")
        print(f"Общее число квантов: {self.total_quanta}")
        print("\nРаспределение энергий на внешнем уровне:")
        for energy, value in self.energy_profile.items():
            if energy in FIRST_LEVEL_ENERGY_RATIO:
                print(f"  {energy.value}: {value} квантов")
        
        print("\nЭнергетический профиль (все уровни):")
        for energy, value in self.energy_profile.items():
            print(f"  {energy.value}: {value} квантов")

class AlternativePeriodicSystem:
    """Класс для создания и работы с альтернативной периодической системой"""
    
    def __init__(self):
        self.elements = []
        self.clusters = {
            ElementType.ACTIVE_METALS: [],
            ElementType.MEDIUM_METALS: [],
            ElementType.SEMI_METALS: [],
            ElementType.NON_METALS: [],
            ElementType.INERT_GASES: []
        }
    
    def add_element(self, element: AlternativeElement):
        """Добавляет элемент в систему"""
        self.elements.append(element)
        self.clusters[element.element_type].append(element)
    
    def create_from_earth_elements(self, elements_data: List[Dict]):
        """Создает систему на основе данных о земных элементах"""
        for data in elements_data:
            element = AlternativeElement(
                name=data['name'],
                symbol=data['symbol'],
                atomic_mass=data['atomic_mass']
            )
            self.add_element(element)
    
    def print_cluster(self, cluster_type: ElementType):
        """Выводит элементы указанного кластера"""
        print(f"\n{'='*50}")
        print(f"КЛАСТЕР: {cluster_type.value}")
        print(f"{'='*50}")
        
        for element in self.clusters[cluster_type]:
            print(f"{element.symbol:3} - {element.name:15} | "
                  f"Доминирующая энергия: {element.dominant_energy.value}")
    
    def find_by_energy_profile(self, target_energy: EnergyType, 
                              min_quanta: int = 0) -> List[AlternativeElement]:
        """Находит элементы с заданным уровнем энергии"""
        return [elem for elem in self.elements 
                if elem.energy_profile.get(target_energy, 0) > min_quanta]
    
    def analyze_energy_transitions(self):
        """Анализирует возможные переходы между элементами внутри кластеров"""
        print("\nАНАЛИЗ ВОЗМОЖНЫХ ЭНЕРГЕТИЧЕСКИХ ПЕРЕХОДОВ")
        print("(в рамках модели МС элементы одного кластера могут трансмутировать)")
        
        for cluster_type, elements in self.clusters.items():
            if elements:
                print(f"\n--- {cluster_type.value} ---")
                print(" → ".join([elem.symbol for elem in elements[:5]]) + " → ...")

# 5. Пример использования
def main():
    """Создание и демонстрация альтернативной периодической системы"""
    
    # Данные некоторых земных элементов для демонстрации
    earth_elements_data = [
        {'name': 'Водород', 'symbol': 'H', 'atomic_mass': 1.0},
        {'name': 'Гелий', 'symbol': 'He', 'atomic_mass': 4.0},
        {'name': 'Литий', 'symbol': 'Li', 'atomic_mass': 6.9},
        {'name': 'Бериллий', 'symbol': 'Be', 'atomic_mass': 9.0},
        {'name': 'Бор', 'symbol': 'B', 'atomic_mass': 10.8},
        {'name': 'Углерод', 'symbol': 'C', 'atomic_mass': 12.0},
        {'name': 'Азот', 'symbol': 'N', 'atomic_mass': 14.0},
        {'name': 'Кислород', 'symbol': 'O', 'atomic_mass': 16.0},
        {'name': 'Фтор', 'symbol': 'F', 'atomic_mass': 19.0},
        {'name': 'Неон', 'symbol': 'Ne', 'atomic_mass': 20.2},
        {'name': 'Натрий', 'symbol': 'Na', 'atomic_mass': 23.0},
        {'name': 'Магний', 'symbol': 'Mg', 'atomic_mass': 24.3},
        {'name': 'Алюминий', 'symbol': 'Al', 'atomic_mass': 27.0},
        {'name': 'Кремний', 'symbol': 'Si', 'atomic_mass': 28.1},
        {'name': 'Железо', 'symbol': 'Fe', 'atomic_mass': 55.8},
        {'name': 'Медь', 'symbol': 'Cu', 'atomic_mass': 63.5},
        {'name': 'Серебро', 'symbol': 'Ag', 'atomic_mass': 107.9},
        {'name': 'Золото', 'symbol': 'Au', 'atomic_mass': 197.0},
        {'name': 'Уран', 'symbol': 'U', 'atomic_mass': 238.0}
    ]
    
    # Создание альтернативной системы
    print("СОЗДАНИЕ АЛЬТЕРНАТИВНОЙ ПЕРИОДИЧЕСКОЙ СИСТЕМЫ")
    print("Основанной на энергетической модели Межзвёздного Союза")
    print("-" * 60)
    
    aps = AlternativePeriodicSystem()
    aps.create_from_earth_elements(earth_elements_data)
    
    # Демонстрация кластеров
    for cluster_type in ElementType:
        aps.print_cluster(cluster_type)
    
    # Детальная информация о ключевых элементах
    print(f"\n{'='*60}")
    print("ДЕТАЛЬНЫЙ АНАЛИЗ КЛЮЧЕВЫХ ЭЛЕМЕНТОВ")
    print(f"{'='*60}")
    
    # Показать детальную информацию для некоторых элементов
    demo_elements = ['H', 'He', 'Li', 'O', 'Ne', 'Fe']
    for elem in aps.elements:
        if elem.symbol in demo_elements:
            elem.print_info()
    
    # Анализ энергетических переходов
    aps.analyze_energy_transitions()
    
    # Поиск элементов с высоким содержанием特定ной энергии
    print(f"\n{'='*60}")
    print("ПОИСК ЭЛЕМЕНТОВ С ВЫСОКИМ СОДЕРЖАНИЕМ ТЕПЛА")
    print(f"{'='*60}")
    
    heat_elements = aps.find_by_energy_profile(EnergyType.HEAT, min_quanta=500)
    for elem in heat_elements:
        print(f"{elem.symbol}: {elem.energy_profile[EnergyType.HEAT]} квантов тепла")

if __name__ == "__main__":
    main()
