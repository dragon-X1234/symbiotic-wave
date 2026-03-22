#!/usr/bin/env python3
import math
import time
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
    from rich.layout import Layout
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

@dataclass
class RenderAtom:
    x: int
    y: int
    symbol: str
    color: str
    value: int

class MolecularRadialTUI:
    """
    Terminal-based radial interface showing sensitivity atoms as chemical structure.
    """
    
    def __init__(self, molecule):
        self.molecule = molecule
        self.console = Console() if RICH_AVAILABLE else None
        self.selected = 'general'
        self.width = 60
        self.height = 30
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
    def clear_screen(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_frame(self) -> str:
        """Render one frame of molecular interface"""
        if not RICH_AVAILABLE:
            return "Rich library required: pip install rich"
        
        # Create canvas
        canvas = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Get positions
        positions = self.molecule.get_radial_positions(self.selected)
        center_atom = self.molecule.atoms[self.selected]
        
        # Draw bonds first
        for bond_id in center_atom.bonds:
            if bond_id in positions:
                angle, dist = positions[bond_id]
                # Scale distance for display
                display_dist = min(12, int(dist * 6))
                x = int(self.center_x + display_dist * math.cos(angle))
                y = int(self.center_y + display_dist * math.sin(angle) * 0.5)  # Aspect ratio correction
                
                # Draw bond line
                self._draw_line(canvas, self.center_x, self.center_y, x, y, '·')
                
                # Draw bonded atom
                atom = self.molecule.atoms[bond_id]
                symbol = atom.element.name[0]
                if 0 <= y < self.height and 0 <= x < self.width:
                    canvas[y][x] = f"[{symbol}]"
                    # Draw value below
                    val_str = str(atom.value)
                    for i, c in enumerate(val_str):
                        if y+1 < self.height and x+i < self.width:
                            canvas[y+1][x+i] = c
        
        # Draw center atom
        center_sym = center_atom.element.name[0]
        canvas[self.center_y][self.center_x] = f"*{center_sym}*"
        val_str = str(center_atom.value)
        for i, c in enumerate(val_str):
            if self.center_y+1 < self.height and self.center_x+i < self.width:
                canvas[self.center_y+1][self.center_x+i] = c
        
        # Convert to string
        lines = [''.join(row) for row in canvas]
        return '\n'.join(lines)
    
    def _draw_line(self, canvas, x0, y0, x1, y1, char):
        """Bresenham line algorithm"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            if 0 <= y0 < len(canvas) and 0 <= x0 < len(canvas[0]):
                canvas[y0][x0] = char
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def display_static(self):
        """Display without live animation"""
        if not RICH_AVAILABLE:
            print("Install Rich: pip install rich")
            return
        
        table = Table(title="MN-SOS Molecular Structure")
        table.add_column("Atom", style="cyan")
        table.add_column("Element", style="green")
        table.add_column("Valence", style="yellow")
        table.add_column("Value", style="magenta")
        table.add_column("Bonds", style="blue")
        
        for atom_id, atom in self.molecule.atoms.items():
            elem_name = atom.element.name
            valence = atom.get_valence()
            bonds_str = ", ".join(atom.bonds)
            marker = ">" if atom_id == self.selected else " "
            table.add_row(
                f"{marker} {atom.name}",
                elem_name,
                str(valence),
                str(atom.value),
                bonds_str
            )
        
        self.console.print(table)
    
    def interactive_mode(self):
        """Simple interactive mode"""
        while True:
            self.clear_screen()
            print("MN-SOS Molecular Interface")
            print("=" * 40)
            self.display_static()
            
            print("\nCommands: [s]elect [a]djust [q]uit")
            cmd = input("> ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 's':
                idx = input("Select atom (general, reddot, 2x, 4x, awm, freelook): ")
                if idx in self.molecule.atoms:
                    self.selected = idx
            elif cmd == 'a':
                try:
                    delta = int(input("Adjust by (+/-): "))
                    self.molecule.propagate_change(self.selected, delta)
                except ValueError:
                    print("Invalid number")

def launch_tui(molecule):
    """Entry point for TUI"""
    tui = MolecularRadialTUI(molecule)
    try:
        tui.interactive_mode()
    except KeyboardInterrupt:
        print("\nExiting...")