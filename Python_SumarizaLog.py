import pandas as pd

def processar_resumos(file_path):
    """
    Processa um arquivo Excel, lê a primeira coluna, classifica o texto
    com base em palavras-chave e adiciona a classificação como uma nova coluna 'Resumo'.

    Args:
        file_path (str): O caminho completo para o arquivo Excel de entrada.
    """
    # Carregar o arquivo Excel
    # A função read_excel lê o conteúdo do arquivo Excel para um DataFrame pandas.
    df = pd.read_excel(file_path)

    # Processar a primeira coluna (índice 0) e gerar resumos
    # Converte o conteúdo da primeira coluna para uma lista de strings.
    texts_a = df.iloc[:, 0].tolist()
    summaries_a = [] # Lista para armazenar os resumos gerados

    # Itera sobre cada texto na lista para classificação
    for text in texts_a:
        # Verifica se o item é uma string e não está vazio após remover espaços em branco
        if isinstance(text, str) and text.strip():
            # Converte o texto para minúsculas para uma comparação de palavras-chave case-insensitive
            text_lower = text.lower()

            # Lógica de classificação baseada em palavras-chave
            if "bilhete" in text_lower or "emissão" in text_lower:
                summary = "VOUCHER"
            elif "pcd" in text_lower or "diária" in text_lower:
                summary = "DIARIA"
            elif "solicita" in text_lower or "pedido" in text_lower:
                summary = "SOLICTACAO"
            elif "autorização" in text_lower or "autoriza" in text_lower:
                summary = "AUTORIZACAO"
            elif "informação" in text_lower or "inscrição" in text_lower:
                summary = "INFORMACAO"
            elif "parecer" in text_lower:
                summary = "PARECER"
            elif "negativa" in text_lower or "indeferir" in text_lower:
                summary = "NEGATIVA"
            else:
                summary = "ANALISE" # Categoria padrão se nenhuma palavra-chave for encontrada
            summaries_a.append(summary)
        else:
            # Adiciona uma string vazia se o texto não for válido (não-string ou vazio)
            summaries_a.append("")

    # Atualizar o dataframe com os resumos na nova coluna 'Resumo'
    df['Resumo'] = summaries_a

    # Salvar o dataframe atualizado em um novo arquivo Excel
    # O novo arquivo terá '_resumido.xlsx' adicionado ao nome original.
    # index=False evita que o índice do DataFrame seja salvo como uma coluna no Excel.
    output_path = file_path.replace('.xlsx', '_resumido.xlsx')
    df.to_excel(output_path, index=False)
    print(f'Resumos salvos em: {output_path}')

if __name__ == "__main__":
    # Exemplo de uso:
    # Solicita ao usuário o caminho do arquivo Excel.
    # file_path = input("Digite o caminho completo do arquivo Excel: ")

    # Caminho do arquivo fixo para o exemplo fornecido.
    # Certifique-se de que este caminho esteja correto para a execução.
    processar_resumos("C:\\Users\\020181551287\\Documents\\PPGMCS\\Experimento\\parte3-sumarizar\\teste_14052025.xlsx")
