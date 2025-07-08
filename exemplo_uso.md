# Exemplo Prático de Uso

## Cenário: Bobina de Resistores 0603

### Medidas Reais da Bobina:
- **Diâmetro interno do hub (H)**: 56 mm
- **Espessura do material do hub (m)**: 2 mm
- **Raio do rolo (R)**: 62 mm (medido da borda até o hub)
- **Espessura da fita (T)**: 0.8 mm (fita de papel)
- **Pitch dos componentes**: 4 mm (padrão para 0603)

### Passos na Aplicação:

1. **Selecione o tipo**: Escolha "0603" no dropdown
2. **Preencha as medidas**:
   - Diâmetro Interno do Hub: 56.0
   - Espessura do Material do Hub: 2.0
   - Raio do Rolo (R): 62.0
   - Espessura da Fita: 0.8
   - Pitch dos Componentes: 4.0 (preenchido automaticamente)

3. **Clique em "Calcular Quantidade"**

### Resultados Esperados:
- **Quantidade Total de Componentes**: 7,068
- **Comprimento da Fita**: 28.3 m
- **Número de Voltas**: 75.0
- **Diâmetro Externo do Rolo**: 180.0 mm
- **Diâmetro Interno do Rolo**: 60.0 mm

## Cenário: Bobina de Capacitores 0402

### Medidas Reais da Bobina:
- **Diâmetro interno do hub (H)**: 56 mm
- **Espessura do material do hub (m)**: 2 mm
- **Raio do rolo (R)**: 62 mm
- **Espessura da fita (T)**: 0.8 mm
- **Pitch dos componentes**: 2 mm (padrão para 0402)

### Resultados Esperados:
- **Quantidade Total de Componentes**: 14,137
- **Comprimento da Fita**: 28.3 m
- **Número de Voltas**: 75.0

## Cenário: Bobina de 13" (330mm)

### Medidas Reais da Bobina:
- **Diâmetro interno do hub (H)**: 85 mm
- **Espessura do material do hub (m)**: 2 mm
- **Raio do rolo (R)**: 122.5 mm
- **Espessura da fita (T)**: 0.8 mm
- **Pitch dos componentes**: 4 mm

### Resultados Esperados:
- **Quantidade Total de Componentes**: 24,783
- **Comprimento da Fita**: 99.1 m
- **Número de Voltas**: 150.0

## Dicas de Medição:

### Como medir o Raio do Rolo (R):
1. Coloque a bobina em uma superfície plana
2. Meça a distância total do centro até a borda externa
3. Subtraia o raio do hub (H/2 + m)
4. Ou meça diretamente da borda do rolo até a borda interna do hub

### Como medir a Espessura da Fita (T):
1. Use um paquímetro digital
2. Meça a espessura da fita de embalagem
3. Valores típicos:
   - Fita de papel: 0.8 mm
   - Fita plástica: 0.1 mm

### Valores Típicos por Tipo de Bobina:

| Tipo de Bobina | H (mm) | m (mm) | R (mm) | T (mm) |
|----------------|--------|--------|--------|--------|
| 7" (178mm)     | 56     | 2      | 61     | 0.8    |
| 13" (330mm)    | 85     | 2      | 122.5  | 0.8    |
| Mini-bobina    | 50     | 0      | 25     | 0.8    |

## Verificação da Precisão:

Para verificar se suas medidas estão corretas:
1. Meça o diâmetro total da bobina
2. Calcule: D = H + 2R
3. Compare com sua medida real
4. Se houver diferença > 2mm, verifique suas medidas

## Observações Importantes:

- **Fita frouxa**: Resultado será uma superestimativa
- **Lead-in/Lead-out**: Alguns fabricantes deixam o início/fim vazio
- **Tolerância**: Considere ±5-10% nos resultados finais
- **Medidas precisas**: Use paquímetro digital para melhor acurácia 