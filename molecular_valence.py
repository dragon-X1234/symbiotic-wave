import math
from typing import Dict, Tuple, List
from dataclasses import dataclass, field
from enum import Enum

class Element(Enum):
    """Chemical elements representing sensitivity scope types"""
    CARBON = 4    # General - 4 bonds (central hub)
    NITROGEN = 3  # Red Dot/2x - 3 bonds
    OXYGEN = 2    # 4x Scope - 2 bonds (double bond character)
    HYDROGEN = 1  # AWM - 1 bond (terminal)
    SULFUR = 6    # Free Look - 6 bonds (hexavalent)

@dataclass
class Atom:
    """Represents a sensitivity setting as a chemical atom"""
    id: str
    element: Element
    name: str
    position: Tuple[float, float]  # x, y coordinates in Angstrom-like units
    value: int                     # Current sensitivity value (1-200)
    base: int                      # Base calculated value
    bonds: List[str] = field(default_factory=list)  # Connected atom IDs
    color: str = "#ffffff"         # Hex color for visualization
    
    def __post_init__(self):
        """Ensure value is clamped to valid range"""
        self.value = max(1, min(200, self.value))
        self.base = max(1, min(200, self.base))
    
    def get_valence(self) -> int:
        """Return maximum number of bonds"""
        return self.element.value
    
    def can_bond(self) -> bool:
        """Check if atom can form more bonds"""
        return len(self.bonds) < self.element.value

class MolecularInterface:
    """
    Represents sensitivity settings as a molecular structure.
    Changes propagate through chemical bonds.
    """
    
    def __init__(self, initial_values: Dict[str, int] = None):
        self.atoms: Dict[str, Atom] = {}
        values = initial_values or {}
        
        self._initialize_atoms(values)
        self._form_bonds()
    
    def _initialize_atoms(self, values: Dict[str, int]):
        """Create atoms with calculated values"""
        defaults = {
            'general': values.get('general', 100),
            'red_dot': values.get('red_dot', 95),
            'scope_2x': values.get('scope_2x', 75),
            'scope_4x': values.get('scope_4x', 50),
            'sniper': values.get('sniper', 30),
            'free_look': values.get('free_look', 110)
        }
        
        self.atoms['general'] = Atom(
            id='general',
            element=Element.CARBON,
            name='General',
            position=(0.0, 0.0),
            value=defaults['general'],
            base=defaults['general'],
            color='#00f2ff'
        )
        
        self.atoms['reddot'] = Atom(
            id='reddot',
            element=Element.NITROGEN,
            name='Red Dot',
            position=(1.5, 0.0),
            value=defaults['red_dot'],
            base=defaults['red_dot'],
            color='#bd00ff'
        )
        
        self.atoms['2x'] = Atom(
            id='2x',
            element=Element.NITROGEN,
            name='2x Scope',
            position=(-0.75, 1.3),
            value=defaults['scope_2x'],
            base=defaults['scope_2x'],
            color='#bd00ff'
        )
        
        self.atoms['4x'] = Atom(
            id='4x',
            element=Element.OXYGEN,
            name='4x Scope',
            position=(0.0, -1.8),
            value=defaults['scope_4x'],
            base=defaults['scope_4x'],
            color='#ff006e'
        )
        
        self.atoms['awm'] = Atom(
            id='awm',
            element=Element.HYDROGEN,
            name='AWM Scope',
            position=(2.5, 0.8),
            value=defaults['sniper'],
            base=defaults['sniper'],
            color='#ffffff'
        )
        
        self.atoms['freelook'] = Atom(
            id='freelook',
            element=Element.SULFUR,
            name='Free Look',
            position=(-2.0, -1.0),
            value=defaults['free_look'],
            base=defaults['free_look'],
            color='#ffaa00'
        )
    
    def _form_bonds(self):
        """Create chemical bonds between atoms"""
        bond_structure = {
            'general': ['reddot', '2x', '4x', 'freelook'],
            'reddot': ['general', 'awm'],
            '2x': ['general'],
            '4x': ['general'],
            'awm': ['reddot'],
            'freelook': ['general']
        }
        
        for atom_id, connections in bond_structure.items():
            if atom_id in self.atoms:
                self.atoms[atom_id].bonds = connections
    
    def update_values(self, new_values: Dict[str, int]):
        """Update atom values from dictionary"""
        mapping = {
            'general': 'general',
            'reddot': 'red_dot',
            '2x': 'scope_2x',
            '4x': 'scope_4x',
            'awm': 'sniper',
            'freelook': 'free_look'
        }
        
        for atom_id, key in mapping.items():
            if atom_id in self.atoms and key in new_values:
                self.atoms[atom_id].value = max(1, min(200, new_values[key]))
                self.atoms[atom_id].base = self.atoms[atom_id].value
    
    def propagate_change(self, source_id: str, delta: int):
        """
        Propagate sensitivity change through chemical bonds.
        Delta affects bonded atoms based on bond distance.
        """
        if source_id not in self.atoms:
            return
        
        source = self.atoms[source_id]
        new_val = max(1, min(200, source.value + delta))
        source.value = new_val
        
        # Propagate to bonded atoms
        for bond_id in source.bonds:
            if bond_id in self.atoms:
                bond_atom = self.atoms[bond_id]
                distance = self._calculate_distance(source.position, bond_atom.position)
                
                # Inverse distance weighting
                if distance > 0:
                    influence = 1.0 / distance
                    propagation = int(delta * influence * 0.5)
                    new_bond_val = max(1, min(200, bond_atom.value + propagation))
                    bond_atom.value = new_bond_val
    
    def _calculate_distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Euclidean distance between atoms"""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    
    def get_values_dict(self) -> Dict[str, int]:
        """Export current values as dictionary"""
        return {
            'General': self.atoms['general'].value,
            'Red_Dot': self.atoms['reddot'].value,
            '2x_Scope': self.atoms['2x'].value,
            '4x_Scope': self.atoms['4x'].value,
            'AWM_Scope': self.atoms['awm'].value,
            'Free_Look': self.atoms['freelook'].value
        }
    
    def get_radial_positions(self, center_id: str = 'general') -> Dict[str, Tuple[float, float]]:
        """
        Get positions for radial display.
        Returns polar coordinates (angle, distance).
        """
        if center_id not in self.atoms:
            return {}
        
        center = self.atoms[center_id]
        positions = {}
        
        for atom_id, atom in self.atoms.items():
            if atom_id == center_id:
                positions[atom_id] = (0.0, 0.0)
            else:
                dx = atom.position[0] - center.position[0]
                dy = atom.position[1] - center.position[1]
                angle = math.atan2(dy, dx)
                dist = self._calculate_distance(center.position, atom.position)
                positions[atom_id] = (angle, dist)
        
        return positions