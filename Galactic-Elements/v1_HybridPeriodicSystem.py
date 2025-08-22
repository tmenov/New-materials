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
import periodictable as pt  # Для получения данных о реальных элементах

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

# Соответствие между электронной конфигурацией и доминирующей энергией
ELECTRON_CONFIG_TO_ENERGY = {
    's1': EnergyType.MAGNETISM,    # Щелочные металлы
    's2': EnergyType.ELECTRICITY,  # Щелочноземельные
    'p1': EnergyType.RADIOWAVES,   # Бор и др.
    'p2': EnergyType.RADIOWAVES,
    'p3': EnergyType.HEAT,         # Пниктогены
    'p4': EnergyType.HEAT,         # Халькогены
    'p5': EnergyType.HEAT,         # Галогены
    'p6': EnergyType.LIGHT,        # Благородные газы
    'd': EnergyType.ELECTRICITY,   # Переходные металлы
    'f': EnergyType.MAGNETISM      # Лантаноиды/актиноиды
}

# ==================== СТРУКТУРЫ ДАННЫХ ====================
@dataclass
class NucleusStructure:
    """Структура атомного ядра"""
    protons: int
    neutrons: int
    stability: float = 1.0  # Коэффициент стабильности 0.0-1.0
    binding_energy: float = 0.0  # Энергия связи в МэВ
    spin: float = 0.0  # Спин ядра
    magnetic_moment: float = 0.0  # Магнитный момент

@dataclass
class Orbital:
    """Квантовая орбиталь"""
    type: OrbitalType
    n: int  # Главное квантовое число
    electrons: int = 0
    energy: float = 0.0  # Энергия орбитали в эВ

@dataclass
class ElectronStructure:
    """Электронная структура атома"""
    configuration: str  # Строковое представление (1s² 2s² 2p⁶)
    orbitals: List[Orbital] = field(default_factory=list)
    valence_electrons: int = 0
    ionization_energy: float = 0.0  # Энергия ионизации в эВ
    electron_affinity: float = 0.0  # Сродство к электрону в эВ

@dataclass
class QuantumEnergyProfile:
    """Квантово-энергетический профиль"""
    total_quanta: int = 0
    level_distribution: Dict[int, int] = field(default_factory=dict)
    energy_quanta: Dict[EnergyType, int] = field(default_factory=dict)
    resonance_frequency: float = 0.0  # Резонансная частота атома в Гц

