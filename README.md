# AWS-GLUE-EKS-EMR
<br />Cria uma aplicação que gera milhares de dados fake estruturados em tabelas distintas. Os diferentes estágios de ingestão, processamento e consulta de resultados se dão em um datalakehouse utilizando alguns dos principais serviços da AWS, a exemplo do AWS Lambda, responsável por determinados deploys. O processamento é feito com um só script, que usa o AWS Glue, Amazon EMR e Amazon EKS, diferentes serviços com um mesmo fim. O output gera também arquivos delta. O Amazon Athena, serviço sem servidor, possibilita uma análise interativa dos dados. A infraestrutura de ingestão, processamento e consulta é implementada usando Terraform como gerador de IAC (infra as code) em cada um desses três estágios. Por fim, o Metabase é utilizado como ferramenta de BI para prover a parte visual e insights do projeto. <br />
As três tabelas geram dados de clientes, pontuação de cartão de crédito e gêneros musicais preferenciais destes consumidores. Como trata-se de dados não verdadeiros, oriundos de uma biblioteca Python, não se busca uma correlação lógica, apenas enriquecimento das tabelas nos devidos estágios.  

## Arquitetura
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/00_arquitetura.png"/>
</p>

### Recursos e serviços utilizados:

* Terraform para provisionar a infraestrutura do projeto em seus diferentes estágios
* Amazon s3 que armazena os objetos em buckets
* AWS Lambda que sobe e faz o deploy de aplicações diversas
* Amazon RDS como serviço de banco de dados relacional gerenciado 
* AWS DMS que extrai os dados do RDS e envia para a camada “landing”
* AWS IAM o recurso que permite gerenciar acessos 
* Amazon VPC como principal serviço de gerenciamento de rede  
* Amazon Kinesis um serviço de captura de dados em tempo real, que nesse caso captura logs
* AWS Glue que processa e cataloga os dados sem servidor
* Amazon EMR uma plataforma de clusters gerenciada que assim como o glue processa dados, porém com foco em Big data
* Amazon EKS serviço gerenciado de baixo custo que gerencia kubernetes na AWS, que assim como os dois anteriores, processa os dados
* Docker para subir as imagens utilizadas no processamento
* Amazon Athena responsável por analisar os dados diretamente dos buckets 
* Metabase uma ferramenta open source de BI que se conecta ao Amazon Athena para gerar dashboards
* Dbeaver também uma ferramenta open source que se conecta ao RDS para consultas diversas

### Preparo preliminar do ambiente
* O projeto foi desenvolvido no Windows utilizando WSL2, podendo também ser feito nos demais sistemas operacionais
* É necessário criar uma conta AWS, tomar nota dos ID’s e segredos necessários para o desenvolvimento
* Ferramentais como a instalação do Python, Docker, Terraform e AWS CLI, Metabase também são necessários. 

# Infraestrutura de ingestão 
<br />Dentro da pasta do projeto na IDE de preferência, inicia-se o processo de inserção de credenciais. A comunicação entre a IDE e a AWS se dá pela AWS CLI, uma interface de linha de comando. Feita a conexão, inicia-se o processo de subida de infraestrutura pelo Terraform. <br />


### Amazon s3
<br />Os componentes de armazenamento constituem o data lakehouse (a fusão de data lakes e data warehouses em um único sistema). 
Na landing zone, são depositados os dados em seu estado bruto, sem alterações, antes mesmo de serem enviados para a bronze. No projeto, os dados já são depositados em parquet, formato colunar de grande compressão e eficiência; <br />
<br />Em bronze, os dados são uma cópia da landing zone, porém com formato mais eficiente, como o parquet caso o formato na landing fosse outro;
Na silver layer, ficam os dados refinados, com conjuntos de registros prontos para consumo. No projeto os dados consultados foram desta camada;<br />
<br />Em gold layer ficam as tabelas agregadas. No código é feito um join com as três tabelas;<br />
<br />A pasta kinesis guarda os logs dos erros gerados pelos dados gerados em tempo real;<br />
<br />O bucket de scripts guarda os códigos e arquivos necessários para o processamento. Diversos serviços são implantados, nos texto abaixo há prints e o papel de cada um deles no desenvolvimento do projeto:
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/01_buckets.png"/>
</p>

### Amazon RDS
É criado o banco de dados projeto, os demais dados serão gerados pela AWS lambda.
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/02_RDS.png"/>
</p>

### AWS Lambda
No processo de criação de infraestrutura, é necessário empacotar as funções para serem geradas as lambdas. São duas, uma que transforma e envia os logs gerados pelo kinesis para o bucket correspondente e outra que cria e copula as tabelas em MySQL no RDS.
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/03_lambdas.png"/>
</p>
O processo de escrita no RDS pode ser acompanhado em tempo real, basta copiar as credenciais do endpoint do RDS, inserir o nome do banco e as credenciais. Conforme resultado abaixo:
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/04_lambda1.png"/>
</p>

