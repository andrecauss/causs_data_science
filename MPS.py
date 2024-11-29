import seaborn as sns
import matplotlib.pyplot as plt

# Função para exibir o gráfico de sequenciamento de produção
def grafico_sequenciamento_producao(demandas_sequenciadas):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=demandas_sequenciadas, x="Item", y="Quantidade", hue="Data de Necessidade", palette="viridis")
    plt.title("Sequenciamento de Produção - Data de Necessidade")
    plt.xlabel("Item")
    plt.ylabel("Quantidade Demandada")
    plt.xticks(rotation=45)
    plt.legend(title="Data de Necessidade")
    plt.tight_layout()
    plt.show()

# Função para exibir gráfico comparativo de estoques
def grafico_estoques(estoque_inicial, estoque_atualizado):
    estoque_inicial_ = estoque_inicial[['Item/Componente', 'Quantidade Atual']].copy()
    estoque_inicial_['Status'] = 'Inicial'
    
    estoque_atualizado_ = estoque_atualizado[['Item/Componente', 'Quantidade Atual']].copy()
    estoque_atualizado_['Status'] = 'Atualizado'
    
    estoque_comparado = pd.concat([estoque_inicial_, estoque_atualizado_])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=estoque_comparado, x='Item/Componente', y='Quantidade Atual', hue='Status')
    plt.title("Comparação de Estoques - Antes e Depois")
    plt.xlabel("Item/Componente")
    plt.ylabel("Quantidade no Estoque")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para exibir gráfico de carga das máquinas
def grafico_carga_maquinas(tempo_por_maquina):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=tempo_por_maquina.index, y=tempo_por_maquina.values, palette="Blues_d")
    plt.title("Carga das Máquinas")
    plt.xlabel("Máquina")
    plt.ylabel("Tempo Total Necessário (minutos)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Código principal de execução
logging.info("Iniciando o planejamento mestre de produção.")

try:
    # Sequenciamento de produção
    demandas_sequenciadas = sequenciar_producao(demandas)
    
    # Visualizar sequenciamento de produção
    grafico_sequenciamento_producao(demandas_sequenciadas)
    
    # Explosão de materiais
    necessidades_componentes = calcular_necessidades(demandas_sequenciadas, componentes, estoques)
    
    # Atualizar estoques
    estoque_atualizado = atualizar_estoques(demandas_sequenciadas, necessidades_componentes, estoques)
    
    # Visualizar comparação de estoques
    grafico_estoques(estoques, estoque_atualizado)
    
    # Cálculo do tempo por máquina
    tempo_por_maquina = calcular_tempo_por_maquina(demandas_sequenciadas, processos)
    
    # Visualizar carga das máquinas
    grafico_carga_maquinas(tempo_por_maquina)
    
    # Exportar resultados
    with pd.ExcelWriter("resultado_planejamento.xlsx") as writer:
        demandas_sequenciadas.to_excel(writer, sheet_name="Cronograma Itens", index=False)
        necessidades_componentes.to_excel(writer, sheet_name="Necessidades Componentes", index=False)
        estoque_atualizado.to_excel(writer, sheet_name="Estoque Atualizado", index=False)
    
    logging.info("Processo de planejamento concluído com sucesso!")
except Exception as e:
    logging.error(f"Erro durante o planejamento: {e}")