@dataclass
class HybridElement:
    """Гибридный элемент - интеграция двух моделей"""
    # Стандартные свойства
    name: str
    symbol: str
    atomic_number: int
    atomic_mass: float
    
    # Квантовая структура
    nucleus: NucleusStructure
    electrons: ElectronStructure
    
    # Энергетические свойства
    energy_profile: QuantumEnergyProfile = field(default_factory=QuantumEnergyProfile)
    dominant_energy: EnergyType = EnergyType.HEAT
    element_type: ElementType = ElementType.NON_METALS
    
    # Вычисляемые свойства
    def __post_init__(self):
        self._calculate_energy_profile()
        self._determine_element_type()
    
    def _calculate_energy_profile(self):
        """Вычисление энергетического профиля на основе квантовых свойств"""
        # Базовое количество квантов (на основе водорода = 1600)
        base_quanta = 1600
        self.energy_profile.total_quanta = int(base_quanta * self.atomic_mass)
        
        # Распределение по уровням
        total = self.energy_profile.total_quanta
        self.energy_profile.level_distribution = {
            3: int(total * LEVEL_ENERGY_DISTRIBUTION[3]),
            2: int(total * LEVEL_ENERGY_DISTRIBUTION[2]), 
            1: int(total * LEVEL_ENERGY_DISTRIBUTION[1])
        }
        
        # Расчет квантов для каждого типа энергии
        first_level = self.energy_profile.level_distribution[1]
        self.energy_profile.energy_quanta = {}
        
        # Энергии первого уровня
        for energy, ratio in FIRST_LEVEL_ENERGY_RATIO.items():
            self.energy_profile.energy_quanta[energy] = int(first_level * ratio)
        
        # Энергии других уровней (расчет на основе квантовых свойств)
        self.energy_profile.energy_quanta[EnergyType.MICRO_GRAVITY] = int(
            self.nucleus.binding_energy * 1000 * self.atomic_mass
        )
        self.energy_profile.energy_quanta[EnergyType.MACRO_GRAVITY] = int(
            self.atomic_mass * 500 * (1 + self.nucleus.neutrons / self.nucleus.protons)
        )
        self.energy_profile.energy_quanta[EnergyType.THERMONUCLEAR] = int(
            self.nucleus.binding_energy * 2000 * self.nucleus.stability
        )
        self.energy_profile.energy_quanta[EnergyType.RADIOACTIVITY] = int(
            (1 - self.nucleus.stability) * 10000 * self.atomic_mass
        )
        
        # Резонансная частота (на основе энергии ионизации)
        self.energy_profile.resonance_frequency = (
            self.electrons.ionization_energy * 2.417989e14  # Преобразование эВ в Гц
        )
    
    def _determine_element_type(self):
        """Определение типа элемента на основе электронной конфигурации"""
        config = self.electrons.configuration.lower()
        
        # Анализ валентных электронов
        if 's1' in config and self.atomic_number != 1:  # Водород - особый случай
            self.dominant_energy = EnergyType.MAGNETISM
        elif 's2' in config and not any(x in config for x in ['p', 'd', 'f']):
            self.dominant_energy = EnergyType.ELECTRICITY
        elif config.endswith('p6'):
            self.dominant_energy = EnergyType.LIGHT
        elif any(x in config for x in ['p3', 'p4', 'p5']):
            self.dominant_energy = EnergyType.HEAT
        elif any(x in config for x in ['p1', 'p2']):
            self.dominant_energy = EnergyType.RADIOWAVES
        elif any(x in config for x in ['d', 'f']):
            # Для переходных металлов определяем по количеству d-электронов
            d_count = sum(1 for orb in self.electrons.orbitals if orb.type == OrbitalType.d)
            if d_count <= 5:
                self.dominant_energy = EnergyType.MAGNETISM
            else:
                self.dominant_energy = EnergyType.ELECTRICITY
        
        self.element_type = DOMINANT_ENERGY_TO_TYPE.get(
            self.dominant_energy, ElementType.NON_METALS
        )
    
    def calculate_vibrational_signature(self) -> Dict[str, float]:
        """Вычисление вибрационной сигнатуры элемента"""
        signature = {
            'base_frequency': self.energy_profile.resonance_frequency,
            'harmonic_1': self.energy_profile.resonance_frequency * 1.618,  # Золотое сечение
            'harmonic_2': self.energy_profile.resonance_frequency * 2.718,  # Число e
            'entropy_factor': np.log(self.atomic_mass) * 1e13,
            'coherence_index': self.nucleus.stability * 0.95 + 0.05
        }
        return signature
    
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
        print(f"   Спин: {self.nucleus.spin}")
        
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
            element = pt.elements[atomic_number]
            
            # Получение данных о ядре
            nucleus = HybridElementFactory._create_nucleus_structure(element)
            
            # Получение электронной структуры
            electrons = HybridElementFactory._create_electron_structure(element)
            
            return HybridElement(
                name=element.name,
                symbol=element.symbol,
                atomic_number=atomic_number,
                atomic_mass=element.mass,
                nucleus=nucleus,
                electrons=electrons
            )
        except Exception as e:
            print(f"Ошибка создания элемента {atomic_number}: {e}")
            return None
    
    @staticmethod
    def _create_nucleus_structure(element) -> NucleusStructure:
        """Создает структуру ядра"""
        protons = element.number
        most_common_isotope = max(
            element.isotopes.values(), 
            key=lambda iso: iso.abundance if iso.abundance else 0
        )
        neutrons = most_common_isotope.mass_number - protons
        
        # Расчет энергии связи (упрощенно)
        binding_energy_per_nucleon = 8.0  # Среднее значение в МэВ
        if protons > 20:
            binding_energy_per_nucleon = 8.5 - (protons - 20) * 0.02
        
        # Расчет стабильности
        stability = 1.0
        if most_common_isotope.half_life is not None:
            stability = 0.3  # Радиоактивные элементы менее стабильны
        
        return NucleusStructure(
            protons=protons,
            neutrons=neutrons,
            binding_energy=binding_energy_per_nucleon,
            stability=stability,
            spin=0.5 if protons % 2 == 1 else 0.0,
            magnetic_moment=2.79 if protons % 2 == 1 else -1.91
        )
    
    @staticmethod
    def _create_electron_structure(element) -> ElectronStructure:
        """Создает электронную структуру"""
        config = element.electrons
        
        # Парсинг электронной конфигурации для создания орбиталей
        orbitals = []
        valence = 0
        
        # Упрощенный парсинг (в реальности нужен более сложный алгоритм)
        if 's' in config:
            valence += int(config.split('s')[-1][0]) if config.split('s')[-1][0].isdigit() else 1
        
        # Расчет энергии ионизации (упрощенно)
        ionization_energy = 5.0 + (element.number * 0.1)  # эВ
        
        return ElectronStructure(
            configuration=config,
            valence_electrons=valence,
            ionization_energy=ionization_energy,
            electron_affinity=ionization_energy * 0.3
        )

# ==================== СИСТЕМА И АНАЛИЗ ====================
class HybridPeriodicSystem:
    """Гибридная периодическая система"""
    
    def __init__(self):
        self.elements = []
        self.clusters = {et: [] for et in ElementType}
    
    def build_system(self, max_elements=118):
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
                print("Возможные переходы:")
                
                # Группировка по схожим вибрационным характеристикам
                for i in range(min(3, len(elements))):
                    elem = elements[i]
                    freq = elem.energy_profile.resonance_frequency
                    print(f"  {elem.symbol}: {freq:.3e} Гц")
                
                if len(elements) > 3:
                    print(f"  ... и ещё {len(elements) - 3} элементов")

# ==================== ОСНОВНАЯ ПРОГРАММА ====================
def main():
    """Демонстрация гибридной периодической системы"""
    print("ГИБРИДНАЯ КВАНТОВО-ЭНЕРГЕТИЧЕСКАЯ МОДЕЛЬ")
    print("Интеграция стандартной физики и модели Межзвёздного Союза")
    print("=" * 80)
    
    # Создание системы
    system = HybridPeriodicSystem()
    system.build_system(max_elements=10)  # Первые 10 элементов для демонстрации
    
    # Детальный анализ ключевых элементов
    demo_elements = [1, 2, 3, 6, 8, 10]  # H, He, Li, C, O, Ne
    
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
