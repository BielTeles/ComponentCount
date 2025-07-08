# 🎯 ComponentCount Calculator

> **Calculadora inteligente para estimar a quantidade de componentes SMD em bobinas**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://windows.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 O que é isso?

Imagine que você está trabalhando com componentes eletrônicos SMD e precisa saber quantos componentes restam em uma bobina. Em vez de contar um por um (que seria uma tarefa interminável! 😅), esta calculadora faz isso matematicamente para você!

**ComponentCount Calculator** é uma aplicação desktop que calcula a quantidade estimada de componentes em bobinas usando fórmulas matemáticas precisas, baseadas na calculadora online da [CompuPhase](https://www.compuphase.com/electronics/reelestimate.htm).

---

## ✨ Por que usar esta calculadora?

- 🎯 **Precisão Matemática**: Usa fórmulas exatas, não aproximações
- 🚀 **Fácil de Usar**: Interface intuitiva e moderna
- 📱 **Executável Standalone**: Não precisa instalar Python
- 🔧 **Múltiplos Componentes**: Suporte para 9 tipos diferentes
- 📊 **Resultados Detalhados**: Quantidade, comprimento, voltas e mais
- 💡 **Baseada em Referência**: Fórmulas validadas e confiáveis

---

## 🎮 Como Funciona?

### A Mágica da Matemática! 🧮

A calculadora usa estas fórmulas exatas:

1. **Diâmetro externo**: `D = H + 2R`
2. **Diâmetro interno**: `d = H + 2m`
3. **Número de voltas**: `W = (D - d) / (2T)`
4. **Comprimento da fita**: `L = ((D + d) / 2) × W × π`
5. **Quantidade**: `Q = L / pitch`

### Componentes Suportados 📦

| Tipo | Pitch | Uso Típico |
|------|-------|------------|
| 0201 | 1mm | Componentes ultra-miniaturizados |
| 0402 | 2mm | Smartphones, wearables |
| 0603 | 4mm | Eletrônicos gerais |
| 0805 | 4mm | Placas de circuito |
| 1206 | 4mm | Aplicações industriais |
| 1210 | 4mm | Alta potência |
| 1812 | 4mm | Componentes especiais |
| 2010 | 4mm | Aplicações específicas |
| 2512 | 4mm | Componentes grandes |

---

## 🚀 Começando

### Opção 1: Executável (Recomendado) ⭐

1. **Baixe** o arquivo `ComponentCount.exe`
2. **Execute** com duplo clique
3. **Pronto!** Não precisa instalar nada

### Opção 2: Código Fonte

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ComponentCount.git
cd ComponentCount

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python main.py
```

---

## 📖 Como Usar

### Passo a Passo Simples 🎯

1. **Abra a aplicação** (duplo clique no .exe)
2. **Selecione o tipo** de componente (ex: 0603)
3. **Meça sua bobina** e preencha os valores:
   - **H**: Diâmetro interno do hub (56mm típico)
   - **m**: Espessura do material (2mm típico)
   - **R**: Raio do rolo (medido da borda até o hub)
   - **T**: Espessura da fita (0.8mm papel, 0.1mm plástico)
4. **Clique em "Calcular"**
5. **Veja os resultados**! 🎉

### Exemplo Prático 📝

**Bobina de Resistores 0603:**
- H = 56mm, m = 2mm, R = 62mm, T = 0.8mm
- **Resultado**: 7,068 componentes (28.3m de fita)

**Bobina de Capacitores 0402:**
- Mesmas medidas, mas pitch = 2mm
- **Resultado**: 14,137 componentes

---

## 🔧 Medindo sua Bobina

### Dicas para Medições Precisas 📏

#### Como medir o Raio (R):
1. Coloque a bobina em uma superfície plana
2. Meça da borda externa até a borda interna do hub
3. Ou calcule: `(Diâmetro_total - Diâmetro_hub) / 2`

#### Valores Típicos:
| Tipo de Bobina | H (mm) | m (mm) | R (mm) | T (mm) |
|----------------|--------|--------|--------|--------|
| 7" (178mm) | 56 | 2 | 61 | 0.8 |
| 13" (330mm) | 85 | 2 | 122.5 | 0.8 |
| Mini-bobina | 50 | 0 | 25 | 0.8 |

---

## 📊 Resultados Esperados

### O que você vai ver:

- 🎯 **Quantidade Total**: Número de componentes na bobina
- 📏 **Comprimento da Fita**: Em metros
- 🔄 **Número de Voltas**: Voltas na bobina
- 📐 **Diâmetros**: Interno e externo do rolo

### Precisão dos Resultados:

- ✅ **Fórmulas**: Matematicamente exatas
- ⚠️ **Tolerância**: ±5-10% (depende da precisão das medidas)
- 📏 **Medidas**: Use paquímetro digital para melhor acurácia
- 🔍 **Fatores**: Fita frouxa pode superestimar o resultado

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
ComponentCount/
├── main.py                 # Aplicação principal
├── test_calculations.py    # Testes dos cálculos
├── ComponentCount.spec     # Configuração do PyInstaller
├── requirements.txt        # Dependências
├── dist/ComponentCount.exe # Executável final
└── docs/                   # Documentação
```

### Build do Executável

```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller ComponentCount.spec

# O executável estará em dist/ComponentCount.exe
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! 🎉

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Sugestões de Melhorias:

- 🎨 Novos temas de interface
- 📱 Suporte para mais tipos de componentes
- 🌍 Traduções para outros idiomas
- 📊 Gráficos e visualizações
- 💾 Salvar/carregar configurações

---

## 🐛 Solução de Problemas

### Aplicação não abre?
- ✅ Verifique se o antivírus não bloqueou
- ✅ Execute como administrador
- ✅ Verifique se o Windows está atualizado

### Resultados incorretos?
- ✅ Verifique se as medidas estão corretas
- ✅ Use paquímetro digital para melhor precisão
- ✅ Consulte os valores típicos na documentação

### Erro de execução?
- ✅ Instale o Visual C++ Redistributable
- ✅ Verifique se tem espaço em disco suficiente

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- **CompuPhase**: Pela calculadora online que serviu como referência
- **Python Community**: Pelas ferramentas incríveis
- **Tkinter**: Pela interface gráfica nativa
- **PyInstaller**: Por tornar possível criar executáveis standalone

---

## 📞 Suporte

Precisa de ajuda? 🤔

- 📖 **Documentação**: Veja os arquivos `.md` no projeto
- 🧪 **Testes**: Execute `test_calculations.py` para verificar os cálculos
- 💬 **Issues**: Abra uma issue no GitHub
- 📧 **Email**: Entre em contato para suporte

---

## ⭐ Se este projeto te ajudou...

Se esta calculadora te salvou de contar milhares de componentes manualmente, considere dar uma ⭐ no repositório! 

**Compartilhe com outros engenheiros e técnicos que também precisam dessa ferramenta!** 🚀

---

**Feito com ❤️ para a comunidade de eletrônicos** 