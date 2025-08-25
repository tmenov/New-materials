# -*- coding: utf-8 -*-
"""
ГИБРИДНАЯ КВАНТОВО-ЭНЕРГЕТИЧЕСКАЯ МОДЕЛЬ ПЕРИОДИЧЕСКОЙ СИСТЕМЫ
С визуализацией энергетических профилей
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
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

class EnergyLevel(Enum):
    LEVEL_1 = "Первый уровень (внешний)"
    LEVEL_2 = "Второй уровень (промежуточный)"
    LEVEL_3 = "Третий уровень (внутренний)"

# ==================== КОНФИГУРАЦИЯ МОДЕЛИ ====================
DOMINANT_ENERGY_TO_TYPE = {
    EnergyType.MAGNETISM: ElementType.ACTIVE_METALS,
    EnergyType.ELECTRICITY: ElementType.MEDIUM_METALS,
    EnergyType.RADIOWAVES: ElementType.SEMI_METALS,
    EnergyType.HEAT: ElementType.NON_METALS,
    EnergyType.LIGHT: ElementType.INERT_GASES
}

LEVEL_ENERGY_DISTRIBUTION = {
    EnergyLevel.LEVEL_3: 0.55,
    EnergyLevel.LEVEL_2: 0.33,
    EnergyLevel.LEVEL_1: 0.12
}

FIRST_LEVEL_ENERGY_RATIO = {
    EnergyType.HEAT: 0.40,
    EnergyType.LIGHT: 0.30, 
    EnergyType.MAGNETISM: 0.20,
    EnergyType.ELECTRICITY: 0.06,
    EnergyType.RADIOWAVES: 0.04
}

SECOND_LEVEL_ENERGY_RATIO = {
    EnergyType.THERMONUCLEAR: 0.50,
    EnergyType.RADIOACTIVITY: 0.30,
    EnergyType.MICRO_GRAVITY: 0.20
}

THIRD_LEVEL_ENERGY_RATIO = {
    EnergyType.MACRO_GRAVITY: 0.60,
    EnergyType.MICRO_GRAVITY: 0.25,
    EnergyType.THERMONUCLEAR: 0.15
}

# Цвета для визуализации разных типов энергий
ENERGY_COLORS = {
    EnergyType.HEAT: "#FF6B6B",        # Красный
    EnergyType.LIGHT: "#FFD93D",       # Желтый
    EnergyType.MAGNETISM: "#4ECDC4",   # Бирюзовый
    EnergyType.ELECTRICITY: "#6C5CE7", # Фиолетовый
    EnergyType.RADIOWAVES: "#FD79A8",  # Розовый
    EnergyType.MICRO_GRAVITY: "#00B894", # Зеленый
    EnergyType.MACRO_GRAVITY: "#0984E3", # Синий
    EnergyType.THERMONUCLEAR: "#E17055", # Оранжевый
    EnergyType.RADIOACTIVITY: "#636E72"  # Серый
}

# ==================== ПОЛНАЯ БАЗА ДАННЫХ ЭЛЕМЕНТОВ ====================
ELEMENTS_DATA = [
    (1, "H", "Водород", 1.008, "1s¹", (1, 0), 0.999, 13.598),
    (2, "He", "Гелий", 4.0026, "1s²", (2, 2), 0.999, 24.587),
    (3, "Li", "Литий", 6.941, "[He] 2s¹", (3, 4), 0.999, 5.392),
    (4, "Be", "Бериллий", 9.0122, "[He] 2s²", (4, 5), 0.999, 9.323),
    (5, "B", "Бор", 10.81, "[He] 2s² 2p¹", (5, 6), 0.999, 8.298),
    (6, "C", "Углерод", 12.011, "[He] 2s² 2p²", (6, 6), 0.999, 11.260),
    (7, "N", "Азот", 14.007, "[He] 2s² 2p³", (7, 7), 0.999, 14.534),
    (8, "O", "Кислород", 15.999, "[He] 2s² 2p⁴", (8, 8), 0.999, 13.618),
    (9, "F", "Фтор", 18.998, "[He] 2s² 2p⁵", (9, 10), 0.999, 17.423),
    (10, "Ne", "Неон", 20.180, "[He] 2s² 2p⁶", (10, 10), 0.999, 21.565),
    (11, "Na", "Натрий", 22.990, "[Ne] 3s¹", (11, 12), 0.999, 5.139),
    (12, "Mg", "Магний", 24.305, "[Ne] 3s²", (12, 12), 0.999, 7.646),
    (13, "Al", "Алюминий", 26.982, "[Ne] 3s² 3p¹", (13, 14), 0.999, 5.986),
    (14, "Si", "Кремний", 28.085, "[Ne] 3s² 3p²", (14, 14), 0.999, 8.152),
    (15, "P", "Фосфор", 30.974, "[Ne] 3s² 3p³", (15, 16), 0.999, 10.487),
    (16, "S", "Сера", 32.06, "[Ne] 3s² 3p⁴", (16, 16), 0.999, 10.360),
    (17, "Cl", "Хлор", 35.45, "[Ne] 3s² 3p⁵", (17, 18), 0.999, 12.968),
    (18, "Ar", "Аргон", 39.948, "[Ne] 3s² 3p⁶", (18, 22), 0.999, 15.760),
    (19, "K", "Калий", 39.098, "[Ar] 4s¹", (19, 20), 0.999, 4.341),
    (20, "Ca", "Кальций", 40.078, "[Ar] 4s²", (20, 20), 0.999, 6.113),
    (21, "Sc", "Скандий", 44.956, "[Ar] 3d¹ 4s²", (21, 24), 0.999, 6.561),
    (22, "Ti", "Титан", 47.867, "[Ar] 3d² 4s²", (22, 26), 0.999, 6.828),
    (23, "V", "Ванадий", 50.942, "[Ar] 3d³ 4s²", (23, 28), 0.999, 6.746),
    (24, "Cr", "Хром", 51.996, "[Ar] 3d⁵ 4s¹", (24, 28), 0.999, 6.767),
    (25, "Mn", "Марганец", 54.938, "[Ar] 3d⁵ 4s²", (25, 30), 0.999, 7.434),
    (26, "Fe", "Железо", 55.845, "[Ar] 3d⁶ 4s²", (26, 30), 0.999, 7.902),
    (27, "Co", "Кобальт", 58.933, "[Ar] 3d⁷ 4s²", (27, 32), 0.999, 7.881),
    (28, "Ni", "Никель", 58.693, "[Ar] 3d⁸ 4s²", (28, 30), 0.999, 7.640),
    (29, "Cu", "Медь", 63.546, "[Ar] 3d¹⁰ 4s¹", (29, 34), 0.999, 7.726),
    (30, "Zn", "Цинк", 65.38, "[Ar] 3d¹⁰ 4s²", (30, 35), 0.999, 9.394),
    (31, "Ga", "Галлий", 69.723, "[Ar] 3d¹⁰ 4s² 4p¹", (31, 39), 0.999, 5.999),
    (32, "Ge", "Германий", 72.630, "[Ar] 3d¹⁰ 4s² 4p²", (32, 41), 0.999, 7.899),
    (33, "As", "Мышьяк", 74.922, "[Ar] 3d¹⁰ 4s² 4p³", (33, 42), 0.999, 9.789),
    (34, "Se", "Селен", 78.971, "[Ar] 3d¹⁰ 4s² 4p⁴", (34, 45), 0.999, 9.752),
    (35, "Br", "Бром", 79.904, "[Ar] 3d¹⁰ 4s² 4p⁵", (35, 44), 0.999, 11.814),
    (36, "Kr", "Криптон", 83.798, "[Ar] 3d¹⁰ 4s² 4p⁶", (36, 48), 0.999, 14.000),
    (37, "Rb", "Рубидий", 85.468, "[Kr] 5s¹", (37, 48), 0.999, 4.177),
    (38, "Sr", "Стронций", 87.62, "[Kr] 5s²", (38, 50), 0.999, 5.695),
    (39, "Y", "Иттрий", 88.906, "[Kr] 4d¹ 5s²", (39, 50), 0.999, 6.217),
    (40, "Zr", "Цирконий", 91.224, "[Kr] 4d² 5s²", (40, 51), 0.999, 6.634),
    (41, "Nb", "Ниобий", 92.906, "[Kr] 4d⁴ 5s¹", (41, 52), 0.999, 6.759),
    (42, "Mo", "Молибден", 95.95, "[Kr] 4d⁵ 5s¹", (42, 54), 0.999, 7.092),
    (43, "Tc", "Технеций", 98.0, "[Kr] 4d⁵ 5s²", (43, 55), 0.100, 7.280),
    (44, "Ru", "Рутений", 101.07, "[Kr] 4d⁷ 5s¹", (44, 56), 0.999, 7.361),
    (45, "Rh", "Родий", 102.91, "[Kr] 4d⁸ 5s¹", (45, 58), 0.999, 7.459),
    (46, "Pd", "Палладий", 106.42, "[Kr] 4d¹⁰", (46, 60), 0.999, 8.337),
    (47, "Ag", "Серебро", 107.87, "[Kr] 4d¹⁰ 5s¹", (47, 61), 0.999, 7.576),
    (48, "Cd", "Кадмий", 112.41, "[Kr] 4d¹⁰ 5s²", (48, 64), 0.999, 8.994),
    (49, "In", "Индий", 114.82, "[Kr] 4d¹⁰ 5s² 5p¹", (49, 66), 0.999, 5.786),
    (50, "Sn", "Олово", 118.71, "[Kr] 4d¹⁰ 5s² 5p²", (50, 69), 0.999, 7.344),
    (51, "Sb", "Сурьма", 121.76, "[Kr] 4d¹⁰ 5s² 5p³", (51, 71), 0.999, 8.641),
    (52, "Te", "Теллур", 127.60, "[Kr] 4d¹⁰ 5s² 5p⁴", (52, 76), 0.999, 9.010),
    (53, "I", "Иод", 126.90, "[Kr] 4d¹⁰ 5s² 5p⁵", (53, 74), 0.999, 10.451),
    (54, "Xe", "Ксенон", 131.29, "[Kr] 4d¹⁰ 5s² 5p⁶", (54, 77), 0.999, 12.130),
    (55, "Cs", "Цезий", 132.91, "[Xe] 6s¹", (55, 78), 0.999, 3.894),
    (56, "Ba", "Барий", 137.33, "[Xe] 6s²", (56, 81), 0.999, 5.212),
    (57, "La", "Лантан", 138.91, "[Xe] 5d¹ 6s²", (57, 82), 0.999, 5.577),
    (58, "Ce", "Церий", 140.12, "[Xe] 4f¹ 5d¹ 6s²", (58, 82), 0.999, 5.539),
    (59, "Pr", "Празеодим", 140.91, "[Xe] 4f³ 6s²", (59, 82), 0.999, 5.464),
    (60, "Nd", "Неодим", 144.24, "[Xe] 4f⁴ 6s²", (60, 84), 0.999, 5.525),
    (61, "Pm", "Прометий", 145.0, "[Xe] 4f⁵ 6s²", (61, 84), 0.100, 5.582),
    (62, "Sm", "Самарий", 150.36, "[Xe] 4f⁶ 6s²", (62, 88), 0.999, 5.644),
    (63, "Eu", "Европий", 151.96, "[Xe] 4f⁷ 6s²", (63, 89), 0.999, 5.670),
    (64, "Gd", "Гадолиний", 157.25, "[Xe] 4f⁷ 5d¹ 6s²", (64, 93), 0.999, 6.150),
    (65, "Tb", "Тербий", 158.93, "[Xe] 4f⁹ 6s²", (65, 94), 0.999, 5.864),
    (66, "Dy", "Диспрозий", 162.50, "[Xe] 4f¹⁰ 6s²", (66, 97), 0.999, 5.939),
    (67, "Ho", "Гольмий", 164.93, "[Xe] 4f¹¹ 6s²", (67, 98), 0.999, 6.022),
    (68, "Er", "Эрбий", 167.26, "[Xe] 4f¹² 6s²", (68, 99), 0.999, 6.108),
    (69, "Tm", "Тулий", 168.93, "[Xe] 4f¹³ 6s²", (69, 100), 0.999, 6.184),
    (70, "Yb", "Иттербий", 173.05, "[Xe] 4f¹⁴ 6s²", (70, 103), 0.999, 6.254),
    (71, "Lu", "Лютеций", 174.97, "[Xe] 4f¹⁴ 5d¹ 6s²", (71, 104), 0.999, 5.426),
    (72, "Hf", "Гафний", 178.49, "[Xe] 4f¹⁴ 5d² 6s²", (72, 106), 0.999, 6.825),
    (73, "Ta", "Тантал", 180.95, "[Xe] 4f¹⁴ 5d³ 6s²", (73, 108), 0.999, 7.550),
    (74, "W", "Вольфрам", 183.84, "[Xe] 4f¹⁴ 5d⁴ 6s²", (74, 110), 0.999, 7.864),
    (75, "Re", "Рений", 186.21, "[Xe] 4f¹⁴ 5d⁵ 6s²", (75, 111), 0.999, 7.833),
    (76, "Os", "Осмий", 190.23, "[Xe] 4f¹⁴ 5d⁶ 6s²", (76, 114), 0.999, 8.438),
    (77, "Ir", "Иридий", 192.22, "[Xe] 4f¹⁴ 5d⁷ 6s²", (77, 115), 0.999, 8.967),
    (78, "Pt", "Платина", 195.08, "[Xe] 4f¹⁴ 5d⁹ 6s¹", (78, 117), 0.999, 8.959),
    (79, "Au", "Золото", 196.97, "[Xe] 4f¹⁴ 5d¹⁰ 6s¹", (79, 118), 0.999, 9.226),
    (80, "Hg", "Ртуть", 200.59, "[Xe] 4f¹⁴ 5d¹⁰ 6s²", (80, 121), 0.999, 10.438),
    (81, "Tl", "Таллий", 204.38, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹", (81, 123), 0.999, 6.108),
    (82, "Pb", "Свинец", 207.2, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²", (82, 125), 0.999, 7.417),
    (83, "Bi", "Висмут", 208.98, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³", (83, 126), 0.999, 7.289),
    (84, "Po", "Полоний", 209.0, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴", (84, 125), 0.100, 8.417),
    (85, "At", "Астат", 210.0, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁵", (85, 125), 0.100, 9.500),
    (86, "Rn", "Радон", 222.0, "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶", (86, 136), 0.100, 10.748),
    (87, "Fr", "Франций", 223.0, "[Rn] 7s¹", (87, 136), 0.100, 4.073),
    (88, "Ra", "Радий", 226.0, "[Rn] 7s²", (88, 138), 0.100, 5.279),
    (89, "Ac", "Актиний", 227.0, "[Rn] 6d¹ 7s²", (89, 138), 0.100, 5.170),
    (90, "Th", "Торий", 232.04, "[Rn] 6d² 7s²", (90, 142), 0.999, 6.307),
    (91, "Pa", "Протактиний", 231.04, "[Rn] 5f² 6d¹ 7s²", (91, 140), 0.100, 5.890),
    (92, "U", "Уран", 238.03, "[Rn] 5f³ 6d¹ 7s²", (92, 146), 0.999, 6.194),
    (93, "Np", "Нептуний", 237.0, "[Rn] 5f⁴ 6d¹ 7s²", (93, 144), 0.100, 6.266),
    (94, "Pu", "Плутоний", 244.0, "[Rn] 5f⁶ 7s²", (94, 150), 0.100, 6.026),
    (95, "Am", "Америций", 243.0, "[Rn] 5f⁷ 7s²", (95, 148), 0.100, 5.974),
    (96, "Cm", "Кюрий", 247.0, "[Rn] 5f⁷ 6d¹ 7s²", (96, 151), 0.100, 5.992),
    (97, "Bk", "Берклий", 247.0, "[Rn] 5f⁹ 7s²", (97, 150), 0.100, 6.198),
    (98, "Cf", "Калифорний", 251.0, "[Rn] 5f¹⁰ 7s²", (98, 153), 0.100, 6.282),
    (99, "Es", "Эйнштейний", 252.0, "[Rn] 5f¹¹ 7s²", (99, 153), 0.100, 6.420),
    (100, "Fm", "Фермий", 257.0, "[Rn] 5f¹² 7s²", (100, 157), 0.100, 6.500),
    (101, "Md", "Менделевий", 258.0, "[Rn] 5f¹³ 7s²", (101, 157), 0.100, 6.580),
    (102, "No", "Нобелий", 259.0, "[Rn] 5f¹⁴ 7s²", (102, 157), 0.100, 6.650),
    (103, "Lr", "Лоуренсий", 262.0, "[Rn] 5f¹⁴ 7s² 7p¹", (103, 159), 0.100, 4.900),
    (104, "Rf", "Резерфордий", 267.0, "[Rn] 5f¹⁴ 6d² 7s²", (104, 163), 0.010, 6.000),
    (105, "Db", "Дубний", 268.0, "[Rn] 5f¹⁴ 6d³ 7s²", (105, 163), 0.010, 6.800),
    (106, "Sg", "Сиборгий", 269.0, "[Rn] 5f¹⁴ 6d⁴ 7s²", (106, 163), 0.010, 7.900),
    (107, "Bh", "Борий", 270.0, "[Rn] 5f¹⁴ 6d⁵ 7s²", (107, 163), 0.010, 7.900),
    (108, "Hs", "Хассий", 277.0, "[Rn] 5f¹⁴ 6d⁶ 7s²", (108, 169), 0.010, 8.300),
    (109, "Mt", "Мейтнерий", 278.0, "[Rn] 5f¹⁴ 6d⁷ 7s²", (109, 169), 0.010, 8.400),
    (110, "Ds", "Дармштадтий", 281.0, "[Rn] 5f¹⁴ 6d⁷ 7s²", (110, 171), 0.010, 7.600),
    (111, "Rg", "Рентгений", 282.0, "[Rn] 5f¹⁴ 6d⁹ 7s²", (111, 171), 0.010, 7.700),
    (112, "Cn", "Коперниций", 285.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s²", (112, 173), 0.010, 8.900),
    (113, "Nh", "Нихоний", 286.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p¹", (113, 173), 0.010, 7.000),
    (114, "Fl", "Флеровий", 289.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p²", (114, 175), 0.010, 8.300),
    (115, "Mc", "Московий", 290.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p³", (115, 175), 0.010, 5.800),
    (116, "Lv", "Ливерморий", 293.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁴", (116, 177), 0.010, 7.500),
    (117, "Ts", "Теннессин", 294.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁵", (117, 177), 0.010, 7.700),
    (118, "Og", "Оганесон", 294.0, "[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁶", (118, 176), 0.010, 8.910)
]

# ==================== СТРУКТУРЫ ДАННЫХ ====================
@dataclass
class NucleusStructure:
    protons: int
    neutrons: int
    stability: float
    binding_energy: float
    spin: float = 0.0
    magnetic_moment: float = 0.0

@dataclass
class ElectronStructure:
    configuration: str
    valence_electrons: int = 0
    ionization_energy: float = 0.0
    electron_affinity: float = 0.0

@dataclass
class EnergyLevelQuanta:
    level: EnergyLevel
    total_quanta: int = 0
    energy_distribution: Dict[EnergyType, int] = field(default_factory=dict)

@dataclass
class QuantumEnergyProfile:
    total_quanta: int = 0
    level_quanta: Dict[EnergyLevel, EnergyLevelQuanta] = field(default_factory=dict)
    resonance_frequency: float = 0.0
    vibrational_coefficient: float = 0.0

@dataclass
class HybridElement:
    name: str
    symbol: str
    atomic_number: int
    atomic_mass: float
    nucleus: NucleusStructure
    electrons: ElectronStructure
    energy_profile: QuantumEnergyProfile = field(default_factory=QuantumEnergyProfile)
    dominant_energy: EnergyType = EnergyType.HEAT
    element_type: ElementType = ElementType.NON_METALS
    energy_signature: str = ""
    
    def __post_init__(self):
        self._calculate_energy_profile()
        self._determine_element_type()
        self._generate_energy_signature()
    
    def _calculate_energy_profile(self):
        base_quanta = 1600
        self.energy_profile.total_quanta = int(base_quanta * self.atomic_mass)
        
        total = self.energy_profile.total_quanta
        
        level_3_quanta = int(total * LEVEL_ENERGY_DISTRIBUTION[EnergyLevel.LEVEL_3])
        level_2_quanta = int(total * LEVEL_ENERGY_DISTRIBUTION[EnergyLevel.LEVEL_2])
        level_1_quanta = int(total * LEVEL_ENERGY_DISTRIBUTION[EnergyLevel.LEVEL_1])
        
        total_calculated = level_1_quanta + level_2_quanta + level_3_quanta
        if total_calculated != total:
            level_3_quanta += total - total_calculated
        
        self.energy_profile.level_quanta = {}
        
        level1 = EnergyLevelQuanta(EnergyLevel.LEVEL_1, level_1_quanta)
        for energy, ratio in FIRST_LEVEL_ENERGY_RATIO.items():
            level1.energy_distribution[energy] = int(level_1_quanta * ratio)
        self.energy_profile.level_quanta[EnergyLevel.LEVEL_1] = level1
        
        level2 = EnergyLevelQuanta(EnergyLevel.LEVEL_2, level_2_quanta)
        for energy, ratio in SECOND_LEVEL_ENERGY_RATIO.items():
            level2.energy_distribution[energy] = int(level_2_quanta * ratio)
        self.energy_profile.level_quanta[EnergyLevel.LEVEL_2] = level2
        
        level3 = EnergyLevelQuanta(EnergyLevel.LEVEL_3, level_3_quanta)
        for energy, ratio in THIRD_LEVEL_ENERGY_RATIO.items():
            level3.energy_distribution[energy] = int(level_3_quanta * ratio)
        self.energy_profile.level_quanta[EnergyLevel.LEVEL_3] = level3
        
        self.energy_profile.resonance_frequency = self.electrons.ionization_energy * 2.417989e14
        self.energy_profile.vibrational_coefficient = (
            self.nucleus.stability * 0.6 + 
            (level1.total_quanta / total) * 0.2 +
            (self.electrons.ionization_energy / 24.587) * 0.2
        )
    
    def _determine_element_type(self):
        config = self.electrons.configuration.lower()
        
        if self.atomic_number == 1:
            self.dominant_energy = EnergyType.HEAT
            self.element_type = ElementType.NON_METALS
        elif config.endswith('p⁶'):
            self.dominant_energy = EnergyType.LIGHT
            self.element_type = ElementType.INERT_GASES
        elif any(x in config for x in ['p⁵', 'p⁴', 'p³']):
            self.dominant_energy = EnergyType.HEAT
            self.element_type = ElementType.NON_METALS
        elif any(x in config for x in ['p¹', 'p²']):
            self.dominant_energy = EnergyType.RADIOWAVES
            self.element_type = ElementType.SEMI_METALS
        elif config.endswith('s¹'):
            self.dominant_energy = EnergyType.MAGNETISM
            self.element_type = ElementType.ACTIVE_METALS
        else:
            self.dominant_energy = EnergyType.ELECTRICITY
            self.element_type = ElementType.MEDIUM_METALS
    
    def _generate_energy_signature(self):
        level1 = self.energy_profile.level_quanta[EnergyLevel.LEVEL_1]
        signature_parts = []
        
        for energy in [EnergyType.HEAT, EnergyType.LIGHT, EnergyType.MAGNETISM, 
                      EnergyType.ELECTRICITY, EnergyType.RADIOWAVES]:
            quanta = level1.energy_distribution.get(energy, 0)
            signature_parts.append(f"{energy.name[:2]}{quanta}")
        
        self.energy_signature = "-".join(signature_parts)
    
    def get_total_energy_quanta(self, energy_type: EnergyType) -> int:
        total = 0
        for level_quanta in self.energy_profile.level_quanta.values():
            total += level_quanta.energy_distribution.get(energy_type, 0)
        return total
    
    def print_detailed_energy_report(self):
        print(f"\n{'='*80}")
        print(f"ДЕТАЛЬНЫЙ ЭНЕРГЕТИЧЕСКИЙ ОТЧЕТ: {self.name} ({self.symbol})")
        print(f"{'='*80}")
        
        print(f"Энергетическая сигнатура: {self.energy_signature}")
        print(f"Общее число квантов: {self.energy_profile.total_quanta:,d}")
        print(f"Резонансная частота: {self.energy_profile.resonance_frequency:.3e} Гц")
        print(f"Коэффициент вибрации: {self.energy_profile.vibrational_coefficient:.3f}")
        
        print(f"\nРАСПРЕДЕЛЕНИЕ КВАНТОВ ПО УРОВНЯМ:")
        for level, level_data in self.energy_profile.level_quanta.items():
            print(f"\n● {level.value}:")
            print(f"   Всего квантов: {level_data.total_quanta:8,d}")
            for energy_type, quanta in level_data.energy_distribution.items():
                percentage = (quanta / level_data.total_quanta * 100) if level_data.total_quanta > 0 else 0
                print(f"   {energy_type.value:20}: {quanta:8,d} квантов ({percentage:5.1f}%)")
        
        print(f"\nОБЩЕЕ РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ЭНЕРГИЙ:")
        total_energy = self.energy_profile.total_quanta
        for energy_type in EnergyType:
            total_quanta = self.get_total_energy_quanta(energy_type)
            percentage = (total_quanta / total_energy * 100) if total_energy > 0 else 0
            print(f"   {energy_type.value:20}: {total_quanta:8,d} квантов ({percentage:5.1f}%)")
    
    def generate_energy_profile_visualization(self):
        """Генерирует текстовую визуализацию энергетического профиля"""
        visualization = []
        
        # Заголовок
        visualization.append(f"\n{'═' * 60}")
        visualization.append(f"ВИЗУАЛИЗАЦИЯ ЭНЕРГЕТИЧЕСКОГО ПРОФИЛЯ: {self.name} ({self.symbol})")
        visualization.append(f"{'═' * 60}")
        
        # Общая информация
        visualization.append(f"Энергетическая сигнатура: {self.energy_signature}")
        visualization.append(f"Общее число квантов: {self.energy_profile.total_quanta:,d}")
        
        # Визуализация по уровням
        for level, level_data in self.energy_profile.level_quanta.items():
            visualization.append(f"\n{level.value}:")
            visualization.append(f"Всего квантов: {level_data.total_quanta:,d}")
            
            # Создаем текстовую диаграмму для уровня
            max_quanta = max(level_data.energy_distribution.values()) if level_data.energy_distribution else 1
            scale = 50 / max_quanta if max_quanta > 0 else 1
            
            for energy_type, quanta in sorted(level_data.energy_distribution.items(), 
                                            key=lambda x: x[1], reverse=True):
                bar_length = int(quanta * scale)
                bar = "█" * bar_length
                percentage = (quanta / level_data.total_quanta * 100) if level_data.total_quanta > 0 else 0
                visualization.append(f"  {energy_type.value:20} {bar} {quanta:6,d} ({percentage:5.1f}%)")
        
        # Круговая диаграмма общего распределения
        visualization.append(f"\n{'─' * 60}")
        visualization.append("ОБЩЕЕ РАСПРЕДЕЛЕНИЕ ЭНЕРГИЙ:")
        visualization.append(f"{'─' * 60}")
        
        total_energy = self.energy_profile.total_quanta
        energy_totals = {}
        
        for energy_type in EnergyType:
            total_quanta = self.get_total_energy_quanta(energy_type)
            energy_totals[energy_type] = total_quanta
        
        # Сортируем по убыванию
        sorted_energies = sorted(energy_totals.items(), key=lambda x: x[1], reverse=True)
        
        for energy_type, total_quanta in sorted_energies:
            percentage = (total_quanta / total_energy * 100) if total_energy > 0 else 0
            bar_length = int(percentage / 2)  # Масштабируем для визуализации
            bar = "■" * bar_length
            visualization.append(f"{energy_type.value:20} {bar} {total_quanta:8,d} ({percentage:5.1f}%)")
        
        return "\n".join(visualization)
    
    def generate_radial_chart(self):
        """Генерирует радиальную диаграмму распределения энергий"""
        chart = []
        chart.append(f"\n{'○' * 20} РАДИАЛЬНАЯ ДИАГРАММА {'○' * 20}")
        
        # Получаем данные для диаграммы
        energy_data = []
        for energy_type in EnergyType:
            quanta = self.get_total_energy_quanta(energy_type)
            if quanta > 0:
                energy_data.append((energy_type, quanta))
        
        # Сортируем по убыванию
        energy_data.sort(key=lambda x: x[1], reverse=True)
        
        # Создаем радиальную диаграмму
        max_quanta = max(quanta for _, quanta in energy_data) if energy_data else 1
        
        for energy_type, quanta in energy_data:
            # Нормализуем значения для отображения
            normalized = (quanta / max_quanta) * 10
            radius = int(normalized)
            
            # Создаем круговую линию
            circle = "◉" * radius
            percentage = (quanta / self.energy_profile.total_quanta * 100) if self.energy_profile.total_quanta > 0 else 0
            
            chart.append(f"{energy_type.value:20} {circle} {quanta:6,d} ({percentage:5.1f}%)")
        
        return "\n".join(chart)

# ==================== ФАБРИКА ЭЛЕМЕНТОВ ====================
class HybridElementFactory:
    @staticmethod
    def create_element(atomic_number: int) -> Optional[HybridElement]:
        try:
            element_data = next((item for item in ELEMENTS_DATA if item[0] == atomic_number), None)
            if not element_data:
                return None
            
            z, symbol, name, mass, config, isotope, stability, ionization = element_data
            protons, neutrons = isotope
            
            nucleus = NucleusStructure(
                protons=protons,
                neutrons=neutrons,
                stability=stability,
                binding_energy=8.0 - (z - 20) * 0.02 if z > 20 else 8.0
            )
            
            valence = HybridElementFactory._calculate_valence_electrons(config)
            
            electrons = ElectronStructure(
                configuration=config,
                valence_electrons=valence,
                ionization_energy=ionization,
                electron_affinity=ionization * 0.3
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
        if 's¹' in config and not any(x in config for x in ['p', 'd', 'f']): return 1
        if 's²' in config and not any(x in config for x in ['p', 'd', 'f']): return 2
        if 'p¹' in config: return 3
        if 'p²' in config: return 4
        if 'p³' in config: return 5
        if 'p⁴' in config: return 6
        if 'p⁵' in config: return 7
        if 'p⁶' in config: return 8
        return 0

# ==================== СИСТЕМА И АНАЛИЗ ====================
class HybridPeriodicSystem:
    def __init__(self):
        self.elements = []
        self.clusters = {et: [] for et in ElementType}
    
    def build_system(self, max_elements=118):
        print("Построение полной гибридной периодической системы...")
        
        for z in range(1, max_elements + 1):
            element = HybridElementFactory.create_element(z)
            if element:
                self.elements.append(element)
                self.clusters[element.element_type].append(element)
        
        print(f"Система построена. Всего элементов: {len(self.elements)}")
    
    def print_summary_statistics(self):
        print(f"\n{'='*60}")
        print("СТАТИСТИКА СИСТЕМЫ ПО КЛАСТЕРАМ")
        print(f"{'='*60}")
        
        for cluster_type, elements in self.clusters.items():
            if elements:
                print(f"{cluster_type.value:25}: {len(elements):3d} элементов")
        
        total_elements = sum(len(elements) for elements in self.clusters.values())
        print(f"{'ВСЕГО':25}: {total_elements:3d} элементов")
    
    def analyze_energy_distribution(self):
        print(f"\n{'='*80}")
        print("АНАЛИЗ ОБЩЕГО РАСПРЕДЕЛЕНИЯ ЭНЕРГИЙ В СИСТЕМЕ")
        print(f"{'='*80}")
        
        total_energy = sum(elem.energy_profile.total_quanta for elem in self.elements)
        energy_totals = {et: 0 for et in EnergyType}
        
        for element in self.elements:
            for energy_type in EnergyType:
                energy_totals[energy_type] += element.get_total_energy_quanta(energy_type)
        
        print(f"Общая энергия системы: {total_energy:,d} квантов")
        print("\nРаспределение по типам энергии:")
        for energy_type, total in energy_totals.items():
            percentage = (total / total_energy * 100) if total_energy > 0 else 0
            print(f"   {energy_type.value:20}: {total:12,d} квантов ({percentage:6.2f}%)")
    
    def generate_comparative_visualization(self, element_numbers: List[int]):
        """Сравнительная визуализация нескольких элементов"""
        print(f"\n{'='*80}")
        print("СРАВНИТЕЛЬНАЯ ВИЗУАЛИЗАЦИЯ ЭНЕРГЕТИЧЕСКИХ ПРОФИЛЕЙ")
        print(f"{'='*80}")
        
        elements_to_compare = []
        for z in element_numbers:
            element = next((e for e in self.elements if e.atomic_number == z), None)
            if element:
                elements_to_compare.append(element)
        
        if not elements_to_compare:
            print("Элементы для сравнения не найдены!")
            return
        
        # Создаем сравнительную таблицу
        print(f"\n{'Элемент':10} {'Сигнатура':20} {'Всего квантов':15} {'Доминирующая энергия':20}")
        print('-' * 70)
        
        for element in elements_to_compare:
            print(f"{element.symbol:10} {element.energy_signature:20} {element.energy_profile.total_quanta:15,d} {element.dominant_energy.value:20}")
        
        # Визуализация для каждого элемента
        for element in elements_to_compare:
            print(f"\n{'='*60}")
            print(f"ВИЗУАЛИЗАЦИЯ ДЛЯ {element.name} ({element.symbol})")
            print(f"{'='*60}")
            print(element.generate_energy_profile_visualization())
            print(element.generate_radial_chart())

# ==================== ОСНОВНАЯ ПРОГРАММА ====================
def main():
    print("ГИБРИДНАЯ КВАНТОВО-ЭНЕРГЕТИЧЕСКАЯ МОДЕЛЬ")
    print("С визуализацией энергетических профилей")
    print("=" * 80)
    
    system = HybridPeriodicSystem()
    system.build_system(max_elements=118)
    
    # Статистика по кластерам
    system.print_summary_statistics()
    
    # Анализ распределения энергии
    system.analyze_energy_distribution()
    
    # Вывод таблицы всех элементов
    print(f"\n{'='*120}")
    print("ТАБЛИЦА ЭНЕРГЕТИЧЕСКИХ ХАРАКТЕРИСТИК ВСЕХ ЭЛЕМЕНТОВ")
    print(f"{'='*120}")
    print(f"{'Z':3} {'Elem':5} {'Name':15} {'Type':20} {'Total Q':10} {'Res Freq':12} {'Vib Coef':8} {'Signature':20}")
    print("-" * 120)
    
    for element in system.elements:
        print(f"{element.atomic_number:3d} {element.symbol:5} {element.name:15} "
              f"{element.element_type.value:20} {element.energy_profile.total_quanta:10,d} "
              f"{element.energy_profile.resonance_frequency:.3e} {element.energy_profile.vibrational_coefficient:8.3f} "
              f"{element.energy_signature:20}")
    
    # Сравнительная визуализация ключевых элементов
    key_elements = [1, 2, 6, 8, 10, 11, 17, 18, 26, 29, 47, 79, 82, 86, 92]
    system.generate_comparative_visualization(key_elements)
    
    # Сохранение полных отчетов с визуализацией
    print(f"\n{'='*80}")
    print("СОХРАНЕНИЕ ПОЛНЫХ ОТЧЕТОВ С ВИЗУАЛИЗАЦИЕЙ")
    print(f"{'='*80}")
    
    with open("полный_энергетический_анализ_с_визуализацией.txt", "w", encoding="utf-8") as f:
        for element in system.elements:
            f.write(element.generate_energy_profile_visualization())
            f.write(element.generate_radial_chart())
            f.write("\n" + "═" * 80 + "\n\n")
    
    print("✓ Полные отчеты с визуализацией сохранены в файл 'полный_энергетический_анализ_с_визуализацией.txt'")

if __name__ == "__main__":
    main()
