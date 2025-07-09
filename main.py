import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import pandas as pd
from datetime import datetime
import os

class ComponentCountCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Quantidade de Componentes em Bobinas")
        self.root.geometry("1300x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.component_type = tk.StringVar(value="0402")
        self.component_sku = tk.StringVar(value="")  # Nova variável para SKU
        self.hub_internal_diameter = tk.DoubleVar(value=56.0)  # Diâmetro interno do hub
        self.hub_material_thickness = tk.DoubleVar(value=2.0)  # Espessura do material do hub
        self.roll_radius = tk.DoubleVar(value=62.0)  # Distância da borda do rolo até a borda interna do hub
        self.tape_thickness = tk.DoubleVar(value=0.8)  # Espessura da fita
        self.component_pitch = tk.DoubleVar(value=4.0)  # Pitch dos componentes
        
        # Lista para armazenar dados dos componentes
        self.components_data = []
        
        # Variáveis para armazenar os últimos resultados calculados
        self.last_results = {}
        
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
        
        # Frame principal superior - Calculadora
        calculator_frame = tk.Frame(self.root, bg='#f0f0f0')
        calculator_frame.pack(padx=20, pady=10, fill='x')
        
        # Frame esquerdo - Parâmetros da bobina
        left_frame = tk.LabelFrame(calculator_frame, text="Parâmetros da Bobina", font=("Arial", 12, "bold"), bg='#f0f0f0')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Campo SKU
        tk.Label(left_frame, text="SKU do Componente:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w', padx=10, pady=5)
        sku_entry = tk.Entry(left_frame, textvariable=self.component_sku, width=20, font=("Arial", 10))
        sku_entry.pack(padx=10, pady=5)
        
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
        right_frame = tk.LabelFrame(calculator_frame, text="Informações e Resultados", font=("Arial", 12, "bold"), bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Informações sobre as medidas
        info_text = """
        Medidas necessárias:
        
        • SKU do componente
        • Tipo de componente
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
        
        # Frame para botões de ação
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        # Botão calcular
        calc_button = tk.Button(
            buttons_frame,
            text="Calcular Quantidade",
            command=self.calculate_quantity,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            padx=20,
            pady=10
        )
        calc_button.pack(side='left', padx=10)
        
        # Botão salvar
        save_button = tk.Button(
            buttons_frame,
            text="Salvar Componente",
            command=self.save_component,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            padx=20,
            pady=10
        )
        save_button.pack(side='left', padx=10)
        
        # Botão excluir
        delete_button = tk.Button(
            buttons_frame,
            text="Excluir Selecionado",
            command=self.delete_component,
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            padx=20,
            pady=10
        )
        delete_button.pack(side='left', padx=10)
        
        # Botão exportar
        export_button = tk.Button(
            buttons_frame,
            text="Exportar Excel",
            command=self.export_to_excel,
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            padx=20,
            pady=10
        )
        export_button.pack(side='left', padx=10)
        
        # Frame de resultados
        results_frame = tk.LabelFrame(self.root, text="Resultados do Cálculo", font=("Arial", 12, "bold"), bg='#f0f0f0')
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
        
        # Frame para tabela de componentes salvos
        table_frame = tk.LabelFrame(self.root, text="Componentes Salvos", font=("Arial", 12, "bold"), bg='#f0f0f0')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Criar Treeview para tabela - Adicionada coluna "Qtd Reels"
        columns = ('SKU', 'Tipo', 'Qtd Reels', 'Quantidade Total', 'Comprimento (m)', 'Voltas', 'Diâm. Ext. (mm)', 'Diâm. Int. (mm)', 'Data/Hora')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
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
        
        # Informações adicionais
        info_frame = tk.LabelFrame(self.root, text="Observações", font=("Arial", 10, "bold"), bg='#f0f0f0')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = """
        • Esta calculadora usa as fórmulas exatas do site de referência
        • Os resultados são precisos se as medidas estiverem corretas
        • Considere uma tolerância de ±0.2mm nas medidas
        • Para bobinas com fita frouxa, o resultado será uma superestimativa
        • Alguns fabricantes deixam o início e fim da fita vazios
        • Preencha o SKU e calcule antes de salvar o componente
        • Para múltiplos reels do mesmo SKU, escolha "Somar" para adicionar as quantidades
        """
        
        tk.Label(info_frame, text=info_text, font=("Arial", 9), bg='#f0f0f0', 
                justify='left', wraplength=1250).pack(padx=10, pady=10)
    
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
        """Mostra diálogo personalizado quando SKU já existe"""
        dialog = tk.Toplevel(self.root)
        dialog.title("SKU Já Existe")
        dialog.geometry("400x250")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        dialog.grab_set()  # Modal
        
        # Centralizar na janela pai
        dialog.transient(self.root)
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        result = {"choice": "cancel"}
        
        # Título
        tk.Label(dialog, text=f"SKU '{sku}' já existe!", 
                font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=10)
        
        # Informações atuais
        info_text = f"""Dados atuais:
Reels: {existing_component['reel_count']}
Quantidade total: {existing_component['quantity']:,}

Novo cálculo:
Quantidade: {self.last_results['quantity']:,}

Escolha uma ação:"""
        
        tk.Label(dialog, text=info_text, font=("Arial", 10), 
                bg='#f0f0f0', justify='left').pack(pady=10)
        
        # Frame para botões
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        def on_sum():
            result["choice"] = "sum"
            dialog.destroy()
            
        def on_replace():
            result["choice"] = "replace"
            dialog.destroy()
            
        def on_cancel():
            result["choice"] = "cancel"
            dialog.destroy()
        
        # Botões
        tk.Button(button_frame, text="Somar Quantidades", command=on_sum,
                 font=("Arial", 10, "bold"), bg='#27ae60', fg='white',
                 padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Substituir", command=on_replace,
                 font=("Arial", 10, "bold"), bg='#f39c12', fg='white',
                 padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Cancelar", command=on_cancel,
                 font=("Arial", 10, "bold"), bg='#e74c3c', fg='white',
                 padx=15, pady=5).pack(side='left', padx=5)
        
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

def main():
    root = tk.Tk()
    app = ComponentCountCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 