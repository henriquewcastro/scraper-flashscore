## Descrição
Scraper criado em Python utilizando o Selenium e o BeautifulSoup para extrair as estatísticas das partidas de um campeonato de futebol no [Flashscore](https://www.flashscore.com.br/ "Flashscore").

## Informações
- Para utilizar o scraper basta adicionar os links dos campeonatos na lista urls do arquivo scraper.py e depois executar esse mesmo arquivo.
> O link tem que terminar com /resultados/, exemplo: https://www.flashscore.com.br/futebol/brasil/serie-a-2021/resultados/
- Os sufixos '_man' e '_vis' no nome das colunas da base são referentes aos times mandante e visitante respectivamente.
- Os valores nulos nas colunas de cartões normalmente são porque não ocorreram cartões na partida e os valores nulos em outras colunas costumam ser pelo flashscore não ter a estatística disponível, mas se uma partida inteira estivar com valores nulos provavelmente ocorreu um erro no scraping, tente executar novamente o scraper.