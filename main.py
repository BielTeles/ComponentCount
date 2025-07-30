import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import pandas as pd
from datetime import datetime
import os

class ComponentCountCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ComponentCount - Calculadora de Componentes SMD")
        self.root.geometry("1400x950")
        self.root.configure(bg='#2c3e50')
        
        # Configurar estilo moderno
        self.setup_styles()
        
        # Variáveis
        self.component_type = tk.StringVar(value="0402")
        self.component_sku = tk.StringVar(value="")
        self.hub_internal_diameter = tk.StringVar(value="56")
        self.roll_radius = tk.DoubleVar(value=62.0)
        self.tape_thickness = tk.StringVar(value="0.8")
        self.component_pitch = tk.StringVar(value="4")
        
        # Lista para armazenar dados dos componentes
        self.components_data = []
        
        # Variáveis para armazenar os últimos resultados calculados
        self.last_results = {}
        
        # Variáveis do projeto
        self.current_project_name = "Projeto Sem Nome"
        self.current_project_file = None
        
        self.setup_ui()
        
    def setup_styles(self):
        """Configura estilos modernos para a aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       foreground='#ecf0f1', 
                       background='#2c3e50')
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground='#ecf0f1', 
                       background='#34495e')
        
        style.configure('Info.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground='#bdc3c7', 
                       background='#34495e')
        
        style.configure('Success.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       foreground='#27ae60', 
                       background='#2c3e50')
        
        style.configure('Warning.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       foreground='#f39c12', 
                       background='#2c3e50')
        
        # Estilo para frames
        style.configure('Card.TFrame', 
                       background='#34495e', 
                       relief='flat', 
                       borderwidth=2)
        
        # Estilo para botões
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#3498db', 
                       foreground='white')
        
        style.configure('Success.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#27ae60', 
                       foreground='white')
        
        style.configure('Warning.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#f39c12', 
                       foreground='white')
        
        style.configure('Danger.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#e74c3c', 
                       foreground='white')
        
        style.configure('Purple.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#8e44ad', 
                       foreground='white')
        
    def create_modern_button(self, parent, text, command, style='Primary', icon=None, **kwargs):
        """Cria um botão moderno com estilo consistente"""
        btn = tk.Button(
            parent,
            text=f"{icon} {text}" if icon else text,
            command=command,
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2',
            **kwargs
        )
        
        # Configurar cores baseadas no estilo
        colors = {
            'Primary': {'bg': '#3498db', 'fg': 'white'},
            'Success': {'bg': '#27ae60', 'fg': 'white'},
            'Warning': {'bg': '#f39c12', 'fg': 'white'},
            'Danger': {'bg': '#e74c3c', 'fg': 'white'},
            'Purple': {'bg': '#8e44ad', 'fg': 'white'},
            'Blue': {'bg': '#2980b9', 'fg': 'white'},
            'Green': {'bg': '#16a085', 'fg': 'white'}
        }
        
        if style in colors:
            btn.configure(**colors[style])
        
        return btn
    
    def create_tooltip(self, widget, text):
        """Cria um tooltip para o widget"""
        def show_tooltip(event):
            # Destruir tooltip anterior se existir
            if hasattr(widget, 'tooltip') and widget.tooltip:
                widget.tooltip.destroy()
            
            # Criar novo tooltip
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            
            # Calcular posição para não sair da tela
            x = event.x_root + 10
            y = event.y_root + 10
            
            # Verificar se vai sair da tela à direita
            tooltip_width = len(text) * 8 + 20  # Estimativa da largura
            screen_width = widget.winfo_screenwidth()
            if x + tooltip_width > screen_width:
                x = event.x_root - tooltip_width - 10
            
            # Verificar se vai sair da tela embaixo
            tooltip_height = 30  # Estimativa da altura
            screen_height = widget.winfo_screenheight()
            if y + tooltip_height > screen_height:
                y = event.y_root - tooltip_height - 10
            
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Criar label com estilo moderno
            label = tk.Label(tooltip, text=text, 
                           justify='left',
                           background="#2c3e50", 
                           foreground="#ecf0f1",
                           relief='flat', 
                           borderwidth=1,
                           font=("Segoe UI", 9),
                           padx=8,
                           pady=4)
            label.pack()
            
            def hide_tooltip(event=None):
                if hasattr(widget, 'tooltip') and widget.tooltip:
                    widget.tooltip.destroy()
                    widget.tooltip = None
            
            # Configurar eventos para esconder o tooltip
            widget.tooltip = tooltip
            widget.bind('<Leave>', hide_tooltip)
            tooltip.bind('<Leave>', hide_tooltip)
            tooltip.bind('<Button-1>', hide_tooltip)  # Clicar no tooltip também o esconde
            
            # Auto-destruir após 3 segundos
            tooltip.after(3000, hide_tooltip)
        
        def hide_tooltip_on_leave(event):
            if hasattr(widget, 'tooltip') and widget.tooltip:
                widget.tooltip.destroy()
                widget.tooltip = None
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip_on_leave)
        
    def setup_ui(self):
        """Configura a interface do usuário com design moderno"""
        # Container principal
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header com título e informações do projeto
        header_frame = tk.Frame(main_container, bg='#34495e', relief='flat', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Título principal
        title_frame = tk.Frame(header_frame, bg='#34495e')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame, 
            text="🔧 ComponentCount",
            font=("Segoe UI", 24, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Calculadora de Componentes SMD em Bobinas",
            font=("Segoe UI", 12),
            bg='#34495e',
            fg='#bdc3c7'
        )
        subtitle_label.pack(side='left', padx=(10, 0), pady=(8, 0))
        
        # Informações do projeto
        project_info_frame = tk.Frame(header_frame, bg='#34495e')
        project_info_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        self.project_label = tk.Label(
            project_info_frame,
            text=f"📁 Projeto: {self.current_project_name}",
            font=("Segoe UI", 11, "bold"),
            bg='#34495e',
            fg='#f39c12'
        )
        self.project_label.pack(side='left')
        
        # Botões de projeto
        project_buttons_frame = tk.Frame(project_info_frame, bg='#34495e')
        project_buttons_frame.pack(side='right')
        
        save_project_btn = self.create_modern_button(
            project_buttons_frame, "💾 Salvar", self.save_project, 'Purple'
        )
        save_project_btn.pack(side='left', padx=5)
        self.create_tooltip(save_project_btn, "Salvar projeto atual em arquivo Excel")
        
        load_project_btn = self.create_modern_button(
            project_buttons_frame, "📂 Carregar", self.load_project, 'Blue'
        )
        load_project_btn.pack(side='left', padx=5)
        self.create_tooltip(load_project_btn, "Carregar projeto de arquivo Excel")
        
        new_project_btn = self.create_modern_button(
            project_buttons_frame, "🆕 Novo", self.new_project, 'Green'
        )
        new_project_btn.pack(side='left', padx=5)
        self.create_tooltip(new_project_btn, "Criar novo projeto (limpar dados)")
        
        # Container principal dividido em duas seções
        content_frame = tk.Frame(main_container, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True)
        
        # Seção esquerda - Calculadora
        left_section = tk.Frame(content_frame, bg='#2c3e50')
        left_section.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Card da calculadora
        calculator_card = tk.Frame(left_section, bg='#34495e', relief='flat', bd=2)
        calculator_card.pack(fill='both', expand=True)
        
        # Título da calculadora
        calc_title = tk.Label(
            calculator_card,
            text="🧮 Calculadora de Componentes",
            font=("Segoe UI", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        calc_title.pack(pady=15)
        
        # Frame para parâmetros
        params_frame = tk.Frame(calculator_card, bg='#34495e')
        params_frame.pack(fill='x', padx=20, pady=10)
        
        # Grid de parâmetros
        params_grid = tk.Frame(params_frame, bg='#34495e')
        params_grid.pack(fill='x')
        
        # SKU do Componente
        tk.Label(params_grid, text="🏷️ SKU do Componente:", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        sku_entry = tk.Entry(params_grid, textvariable=self.component_sku, 
                           font=("Segoe UI", 10), relief='flat', bd=2, bg='#ecf0f1')
        sku_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.create_tooltip(sku_entry, "Digite o código SKU do componente")
        
        # Tipo de Componente
        tk.Label(params_grid, text="📦 Tipo de Componente:", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        component_combo = ttk.Combobox(params_grid, textvariable=self.component_type,
                                     values=["0201", "0402", "0603", "0805", "1206", "1210", "1812", "2010", "2512"],
                                     state="readonly", font=("Segoe UI", 10), width=15)
        component_combo.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        component_combo.bind('<<ComboboxSelected>>', self.update_component_pitch)
        self.create_tooltip(component_combo, "Selecione o tamanho do componente SMD")
        
        # Diâmetro interno do hub
        tk.Label(params_grid, text="🔘 Diâmetro Interno do Hub (mm):", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
        hub_combo = ttk.Combobox(params_grid, textvariable=self.hub_internal_diameter,
                                values=["56", "60", "90"], state="readonly", font=("Segoe UI", 10), width=15)
        hub_combo.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.create_tooltip(hub_combo, "Diâmetro interno do hub da bobina")
        
        # Raio do rolo
        tk.Label(params_grid, text="📏 Raio do Rolo (R) (mm):", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=5)
        roll_entry = tk.Entry(params_grid, textvariable=self.roll_radius, 
                            font=("Segoe UI", 10), relief='flat', bd=2, bg='#ecf0f1')
        roll_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.create_tooltip(roll_entry, "Distância da borda do rolo até a borda interna do hub")
        
        # Espessura da fita
        tk.Label(params_grid, text="📋 Espessura da Fita (mm):", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=4, column=0, sticky='w', pady=5)
        tape_combo = ttk.Combobox(params_grid, textvariable=self.tape_thickness,
                                 values=["0.5", "0.8", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8"],
                                 state="readonly", font=("Segoe UI", 10), width=15)
        tape_combo.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.create_tooltip(tape_combo, "Espessura da fita que contém os componentes")
        
        # Pitch dos componentes
        tk.Label(params_grid, text="📐 Pitch dos Componentes (mm):", 
                font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#ecf0f1').grid(row=5, column=0, sticky='w', pady=5)
        pitch_combo = ttk.Combobox(params_grid, textvariable=self.component_pitch,
                                  values=["2", "4", "8", "12", "16", "20", "24", "28", "32", "36", "40", "44"],
                                  state="readonly", font=("Segoe UI", 10), width=15)
        pitch_combo.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.create_tooltip(pitch_combo, "Distância entre os componentes na fita")
        
        # Configurar grid
        params_grid.columnconfigure(1, weight=1)
        
        # Botões de ação
        action_buttons_frame = tk.Frame(calculator_card, bg='#34495e')
        action_buttons_frame.pack(pady=20)
        
        calc_button = self.create_modern_button(
            action_buttons_frame, "⚡ Calcular", self.calculate_quantity, 'Primary'
        )
        calc_button.pack(side='left', padx=5)
        self.create_tooltip(calc_button, "Calcular quantidade de componentes na bobina")
        
        save_button = self.create_modern_button(
            action_buttons_frame, "💾 Salvar", self.save_component, 'Success'
        )
        save_button.pack(side='left', padx=5)
        self.create_tooltip(save_button, "Salvar componente calculado na tabela")
        
        delete_button = self.create_modern_button(
            action_buttons_frame, "🗑️ Excluir", self.delete_component, 'Danger'
        )
        delete_button.pack(side='left', padx=5)
        self.create_tooltip(delete_button, "Excluir componente selecionado da tabela")
        
        export_button = self.create_modern_button(
            action_buttons_frame, "📊 Exportar", self.export_to_excel, 'Warning'
        )
        export_button.pack(side='left', padx=5)
        self.create_tooltip(export_button, "Exportar dados para arquivo Excel")
        
        # Seção direita - Resultados e Tabela
        right_section = tk.Frame(content_frame, bg='#2c3e50')
        right_section.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Card de resultados
        results_card = tk.Frame(right_section, bg='#34495e', relief='flat', bd=2)
        results_card.pack(fill='x', pady=(0, 10))
        
        results_title = tk.Label(
            results_card,
            text="📊 Resultados do Cálculo",
            font=("Segoe UI", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        results_title.pack(pady=15)
        
        # Frame para resultados
        results_content = tk.Frame(results_card, bg='#34495e')
        results_content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Labels para resultados
        self.result_labels = {}
        result_items = [
            ("🔢 Quantidade Total:", "Quantidade Total de Componentes:"),
            ("📏 Comprimento da Fita:", "Comprimento da Fita (m):"),
            ("🔄 Número de Voltas:", "Número de Voltas:"),
            ("📐 Diâmetro Externo:", "Diâmetro Externo do Rolo (mm):"),
            ("📐 Diâmetro Interno:", "Diâmetro Interno do Rolo (mm):")
        ]
        
        for i, (icon, item) in enumerate(result_items):
            frame = tk.Frame(results_content, bg='#34495e')
            frame.pack(fill='x', pady=3)
            
            tk.Label(frame, text=icon, font=("Segoe UI", 12), bg='#34495e', fg='#3498db').pack(side='left')
            tk.Label(frame, text=item, font=("Segoe UI", 10), bg='#34495e', fg='#ecf0f1').pack(side='left', padx=(5, 0))
            label = tk.Label(frame, text="---", font=("Segoe UI", 10, "bold"), bg='#34495e', fg='#e74c3c')
            label.pack(side='right')
            self.result_labels[item] = label
        
        # Card da tabela
        table_card = tk.Frame(right_section, bg='#34495e', relief='flat', bd=2)
        table_card.pack(fill='both', expand=True)
        
        table_title = tk.Label(
            table_card,
            text="📋 Componentes Salvos",
            font=("Segoe UI", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        table_title.pack(pady=15)
        
        # Frame para tabela
        table_frame = tk.Frame(table_card, bg='#34495e')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Criar Treeview com estilo moderno
        columns = ('SKU', 'Tipo', 'Qtd Reels', 'Quantidade Total', 'Comprimento (m)', 'Voltas', 'Diâm. Ext. (mm)', 'Diâm. Int. (mm)', 'Data/Hora')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # Configurar estilo da tabela
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#ecf0f1",
                       foreground="#2c3e50",
                       rowheight=25,
                       fieldbackground="#ecf0f1")
        style.configure("Treeview.Heading", 
                       font=('Segoe UI', 10, 'bold'),
                       background="#34495e",
                       foreground="#ecf0f1")
        
        # Definir cabeçalhos e larguras
        column_widths = {'SKU': 100, 'Tipo': 80, 'Qtd Reels': 80, 'Quantidade Total': 120, 
                        'Comprimento (m)': 120, 'Voltas': 80, 'Diâm. Ext. (mm)': 100, 
                        'Diâm. Int. (mm)': 100, 'Data/Hora': 140}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 120), anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionar elementos
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Footer com informações
        footer_frame = tk.Frame(main_container, bg='#34495e', relief='flat', bd=2)
        footer_frame.pack(fill='x', pady=(20, 0))
        
        footer_title = tk.Label(
            footer_frame,
            text="💡 Observações Importantes",
            font=("Segoe UI", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        footer_title.pack(pady=10)
        
        info_text = """
        • Esta calculadora usa fórmulas precisas para determinar a quantidade de componentes SMD em bobinas
        • Os resultados são precisos se as medidas estiverem corretas (tolerância recomendada: ±0.2mm)
        • Para bobinas com fita frouxa, o resultado será uma superestimativa
        • Alguns fabricantes deixam o início e fim da fita vazios
        • Preencha o SKU e calcule antes de salvar o componente
        • Para múltiplos reels do mesmo SKU, escolha "Somar" para adicionar as quantidades
        • Use "Salvar Projeto" para manter seus dados entre sessões
        """
        
        info_label = tk.Label(
            footer_frame,
            text=info_text,
            font=("Segoe UI", 9),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left',
            wraplength=1350
        )
        info_label.pack(padx=20, pady=(0, 15))
    
    def update_component_pitch(self, event=None):
        """Atualiza o pitch baseado no tipo de componente selecionado"""
        pitches = {
            "0201": "1",  # 1mm pitch
            "0402": "2",  # 2mm pitch
            "0603": "4",  # 4mm pitch
            "0805": "4",  # 4mm pitch
            "1206": "4",  # 4mm pitch
            "1210": "4",  # 4mm pitch
            "1812": "4",  # 4mm pitch
            "2010": "4",  # 4mm pitch
            "2512": "4"   # 4mm pitch
        }
        
        selected = self.component_type.get()
        if selected in pitches:
            self.component_pitch.set(pitches[selected])
    
    def calculate_quantity(self):
        """Calcula a quantidade de componentes na bobina usando as fórmulas corretas"""
        try:
            # Obter valores (convertendo strings para float)
            H = float(self.hub_internal_diameter.get())  # Diâmetro interno do hub
            R = self.roll_radius.get()  # Distância da borda do rolo até a borda interna do hub
            T = float(self.tape_thickness.get())  # Espessura da fita
            pitch = float(self.component_pitch.get())  # Pitch dos componentes
            
            # Validações básicas
            if any(v <= 0 for v in [H, R, T, pitch]):
                messagebox.showerror("Erro", "Todos os valores devem ser maiores que zero!")
                return
            
            # Cálculos baseados nas fórmulas do site de referência
            # Nota: Removida a espessura do material do hub (m) dos cálculos
            
            # 1. Diâmetro externo do rolo: D = H + 2R
            D = H + 2 * R
            
            # 2. Diâmetro interno do rolo: d = H (agora igual ao diâmetro interno do hub)
            d = H
            
            # 3. Número de voltas: W = (D - d) / (2T)
            W = (D - d) / (2 * T)
            
            # 4. Comprimento da fita: L = ((D + d) / 2) * W * π
            L = ((D + d) / 2) * W * math.pi
            
            # 5. Quantidade de componentes: Q = L / pitch
            Q = L / pitch
            
            # Converter comprimento para metros
            L_meters = L / 1000
            
            # Armazenar resultados para uso posterior
            self.last_results = {
                'quantity': int(Q),
                'length_m': L_meters,
                'turns': W,
                'external_diameter': D,
                'internal_diameter': d
            }
            
            # Atualizar resultados
            self.result_labels["Quantidade Total de Componentes:"].config(text=f"{int(Q):,}")
            self.result_labels["Comprimento da Fita (m):"].config(text=f"{L_meters:.1f}")
            self.result_labels["Número de Voltas:"].config(text=f"{W:.1f}")
            self.result_labels["Diâmetro Externo do Rolo (mm):"].config(text=f"{D:.1f}")
            self.result_labels["Diâmetro Interno do Rolo (mm):"].config(text=f"{d:.1f}")
            
            # Mudar cor para verde quando há resultados
            for label in self.result_labels.values():
                label.config(fg='#27ae60')
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def save_component(self):
        """Salva o componente calculado na tabela"""
        try:
            # Verificar se há resultados calculados
            if not self.last_results:
                messagebox.showwarning("Aviso", "Execute o cálculo antes de salvar!")
                return
            
            # Verificar se o SKU foi preenchido
            sku = self.component_sku.get().strip()
            if not sku:
                messagebox.showwarning("Aviso", "Preencha o SKU do componente!")
                return
            
            # Verificar se já existe um componente com o mesmo SKU
            existing_component = None
            existing_tree_item = None
            
            for item in self.components_data:
                if item['sku'] == sku:
                    existing_component = item
                    break
            
            # Encontrar o item na Treeview
            if existing_component:
                for tree_item in self.tree.get_children():
                    if self.tree.item(tree_item)['values'][0] == sku:
                        existing_tree_item = tree_item
                        break
            
            if existing_component:
                # Criar diálogo personalizado para escolher ação
                choice = self.show_sku_exists_dialog(sku, existing_component)
                
                if choice == "cancel":
                    return
                elif choice == "replace":
                    # Substituir (comportamento original)
                    self.components_data.remove(existing_component)
                    if existing_tree_item:
                        self.tree.delete(existing_tree_item)
                elif choice == "sum":
                    # Somar quantidades
                    existing_component['quantity'] += self.last_results['quantity']
                    existing_component['reel_count'] += 1
                    existing_component['datetime'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                    
                    # Atualizar na Treeview
                    if existing_tree_item:
                        self.tree.item(existing_tree_item, values=(
                            existing_component['sku'],
                            existing_component['type'],
                            existing_component['reel_count'],
                            f"{existing_component['quantity']:,}",
                            f"{existing_component['length_m']:.1f}",
                            f"{existing_component['turns']:.1f}",
                            f"{existing_component['external_diameter']:.1f}",
                            f"{existing_component['internal_diameter']:.1f}",
                            existing_component['datetime']
                        ))
                    
                    messagebox.showinfo("Sucesso", 
                        f"Componente '{sku}' atualizado!\n"
                        f"Reels: {existing_component['reel_count']}\n"
                        f"Quantidade total: {existing_component['quantity']:,}")
                    
                    # Limpar o campo SKU para o próximo componente
                    self.component_sku.set("")
                    return
            
            # Criar dados do novo componente
            component_data = {
                'sku': sku,
                'type': self.component_type.get(),
                'reel_count': 1,
                'quantity': self.last_results['quantity'],
                'length_m': self.last_results['length_m'],
                'turns': self.last_results['turns'],
                'external_diameter': self.last_results['external_diameter'],
                'internal_diameter': self.last_results['internal_diameter'],
                'datetime': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            # Adicionar à lista
            self.components_data.append(component_data)
            
            # Adicionar à Treeview
            self.tree.insert('', 'end', values=(
                component_data['sku'],
                component_data['type'],
                component_data['reel_count'],
                f"{component_data['quantity']:,}",
                f"{component_data['length_m']:.1f}",
                f"{component_data['turns']:.1f}",
                f"{component_data['external_diameter']:.1f}",
                f"{component_data['internal_diameter']:.1f}",
                component_data['datetime']
            ))
            
            messagebox.showinfo("Sucesso", f"Componente '{sku}' salvo com sucesso!")
            
            # Limpar o campo SKU para o próximo componente
            self.component_sku.set("")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar componente: {str(e)}")
    
    def show_sku_exists_dialog(self, sku, existing_component):
        """Mostra diálogo moderno quando SKU já existe"""
        print(f"DEBUG: Criando diálogo para SKU '{sku}'")
        
        dialog = tk.Toplevel(self.root)
        dialog.title("⚠️ SKU Já Existe")
        dialog.geometry("700x600")
        dialog.configure(bg='#2c3e50')
        dialog.resizable(False, False)
        
        # Forçar foco e visibilidade
        dialog.transient(self.root)
        dialog.grab_set()  # Modal
        dialog.focus_force()  # Forçar foco
        dialog.lift()  # Trazer para frente
        dialog.attributes('-topmost', True)  # Sempre no topo
        
        # Centralizar na tela (não na janela pai)
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width // 2) - 350
        y = (screen_height // 2) - 300
        dialog.geometry(f"700x600+{x}+{y}")
        
        result = {"choice": "cancel"}
        
        # Container principal
        main_frame = tk.Frame(dialog, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título grande e visível
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(title_frame, text="⚠️ ATENÇÃO ⚠️", 
                font=("Segoe UI", 20, "bold"), bg='#2c3e50', fg='#f39c12').pack()
        
        tk.Label(title_frame, text=f"SKU '{sku}' já existe no sistema!", 
                font=("Segoe UI", 16, "bold"), bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
                
        tk.Label(title_frame, text="Escolha uma das opções abaixo:", 
                font=("Segoe UI", 12), bg='#2c3e50', fg='#bdc3c7').pack()
        
        # Card de informações
        info_card = tk.Frame(main_frame, bg='#34495e', relief='flat', bd=2)
        info_card.pack(fill='x', pady=(0, 20))
        
        # Informações atuais
        current_frame = tk.Frame(info_card, bg='#34495e')
        current_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(current_frame, text="📊 Dados Atuais:", 
                font=("Segoe UI", 12, "bold"), bg='#34495e', fg='#3498db').pack(anchor='w')
        
        current_info = f"""   🔢 Reels: {existing_component['reel_count']}
   📦 Quantidade total: {existing_component['quantity']:,} componentes
   📏 Comprimento: {existing_component['length_m']:.1f}m"""
        
        tk.Label(current_frame, text=current_info, font=("Segoe UI", 10), 
                bg='#34495e', fg='#ecf0f1', justify='left').pack(anchor='w', padx=20)
        
        # Separador
        separator = tk.Frame(info_card, bg='#7f8c8d', height=1)
        separator.pack(fill='x', padx=15, pady=5)
        
        # Novos dados
        new_frame = tk.Frame(info_card, bg='#34495e')
        new_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(new_frame, text="🆕 Novo Cálculo:", 
                font=("Segoe UI", 12, "bold"), bg='#34495e', fg='#27ae60').pack(anchor='w')
        
        new_info = f"""   📦 Quantidade: {self.last_results['quantity']:,} componentes
   📏 Comprimento: {self.last_results['length_m']:.1f}m"""
        
        tk.Label(new_frame, text=new_info, font=("Segoe UI", 10), 
                bg='#34495e', fg='#ecf0f1', justify='left').pack(anchor='w', padx=20)
        
        # Separador visual
        separator2 = tk.Frame(main_frame, bg='#7f8c8d', height=2)
        separator2.pack(fill='x', padx=20, pady=20)
        
        # Texto explicativo
        instruction_label = tk.Label(
            main_frame, text="Escolha uma das opções abaixo:",
            font=("Segoe UI", 14, "bold"), bg='#2c3e50', fg='#ecf0f1'
        )
        instruction_label.pack(pady=(0, 20))
        
        # Frame para botões com tamanho fixo
        button_frame = tk.Frame(main_frame, bg='#2c3e50', width=500, height=200)
        button_frame.pack(pady=20, expand=True, fill='both')
        button_frame.pack_propagate(False)  # Manter tamanho fixo
        
        def on_sum():
            print("DEBUG: Botão SOMAR clicado")
            result["choice"] = "sum"
            dialog.destroy()
            
        def on_replace():
            print("DEBUG: Botão SUBSTITUIR clicado")
            result["choice"] = "replace"
            dialog.destroy()
            
        def on_cancel():
            print("DEBUG: Botão CANCELAR clicado")
            result["choice"] = "cancel"
            dialog.destroy()
        
        # Botão SOMAR (mais destacado)
        sum_btn = tk.Button(
            button_frame, text="➕ SOMAR REELS (RECOMENDADO)", command=on_sum,
            font=('Segoe UI', 16, 'bold'), bg='#27ae60', fg='white',
            relief='raised', borderwidth=3, padx=30, pady=20, cursor='hand2',
            activebackground='#229954', activeforeground='white'
        )
        sum_btn.pack(pady=(20, 10), padx=50, fill='x')
        
        # Botão SUBSTITUIR
        replace_btn = tk.Button(
            button_frame, text="🔄 SUBSTITUIR DADOS", command=on_replace,
            font=('Segoe UI', 14, 'bold'), bg='#f39c12', fg='white',
            relief='raised', borderwidth=2, padx=30, pady=15, cursor='hand2',
            activebackground='#e67e22', activeforeground='white'
        )
        replace_btn.pack(pady=5, padx=50, fill='x')
        
        # Botão CANCELAR
        cancel_btn = tk.Button(
            button_frame, text="❌ CANCELAR OPERAÇÃO", command=on_cancel,
            font=('Segoe UI', 14, 'bold'), bg='#e74c3c', fg='white',
            relief='raised', borderwidth=2, padx=30, pady=15, cursor='hand2',
            activebackground='#c0392b', activeforeground='white'
        )
        cancel_btn.pack(pady=(5, 20), padx=50, fill='x')
        
        dialog.wait_window()
        return result["choice"]
    
    def delete_component(self):
        """Exclui o componente selecionado da tabela"""
        try:
            # Verificar se há item selecionado
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um componente para excluir!")
                return
            
            # Obter dados do item selecionado
            item_values = self.tree.item(selected_item)['values']
            sku = item_values[0]
            
            # Confirmar exclusão
            if messagebox.askyesno("Confirmar Exclusão", 
                                 f"Deseja excluir o componente '{sku}'?"):
                
                # Remover da lista de dados
                self.components_data = [item for item in self.components_data if item['sku'] != sku]
                
                # Remover da Treeview
                self.tree.delete(selected_item)
                
                messagebox.showinfo("Sucesso", f"Componente '{sku}' excluído com sucesso!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir componente: {str(e)}")
    
    def export_to_excel(self):
        """Exporta os dados para um arquivo Excel"""
        try:
            # Verificar se há dados para exportar
            if not self.components_data:
                messagebox.showwarning("Aviso", "Não há dados para exportar!")
                return
            
            # Abrir diálogo para salvar arquivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar planilha como"
            )
            
            if not file_path:
                return
            
            # Criar DataFrame
            df_data = []
            for item in self.components_data:
                df_data.append({
                    'SKU': item['sku'],
                    'Tipo de Componente': item['type'],
                    'Quantidade de Reels': item['reel_count'],
                    'Quantidade Total': item['quantity'],
                    'Comprimento da Fita (m)': round(item['length_m'], 1),
                    'Número de Voltas': round(item['turns'], 1),
                    'Diâmetro Externo (mm)': round(item['external_diameter'], 1),
                    'Diâmetro Interno (mm)': round(item['internal_diameter'], 1),
                    'Data/Hora': item['datetime']
                })
            
            df = pd.DataFrame(df_data)
            
            # Salvar no Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Componentes', index=False)
                
                # Ajustar largura das colunas
                worksheet = writer.sheets['Componentes']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso!\nArquivo: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")

    def save_project(self):
        """Salva o projeto atual em arquivo Excel"""
        try:
            # Verificar se há dados para salvar
            if not self.components_data:
                messagebox.showwarning("Aviso", "Não há dados para salvar no projeto!")
                return
            
            # Abrir diálogo para salvar arquivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Projeto como"
            )
            
            if not file_path:
                return
            
            # Obter nome do projeto do nome do arquivo
            project_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Criar DataFrame com metadados do projeto
            project_info = pd.DataFrame({
                'Informação': ['Nome do Projeto', 'Data de Criação', 'Total de Componentes', 'Total de SKUs', 'Descrição'],
                'Valor': [
                    project_name,
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    sum(item['quantity'] for item in self.components_data),
                    len(self.components_data),
                    f"Projeto salvo automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                ]
            })
            
            # Criar DataFrame dos componentes
            df_data = []
            for item in self.components_data:
                df_data.append({
                    'SKU': item['sku'],
                    'Tipo de Componente': item['type'],
                    'Quantidade de Reels': item['reel_count'],
                    'Quantidade Total': item['quantity'],
                    'Comprimento da Fita (m)': round(item['length_m'], 1),
                    'Número de Voltas': round(item['turns'], 1),
                    'Diâmetro Externo (mm)': round(item['external_diameter'], 1),
                    'Diâmetro Interno (mm)': round(item['internal_diameter'], 1),
                    'Data/Hora': item['datetime']
                })
            
            df_components = pd.DataFrame(df_data)
            
            # Salvar no Excel com múltiplas abas
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Aba de informações do projeto
                project_info.to_excel(writer, sheet_name='Informações do Projeto', index=False)
                
                # Aba dos componentes
                df_components.to_excel(writer, sheet_name='Componentes', index=False)
                
                # Ajustar largura das colunas em ambas as abas
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Atualizar informações do projeto
            self.current_project_name = project_name
            self.current_project_file = file_path
            self.update_project_display()
            
            messagebox.showinfo("Sucesso", 
                f"Projeto salvo com sucesso!\n"
                f"Nome: {project_name}\n"
                f"Arquivo: {file_path}\n"
                f"Componentes: {len(self.components_data)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar projeto: {str(e)}")
    
    def load_project(self):
        """Carrega um projeto de arquivo Excel"""
        try:
            # Abrir diálogo para selecionar arquivo
            file_path = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Carregar Projeto"
            )
            
            if not file_path:
                return
            
            # Verificar se o arquivo existe
            if not os.path.exists(file_path):
                messagebox.showerror("Erro", "Arquivo não encontrado!")
                return
            
            # Ler o arquivo Excel
            try:
                # Tentar ler a aba de componentes
                df_components = pd.read_excel(file_path, sheet_name='Componentes')
                
                # Limpar dados atuais
                self.components_data.clear()
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Carregar dados dos componentes
                for _, row in df_components.iterrows():
                    component_data = {
                        'sku': str(row['SKU']),
                        'type': str(row['Tipo de Componente']),
                        'reel_count': int(row['Quantidade de Reels']),
                        'quantity': int(row['Quantidade Total']),
                        'length_m': float(row['Comprimento da Fita (m)']),
                        'turns': float(row['Número de Voltas']),
                        'external_diameter': float(row['Diâmetro Externo (mm)']),
                        'internal_diameter': float(row['Diâmetro Interno (mm)']),
                        'datetime': str(row['Data/Hora'])
                    }
                    
                    self.components_data.append(component_data)
                    
                    # Adicionar à Treeview
                    self.tree.insert('', 'end', values=(
                        component_data['sku'],
                        component_data['type'],
                        component_data['reel_count'],
                        f"{component_data['quantity']:,}",
                        f"{component_data['length_m']:.1f}",
                        f"{component_data['turns']:.1f}",
                        f"{component_data['external_diameter']:.1f}",
                        f"{component_data['internal_diameter']:.1f}",
                        component_data['datetime']
                    ))
                
                # Atualizar informações do projeto
                project_name = os.path.splitext(os.path.basename(file_path))[0]
                self.current_project_name = project_name
                self.current_project_file = file_path
                self.update_project_display()
                
                messagebox.showinfo("Sucesso", 
                    f"Projeto carregado com sucesso!\n"
                    f"Nome: {project_name}\n"
                    f"Componentes carregados: {len(self.components_data)}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo Excel: {str(e)}\nVerifique se o arquivo tem a aba 'Componentes'.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar projeto: {str(e)}")
    
    def new_project(self):
        """Cria um novo projeto (limpa dados atuais)"""
        try:
            if self.components_data:
                # Confirmar se deseja limpar dados
                if not messagebox.askyesno("Novo Projeto", 
                    "Deseja criar um novo projeto?\nIsso irá limpar todos os dados atuais."):
                    return
            
            # Limpar dados
            self.components_data.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Resetar informações do projeto
            self.current_project_name = "Projeto Sem Nome"
            self.current_project_file = None
            self.update_project_display()
            
            messagebox.showinfo("Sucesso", "Novo projeto criado!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar novo projeto: {str(e)}")
    
    def update_project_display(self):
        """Atualiza a exibição das informações do projeto"""
        try:
            # Atualizar label do projeto
            if self.current_project_file:
                self.project_label.config(
                    text=f"📁 Projeto: {self.current_project_name} ({len(self.components_data)} componentes)",
                    fg='#27ae60'
                )
            else:
                self.project_label.config(
                    text=f"📁 Projeto: {self.current_project_name} ({len(self.components_data)} componentes)",
                    fg='#e74c3c'
                )
        except Exception as e:
            print(f"Erro ao atualizar display do projeto: {e}")

def main():
    root = tk.Tk()
    app = ComponentCountCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 