# Webscrapselenium
Pegando dados de endereços de bases do site da FAB
workflow:
[ INÍCIO ]
    |
    v
[ Lista de URLs por estado ]
    |
    v
[ Para cada URL de estado ]
    |
    v
[ Abrir página do estado ]
    |
    v
[ Coletar todos os links das unidades ]
    |
    v
[ Para cada link de unidade ]
    |
    v
[ Abrir página da unidade ]
    |
    v
[ Extrair nome, endereço, CEP, cidade, estado ]
    |
    v
[ Salvar os dados numa lista ]
    |
    v
[ Repetir para todas as unidades ]
    |
    v
[ Criar DataFrame com Pandas ]
    |
    v
[ Exportar para Excel na pasta Downloads ]
    |
    v
[ FIM ]