### AWS DMS 
Aqui são criados dois endpoints, um de origem dos dados e outro de destino, uma instancia de replicação e uma tarefa de migração de banco de dados. 
Ao fim do processo de migração o DMS extrai os dados do Amazon RDS e os insere na landing zone. As pastas customers, credit_score e music são criadas contando os dados brutos.
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/05_DMS.png"/>
</p>
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/06_DMS_load.png"/>
</p>

### Amazon Kinesis
O serviço é criado e captura os logs para consumo, conforme demonstrado nas imagens abaixo: 
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/07_kinesis.png"/>
</p>
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/08_lambda2.png"/>
</p>

# Infraestrutura de processamento
<br />O processamento é repetido com três ferramentas distintas, com o glue, de maior custo entre os três, porém o que demanda menos tempo e habilidade para construção; com o EMR, um meio termo entre custo e esforço de construção, e por fim o EKS, solução mais barata entre as três que utiliza soluções open source, porém que depende de variadas ferramentas para o funcionamento, o que traz grande esforço de construção. <br />
<br />Os três serviços utilizam o mesmo job com arquivos que parametrizam o processamento dos arquivos Delta, é utilizado overwrite, como há uma tabela de catálogo neste formato, não há duplicação de dado, então é possível escrever apenas o arquivo novo ou modificado. Em variables ficam as querys em si, suas transformações e etc. Por fim a classe main etl.py que faz a chamada da classe para a escrita nas camadas correspondentes. <br />
<br />Todos os processamentos geram delta logs, um histórico de execuções dos Jobs e o symlink format manifest, o mapeamento dos arquivos inseridos citado no parágrafo anterior. <br />
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/09_job.png"/>
</p>

### AWS Glue
O processamento utilizando o AWS Glue é o mais simples de todos, um script com poucas linhas é suficiente para criar o glue job. Após criado, basta executar para que as tabelas sejam escritas nas devidas camadas. 
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/10_glue_job.png"/>
</p>

### Amazon EMR
Para o deploy é utilizado AWS Lambda que sobe um Amazon EMR via função. O empacotamento dos arquivos como na ingestão também é necessário.  Após conclusão basta rodar a lambda para construção do cluster conforme abaixo:
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/11_lambdas_emr.png"/>
</p>
Quando o cluster estiver em estado “waiting” será necessário sincronizar uma Key Pairs, serviço da AWS. Se finalizado o processo anterior, basta iniciar a outra lamba chamada step para iniciar o processamento em si. A terceira lambda derruba o cluster. 
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/12_cluster_EMR.png"/>
</p>

### Amazon EKS
<br />O objetivo é provisionar um cluster kubernets na AWS e instalar o Spark operator nele, depois processar o job com os mesmos arquivos de origem, a exemplo dos serviços anteriores. Resumo do passo a passo:<br />
<br />1. Criar o cluster via Terraform utilizando módulos que a HashiCorp disponibiliza.<br />
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/13_cluster_EKS.png"/>
</p>
<br />2. Conectar via kubectl<br />
<br />3. Criar a infraestrutura via Docker construindo e fazendo push da imagem<br />
<br />4.Gerar um namespace Spark para o Spark operator<br />
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/14_operador%20spark.png"/>
</p>
<br />5. Inserir secrets para a conexão<br />
<br />6.Iniciar o processamento utilizando Spark<br />
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/15_processamento_EKS.png"/>
</p>
<br />Em um resumo geral de processamento, o AWS Glue se mostra eficiente para dados menores que demandam pouco tempo de elaboração, porque é cobrado por tempo e principalmente por unidade de processamento de dados. Já o EMR é ideal para processamentos mais duradouros e seu custo final dependerá de qual instancia está sendo utilizada, além do tempo de uso da mesma, o que está sendo processado não impacta no custo. E o EKS para performance ao menor custo possível, com maior quantidade de variáveis para construção. O que está sendo processado também não é levado em consideração. <br />

# Consulta e BI
A consulta dos dados será feita via Amazon Athena, para isso é necessário que o Crawler do AWS Glue catalogue os dados das tabelas. Já a parte de BI será feita via Metabase, assim que os dados ficam disponíveis para o Amazon Athena.  

### Glue Crawler
O script terraform cria um crawler, uma database e uma Delta connection. Ao rodar o crawler, o glue cataloga os dados na database criada possibilitando a consulta serverless no Amazon Athena.  
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/16_crawler.png"/>
</p>

### Amazon Athena
Aqui é possível consultar as tabelas catalogadas pelo crawler do glue utilizando comandos SQL, inclusive joins como no exemplo abaixo:
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/17_athena.png"/>
</p>

### Metabase
Por fim o Metabase, ferramenta open source, se conecta e utiliza o Athena para ter acesso aos dados finais. Aqui também é possível manipulações diversas utilizando SQL e também é possível criar dashboards atualizados em tempo real. O painel mostra os totais das tabelas, idade dos consumidores, seus sexos, o que acontece em cada mês do ano, cria-se uma análise fictícia entre o gênero musical preferencial de animes e uma possível tendência a consumo de produtos geek etc.  
<p align="center">
<img src="https://github.com/LeandroRFausto/AWS-GLUE-EKS-EMR/blob/main/imagens/18_painel.png"/>
</p>









   



