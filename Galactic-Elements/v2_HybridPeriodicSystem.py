# -*- coding: utf-8 -*-
"""
ГИБРИДНАЯ КВАНТОВО-ЭНЕРГЕТИЧЕСКАЯ МОДЕЛЬ ПЕРИОДИЧЕСКОЙ СИСТЕМЫ
Интеграция стандартной модели (протоны, нейтроны, электронные орбитали) 
с энергетической моделью Межзвёздного Союза (9 энергий, 3 уровня)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum

# ==================== ЭНУМЕРАТИВНЫЕ ТИПЫ ====================
class EnergyType(Enum):
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
    ACTIVE_METALS = "Активные металлы"
    MEDIUM_METALS = "Средние металлы"
    SEMI_METALS = "Полуметаллы"
    NON_METALS = "Неметаллы"
    INERT_GASES = "Инертные газы"

class OrbitalType(Enum):
    s = "s-орбиталь"
    p = "p-орбиталь" 
    d = "d-орбиталь"
    f = "f-орбиталь"

# ==================== КОНФИГУРАЦИЯ МОДЕЛИ ====================
DOMINANT_ENERGY_TO_TYPE = {
    EnergyType.MAGNETISM: ElementType.ACTIVE_METALS,
    EnergyType.ELECTRICITY: ElementType.MEDIUM_METALS,
    EnergyType.RADIOWAVES: ElementType.SEMI_METALS,
    EnergyType.HEAT: ElementType.NON_METALS,
    EnergyType.LIGHT: ElementType.INERT_GASES
}

FIRST_LEVEL_ENERGY_RATIO = {
    EnergyType.HEAT: 0.40,
    EnergyType.LIGHT: 0.30, 
    EnergyType.MAGNETISM: 0.20,
    EnergyType.ELECTRICITY: 0.06,
    EnergyType.RADIOWAVES: 0.04
}

LEVEL_ENERGY_DISTRIBUTION = {3: 0.55, 2: 0.33, 1: 0.12}

# ==================== БАЗА ДАННЫХ ЭЛЕМЕНТОВ ====================
ELEMENTS_DATA = [
    # Z, Symbol, Name, Mass, Electrons, Most Common Isotope (protons/neutrons), Stability
    (1, "H", "Водород", 1.008, "1s¹", (1, 0), 0.999),
    (2, "He", "Гелий", 4.0026, "1s²", (2, 2), 0.999),
    (3, "Li", "Литий", 6.94, "1s² 2s¹", (3, 4), 0.999),
    (4, "Be", "Бериллий", 9.0122, "1s² 2s²", (4, 5), 0.999),
    (5, "B", "Бор", 10.81, "1s² 2s² 2p¹", (5, 6), 0.999),
    (6, "C", "Углерод", 12.011, "1s² 2s² 2p²", (6, 6), 0.999),
    (7, "N", "Азот", 14.007, "1s² 2s² 2p³", (7, 7), 0.999),
    (8, "O", "Кислород", 15.999, "1s² 2s² 2p⁴", (8, 8), 0.999),
    (9, "F", "Фтор", 18.998, "1s² 2s² 2p⁵", (9, 10), 0.999),
    (10, "Ne", "Неон", 20.180, "1s² 2s² 2p⁶", (10, 10), 0.999),
    (11, "Na", "Натрий", 22.990, "[Ne] 3s¹", (11, 12), 0.999),
    (12, "Mg", "Магний", 24.305, "[Ne] 3s²", (12, 12), 0.999),
    (13, "Al", "Алюминий", 26.982, "[Ne] 3s² 3p¹", (13, 14), 0.999),
    (14, "Si", "Кремний", 28.085, "[Ne] 3s² 3p²", (14, 14), 0.999),
    (15, "P", "Фосфор", 30.974, "[Ne] 3s² 3p³", (15, 16), 0.999),
    (16, "S", "Сера", 32.06, "[Ne] 3s² 3p⁴", (16, 16), 0.999),
    (17, "Cl", "Хлор", 35.45, "[Ne] 3s² 3p⁵", (17, 18), 0.999),
    (18, "Ar", "Аргон", 39.948, "[Ne] 3s² 3p⁶", (18, 22), 0.999),
    (19, "K", "Калий", 39.098, "[Ar] 4s¹", (19, 20), 0.999),
    (20, "Ca", "Кальций", 40.078, "[Ar] 4s²", (20, 20), 0.999),
]

# Энергии ионизации для элементов (в эВ)
IONIZATION_ENERGIES = {
    1: 13.598, 2: 24.587, 3: 5.392, 4: 9.323, 5: 8.298,
    6: 11.260, 7: 14.534, 8: 13.618, 9: 17.423, 10: 21.565,
    11: 5.139, 12: 7.646, 13: 5.986, 14: 8.152, 15: 10.487,
    16: 10.360, 17: 12.968, 18: 15.760, 19: 4.341, 20: 6.113
}

# ==================== СТРУКТУРЫ ДАННЫХ ====================
@dataclass
class NucleusStructure:
    """Структура атомного ядра"""
    protons: int
    neutrons: int
    stability: float = 1.0
    binding_energy: float = 0.0
    spin: float = 0.0
    magnetic_moment: float = 0.0

@dataclass
class Orbital:
    """Квантовая орбиталь"""
    type: OrbitalType
    n: int
    electrons: int = 0
    energy: float = 0.0

@dataclass
class ElectronStructure:
    """Электронная структура атома"""
    configuration: str
    valence_electrons: int = 0
    ionization_energy: float = 0.0
    electron_affinity: float = 0.0

@dataclass
class QuantumEnergyProfile:
    """Квантово-энергетический профиль"""
    total_quanta: int = 0
    level_distribution: Dict[int, int] = field(default_factory=dict)
    energy_quanta: Dict[EnergyType, int] = field(default_factory=dict)
    resonance_frequency: float = 0.0

@dataclass
class HybridElement:
    """Гибридный элемент - интеграция двух моделей"""
    name: str
    symbol: str
    atomic_number: int
    atomic_mass: float
    nucleus: NucleusStructure
    electrons: ElectronStructure
    energy_profile: QuantumEnergyProfile = field(default_factory=QuantumEnergyProfile)
    dominant_energy: EnergyType = EnergyType.HEAT
    element_type: ElementType = ElementType.NON_METALS
    
    def __post_init__(self):
        self._calculate_energy_profile()
        self._determine_element_type()
    
    def _calculate_energy_profile(self):
        """Вычисление энергетического профиля"""
        base_quanta = 1600
        self.energy_profile.total_quanta = int(base_quanta * self.atomic_mass)
        
        total = self.energy_profile.total_quanta
        self.energy_profile.level_distribution = {
            3: int(total * LEVEL_ENERGY_DISTRIBUTION[3]),
            2: int(total * LEVEL_ENERGY_DISTRIBUTION[2]), 
            1: int(total * LEVEL_ENERGY_DISTRIBUTION[1])
        }
        
        first_level = self.energy_profile.level_distribution[1]
        self.energy_profile.energy_quanta = {}
        
        # Энергии первого уровня
        for energy, ratio in FIRST_LEVEL_ENERGY_RATIO.items():
            self.energy_profile.energy_quanta[energy] = int(first_level * ratio)
        
        # Энергии других уровней
        binding_energy_mev = 8.0 - (self.atomic_number - 20) * 0.02 if self.atomic_number > 20 else 8.0
        self.energy_profile.energy_quanta[EnergyType.MICRO_GRAVITY] = int(
            binding_energy_mev * 1000 * self.atomic_mass
        )
        self.energy_profile.energy_quanta[EnergyType.MACRO_GRAVITY] = int(
            self.atomic_mass * 500 * (1 + self.nucleus.neutrons / max(1, self.nucleus.protons))
        )
        self.energy_profile.energy_quanta[EnergyType.THERMONUCLEAR] = int(
            binding_energy_mev * 2000 * self.nucleus.stability
        )
        self.energy_profile.energy_quanta[EnergyType.RADIOACTIVITY] = int(
            (1 - self.nucleus.stability) * 10000 * self.atomic_mass
        )
        
        # Резонансная частота
        self.energy_profile.resonance_frequency = self.electrons.ionization_energy * 2.417989e14
    
    def _determine_element_type(self):
        """Определение типа элемента на основе электронной конфигурации"""
        config = self.electrons.configuration.lower()
        
        if self.atomic_number == 1:  # Водород - особый случай
            self.dominant_energy = EnergyType.HEAT
        elif config.endswith('s¹'):
            self.dominant_energy = EnergyType.MAGNETISM
        elif config.endswith('s²'):
            self.dominant_energy = EnergyType.ELECTRICITY
        elif 'p⁶' in config:
            self.dominant_energy = EnergyType.LIGHT
        elif any(x in config for x in ['p³', 'p⁴', 'p⁵']):
            self.dominant_energy = EnergyType.HEAT
        elif any(x in config for x in ['p¹', 'p²']):
            self.dominant_energy = EnergyType.RADIOWAVES
        else:
            self.dominant_energy = EnergyType.ELECTRICITY
        
        self.element_type = DOMINANT_ENERGY_TO_TYPE.get(self.dominant_energy, ElementType.NON_METALS)
    
    def calculate_vibrational_signature(self) -> Dict[str, float]:
        """Вычисление вибрационной сигнатуры элемента"""
        return {
            'base_frequency': self.energy_profile.resonance_frequency,
            'harmonic_1': self.energy_profile.resonance_frequency * 1.618,
            'harmonic_2': self.energy_profile.resonance_frequency * 2.718,
            'entropy_factor': np.log(self.atomic_mass) * 1e13,
            'coherence_index': self.nucleus.stability * 0.95 + 0.05
        }
    
    def print_detailed_info(self):
        """Вывод детальной информации об элементе"""
        print(f"\n{'='*80}")
        print(f"ГИБРИДНЫЙ АНАЛИЗ ЭЛЕМЕНТА: {self.name} ({self.symbol})")
        print(f"{'='*80}")
        
        print(f"\n● СТАНДАРТНЫЕ ХАРАКТЕРИСТИКИ:")
        print(f"   Атомный номер: {self.atomic_number}")
        print(f"   Атомная масса: {self.atomic_mass:.4f}")
        print(f"   Электронная конфигурация: {self.electrons.configuration}")
        print(f"   Валентные электроны: {self.electrons.valence_electrons}")
        
        print(f"\n● СТРУКТУРА ЯДРА:")
        print(f"   Протоны/Нейтроны: {self.nucleus.protons}/{self.nucleus.neutrons}")
        print(f"   Энергия связи: {self.nucleus.binding_energy:.2f} МэВ/нуклон")
        print(f"   Стабильность: {self.nucleus.stability:.3f}")
        
        print(f"\n● ЭНЕРГЕТИЧЕСКИЙ ПРОФИЛЬ (Модель МС):")
        print(f"   Общее число квантов: {self.energy_profile.total_quanta}")
        print(f"   Тип элемента: {self.element_type.value}")
        print(f"   Доминирующая энергия: {self.dominant_energy.value}")
        print(f"   Резонансная частота: {self.energy_profile.resonance_frequency:.3e} Гц")
        
        print(f"\n   Распределение квантов по энергиям:")
        for energy, quanta in self.energy_profile.energy_quanta.items():
            print(f"   {energy.value:20}: {quanta:6d} квантов")
        
        print(f"\n● ВИБРАЦИОННАЯ СИГНАТУРА:")
        signature = self.calculate_vibrational_signature()
        for key, value in signature.items():
            if 'frequency' in key:
                print(f"   {key:20}: {value:.3e} Гц")
            else:
                print(f"   {key:20}: {value:.4f}")

# ==================== ФАБРИКА ЭЛЕМЕНТОВ ====================
class HybridElementFactory:
    """Фабрика для создания гибридных элементов"""
    
    @staticmethod
    def create_element(atomic_number: int) -> Optional[HybridElement]:
        """Создает гибридный элемент по атомному номеру"""
        try:
            # Поиск элемента в базе данных
            element_data = next((item for item in ELEMENTS_DATA if item[0] == atomic_number), None)
            if not element_data:
                return None
            
            z, symbol, name, mass, config, isotope, stability = element_data
            protons, neutrons = isotope
            
            # Создание структуры ядра
            nucleus = NucleusStructure(
                protons=protons,
                neutrons=neutrons,
                stability=stability,
                binding_energy=8.0 - (z - 20) * 0.02 if z > 20 else 8.0,
                spin=0.5 if protons % 2 == 1 else 0.0
            )
            
            # Создание электронной структуры
            valence = HybridElementFactory._calculate_valence_electrons(config)
            ionization_energy = IONIZATION_ENERGIES.get(z, 5.0 + z * 0.1)
            
            electrons = ElectronStructure(
                configuration=config,
                valence_electrons=valence,
                ionization_energy=ionization_energy,
                electron_affinity=ionization_energy * 0.3
            )
            
            return HybridElement(
                name=name,
                symbol=symbol,
                atomic_number=z,
                atomic_mass=mass,
                nucleus=nucleus,
                electrons=electrons
            )
        except Exception as e:
            print(f"Ошибка создания элемента {atomic_number}: {e}")
            return None
    
    @staticmethod
    def _calculate_valence_electrons(config: str) -> int:
        """Вычисляет количество валентных электронов из конфигурации"""
        if 's¹' in config: return 1
        if 's²' in config and 'p¹' in config: return 3
        if 's²' in config and 'p²' in config: return 4
        if 's²' in config and 'p³' in config: return 5
        if 's²' in config and 'p⁴' in config: return 6
        if 's²' in config and 'p⁵' in config: return 7
        if 's²' in config and 'p⁶' in config: return 8
        if 's¹' in config and config.endswith('s¹'): return 1
        if 's²' in config and config.endswith('s²'): return 2
        return 0

# ==================== СИСТЕМА И АНАЛИЗ ====================
class HybridPeriodicSystem:
    """Гибридная периодическая система"""
    
    def __init__(self):
        self.elements = []
        self.clusters = {et: [] for et in ElementType}
    
    def build_system(self, max_elements=20):
        """Построение системы элементов"""
        print("Построение гибридной периодической системы...")
        
        for z in range(1, max_elements + 1):
            element = HybridElementFactory.create_element(z)
            if element:
                self.elements.append(element)
                self.clusters[element.element_type].append(element)
        
        print(f"Система построена. Элементов: {len(self.elements)}")
    
    def analyze_cluster_transmutations(self):
        """Анализ возможных трансмутаций внутри кластеров"""
        print(f"\n{'='*60}")
        print("АНАЛИЗ ЭНЕРГЕТИЧЕСКИХ ТРАНСМУТАЦИЙ")
        print(f"{'='*60}")
        
        for cluster_type, elements in self.clusters.items():
            if elements:
                print(f"\n--- {cluster_type.value} ---")
                print("Элементы и их резонансные частоты:")
                
                for elem in elements[:5]:  # Показываем первые 5 элементов каждого кластера
                    freq = elem.energy_profile.resonance_frequency
                    print(f"  {elem.symbol}: {freq:.3e} Гц")
                
                if len(elements) > 5:
                    print(f"  ... и ещё {len(elements) - 5} элементов")

# ==================== ОСНОВНАЯ ПРОГРАММА ====================
def main():
    """Демонстрация гибридной периодической системы"""
    print("ГИБРИДНАЯ КВАНТОВО-ЭНЕРГЕТИЧЕСКАЯ МОДЕЛЬ")
    print("Интеграция стандартной физики и модели Межзвёздного Союза")
    print("=" * 80)
    
    # Создание системы
    system = HybridPeriodicSystem()
    system.build_system(max_elements=10)
    
    # Детальный анализ ключевых элементов
    demo_elements = [1, 2, 3, 6, 8, 10]
    
    print(f"\n{'='*80}")
    print("ДЕТАЛЬНЫЙ АНАЛИЗ КЛЮЧЕВЫХ ЭЛЕМЕНТОВ")
    print(f"{'='*80}")
    
    for element in system.elements:
        if element.atomic_number in demo_elements:
            element.print_detailed_info()
    
    # Анализ кластеров и трансмутаций
    system.analyze_cluster_transmutations()
    
    # Создание полной таблицы энергий
    print(f"\n{'='*80}")
    print("ТАБЛИЦА ЭНЕРГЕТИЧЕСКИХ ХАРАКТЕРИСТИК")
    print(f"{'='*80}")
    print(f"{'Elem':5} {'Type':20} {'Dominant':15} {'Total Q':10} {'Resonance':15}")
    print("-" * 80)
    
    for element in system.elements:
        print(f"{element.symbol:5} {element.element_type.value:20} "
              f"{element.dominant_energy.value:15} "
              f"{element.energy_profile.total_quanta:10} "
              f"{element.energy_profile.resonance_frequency:.3e}")

if __name__ == "__main__":
    main()
