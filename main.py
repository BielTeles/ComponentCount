import tkinter as tk
from tkinter import ttk, messagebox
import math

class ComponentCountCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Quantidade de Componentes em Bobinas")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.component_type = tk.StringVar(value="0402")
        self.hub_internal_diameter = tk.DoubleVar(value=56.0)  # Diâmetro interno do hub
        self.hub_material_thickness = tk.DoubleVar(value=2.0)  # Espessura do material do hub
        self.roll_radius = tk.DoubleVar(value=62.0)  # Distância da borda do rolo até a borda interna do hub
        self.tape_thickness = tk.DoubleVar(value=0.8)  # Espessura da fita
        self.component_pitch = tk.DoubleVar(value=4.0)  # Pitch dos componentes
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título principal
        title_label = tk.Label(
            self.root, 
            text="Calculadora de Quantidade de Componentes em Bobinas",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Frame esquerdo - Parâmetros da bobina
        left_frame = tk.LabelFrame(main_frame, text="Parâmetros da Bobina", font=("Arial", 12, "bold"), bg='#f0f0f0')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Tipo de componente
        tk.Label(left_frame, text="Tipo de Componente:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w', padx=10, pady=5)
        component_combo = ttk.Combobox(left_frame, textvariable=self.component_type, 
                                     values=["0201", "0402", "0603", "0805", "1206", "1210", "1812", "2010", "2512"],
                                     state="readonly", width=15)
        component_combo.pack(padx=10, pady=5)
        component_combo.bind('<<ComboboxSelected>>', self.update_component_pitch)
        
        # Parâmetros da bobina (baseados no site de referência)
        params = [
            ("Diâmetro Interno do Hub (mm):", self.hub_internal_diameter),
            ("Espessura do Material do Hub (mm):", self.hub_material_thickness),
            ("Raio do Rolo (R) (mm):", self.roll_radius),
            ("Espessura da Fita (mm):", self.tape_thickness),
            ("Pitch dos Componentes (mm):", self.component_pitch)
        ]
        
        for label_text, var in params:
            frame = tk.Frame(left_frame, bg='#f0f0f0')
            frame.pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=label_text, font=("Arial", 10), bg='#f0f0f0').pack(side='left')
            tk.Entry(frame, textvariable=var, width=10, font=("Arial", 10)).pack(side='right')
        
        # Frame direito - Informações e resultados
        right_frame = tk.LabelFrame(main_frame, text="Informações e Resultados", font=("Arial", 12, "bold"), bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Informações sobre as medidas
        info_text = """
        Medidas necessárias:
        
        • Diâmetro interno do hub (H)
        • Espessura do material do hub (m)
        • Distância da borda do rolo até 
          a borda interna do hub (R)
        • Espessura da fita (T)
        • Pitch dos componentes
        
        Todas as medidas em mm.
        """
        
        tk.Label(right_frame, text=info_text, font=("Arial", 9), bg='#f0f0f0', 
                justify='left', wraplength=350).pack(padx=10, pady=10)
        
        # Botão calcular
        calc_button = tk.Button(
            self.root,
            text="Calcular Quantidade",
            command=self.calculate_quantity,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            padx=20,
            pady=10
        )
        calc_button.pack(pady=20)
        
        # Frame de resultados
        results_frame = tk.LabelFrame(self.root, text="Resultados", font=("Arial", 12, "bold"), bg='#f0f0f0')
        results_frame.pack(fill='x', padx=20, pady=10)
        
        # Labels para resultados
        self.result_labels = {}
        result_items = [
            "Quantidade Total de Componentes:",
            "Comprimento da Fita (m):",
            "Número de Voltas:",
            "Diâmetro Externo do Rolo (mm):",
            "Diâmetro Interno do Rolo (mm):"
        ]
        
        for item in result_items:
            frame = tk.Frame(results_frame, bg='#f0f0f0')
            frame.pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=item, font=("Arial", 10), bg='#f0f0f0').pack(side='left')
            label = tk.Label(frame, text="---", font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#e74c3c')
            label.pack(side='right')
            self.result_labels[item] = label
        
        # Informações adicionais
        info_frame = tk.LabelFrame(self.root, text="Observações", font=("Arial", 10, "bold"), bg='#f0f0f0')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = """
        • Esta calculadora usa as fórmulas exatas do site de referência
        • Os resultados são precisos se as medidas estiverem corretas
        • Considere uma tolerância de ±0.2mm nas medidas
        • Para bobinas com fita frouxa, o resultado será uma superestimativa
        • Alguns fabricantes deixam o início e fim da fita vazios
        """
        
        tk.Label(info_frame, text=info_text, font=("Arial", 9), bg='#f0f0f0', 
                justify='left', wraplength=750).pack(padx=10, pady=10)
    
    def update_component_pitch(self, event=None):
        """Atualiza o pitch baseado no tipo de componente selecionado"""
        pitches = {
            "0201": 1.0,  # 1mm pitch
            "0402": 2.0,  # 2mm pitch
            "0603": 4.0,  # 4mm pitch
            "0805": 4.0,  # 4mm pitch
            "1206": 4.0,  # 4mm pitch
            "1210": 4.0,  # 4mm pitch
            "1812": 4.0,  # 4mm pitch
            "2010": 4.0,  # 4mm pitch
            "2512": 4.0   # 4mm pitch
        }
        
        selected = self.component_type.get()
        if selected in pitches:
            self.component_pitch.set(pitches[selected])
    
    def calculate_quantity(self):
        """Calcula a quantidade de componentes na bobina usando as fórmulas corretas"""
        try:
            # Obter valores
            H = self.hub_internal_diameter.get()  # Diâmetro interno do hub
            m = self.hub_material_thickness.get()  # Espessura do material do hub
            R = self.roll_radius.get()  # Distância da borda do rolo até a borda interna do hub
            T = self.tape_thickness.get()  # Espessura da fita
            pitch = self.component_pitch.get()  # Pitch dos componentes
            
            # Validações básicas
            if any(v <= 0 for v in [H, m, R, T, pitch]):
                messagebox.showerror("Erro", "Todos os valores devem ser maiores que zero!")
                return
            
            # Cálculos baseados nas fórmulas do site de referência
            
            # 1. Diâmetro externo do rolo: D = H + 2R
            D = H + 2 * R
            
            # 2. Diâmetro interno do rolo (diâmetro externo do hub): d = H + 2m
            d = H + 2 * m
            
            # 3. Número de voltas: W = (D - d) / (2T)
            W = (D - d) / (2 * T)
            
            # 4. Comprimento da fita: L = ((D + d) / 2) * W * π
            L = ((D + d) / 2) * W * math.pi
            
            # 5. Quantidade de componentes: Q = L / pitch
            Q = L / pitch
            
            # Converter comprimento para metros
            L_meters = L / 1000
            
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

def main():
    root = tk.Tk()
    app = ComponentCountCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 