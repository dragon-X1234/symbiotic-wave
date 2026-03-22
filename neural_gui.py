#!/usr/bin/env python3
try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("CustomTkinter not available. Install: pip install customtkinter")

class IAMGUI:
    """
    I AM GUI aesthetic implementation with glassmorphism.
    """
    
    def __init__(self, root):
        if not GUI_AVAILABLE:
            raise ImportError("CustomTkinter required")
            
        self.root = root
        self.root.title("MN-SOS v3.0 | Neural Interface")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#0a0a0f")
        
        # Color scheme - I AM aesthetic
        self.colors = {
            'bg': "#0a0a0f",
            'card': "#12121a",
            'accent_cyan': "#00f2ff",
            'accent_purple': "#bd00ff",
            'accent_pink': "#ff006e",
            'text': "#ffffff",
            'text_sec': "#8b8b9a",
            'success': "#00ff88"
        }
        
        self.setup_fonts()
        self.create_layout()
    
    def setup_fonts(self):
        """Configure typography"""
        self.fonts = {
            'title': ctk.CTkFont(family="Inter", size=32, weight="bold"),
            'heading': ctk.CTkFont(family="Inter", size=20, weight="bold"),
            'body': ctk.CTkFont(family="Inter", size=14),
            'mono': ctk.CTkFont(family="JetBrains Mono", size=12)
        }
    
    def create_layout(self):
        """Create glassmorphism layout"""
        # Main container
        self.main = ctk.CTkFrame(self.root, fg_color=self.colors['bg'])
        self.main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Content grid
        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.pack(fill="both", expand=True, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=2)
        
        # Left panel - Hardware
        self.create_hardware_panel()
        
        # Right panel - Results
        self.create_results_panel()
    
    def create_header(self):
        """Create header with glow effect"""
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="MN-SOS",
            font=self.fonts['title'],
            text_color=self.colors['accent_cyan']
        )
        title.pack(side="left")
        
        version = ctk.CTkLabel(
            header,
            text="v3.0",
            font=ctk.CTkFont(size=14),
            fg_color=self.colors['accent_purple'],
            text_color=self.colors['text'],
            corner_radius=10,
            padx=10
        )
        version.pack(side="left", padx=(10, 0))
    
    def create_hardware_panel(self):
        """Create hardware specification panel"""
        panel = ctk.CTkFrame(
            self.content,
            fg_color=self.colors['card'],
            border_color=self.colors['accent_cyan'],
            border_width=1,
            corner_radius=20
        )
        panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        ctk.CTkLabel(
            panel,
            text="HARDWARE PROFILE",
            font=self.fonts['heading'],
            text_color=self.colors['accent_cyan']
        ).pack(pady=20)
        
        # Separator
        ctk.CTkFrame(
            panel,
            fg_color=self.colors['accent_purple'],
            height=2
        ).pack(fill="x", padx=20)
        
        # Input fields
        self.inputs = {}
        fields = [
            ("DPI", "400"),
            ("Refresh Rate", "90"),
            ("Touch Hz", "240"),
            ("CPU Cores", "8"),
            ("CPU GHz", "2.4"),
            ("RAM GB", "8")
        ]
        
        for label, default in fields:
            self.create_input_field(panel, label, default)
        
        # Calculate button
        calc_btn = ctk.CTkButton(
            panel,
            text="⚡ CALCULATE",
            font=self.fonts['heading'],
            fg_color=self.colors['accent_cyan'],
            text_color=self.colors['bg'],
            hover_color=self.colors['accent_purple'],
            height=50,
            command=self.calculate
        )
        calc_btn.pack(fill="x", padx=20, pady=30)
    
    def create_input_field(self, parent, label, default):
        """Create labeled input field"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=self.fonts['body'],
            text_color=self.colors['text_sec']
        ).pack(anchor="w")
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=default,
            font=self.fonts['mono'],
            fg_color="#1a1a24",
            border_color=self.colors['accent_purple'],
            border_width=2,
            height=40
        )
        entry.pack(fill="x", pady=(5, 0))
        entry.insert(0, default)
        
        self.inputs[label] = entry
    
    def create_results_panel(self):
        """Create results display panel"""
        panel = ctk.CTkFrame(
            self.content,
            fg_color=self.colors['card'],
            border_color=self.colors['accent_purple'],
            border_width=1,
            corner_radius=20
        )
        panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            panel,
            text="SENSITIVITY MATRIX",
            font=self.fonts['heading'],
            text_color=self.colors['accent_purple']
        ).pack(pady=20)
        
        # Results text area
        self.results_text = ctk.CTkTextbox(
            panel,
            fg_color="#0f0f16",
            border_color=self.colors['accent_cyan'],
            border_width=1,
            font=self.fonts['mono'],
            height=400
        )
        self.results_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Export button
        export_btn = ctk.CTkButton(
            panel,
            text="📁 EXPORT",
            font=self.fonts['body'],
            fg_color=self.colors['accent_purple'],
            command=self.export_results
        )
        export_btn.pack(pady=20)
    
    def calculate(self):
        """Perform calculation"""
        try:
            # Get values from inputs
            dpi = int(self.inputs["DPI"].get() or 400)
            
            # Import here to avoid startup delay
            from core.dynamic_calculator import DynamicSensitivityEngine
            from core.hardware_probe import DeviceProfile
            
            # Create device profile from inputs
            device = DeviceProfile(
                dpi=dpi,
                screen_width=1080,
                screen_height=2400,
                physical_size_inches=6.5,
                refresh_rate=int(self.inputs["Refresh Rate"].get() or 90),
                touch_sampling_rate=int(self.inputs["Touch Hz"].get() or 240),
                cpu_cores=int(self.inputs["CPU Cores"].get() or 8),
                cpu_max_freq_ghz=float(self.inputs["CPU GHz"].get() or 2.4),
                cpu_architecture='arm64',
                gpu_renderer='Unknown',
                ram_gb=float(self.inputs["RAM GB"].get() or 8),
                thermal_zone_paths=[],
                android_version=12,
                kernel_version='unknown'
            )
            
            # Calculate
            engine = DynamicSensitivityEngine(device)
            matrix = engine.calculate_matrix()
            
            # Display results
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "🎯 OPTIMAL CONFIGURATION\\n")
            self.results_text.insert("end", "=" * 30 + "\\n\\n")
            self.results_text.insert("end", f"General:     {matrix.general}\\n")
            self.results_text.insert("end", f"Red Dot:     {matrix.red_dot}\\n")
            self.results_text.insert("end", f"2x Scope:    {matrix.scope_2x}\\n")
            self.results_text.insert("end", f"4x Scope:    {matrix.scope_4x