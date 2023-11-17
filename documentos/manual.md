# Manual Modelo Preditivo Artificial Air - Azul e Inteli
**Alysson Cordeiro, Henrique Schilder, Jean Rothstein, João Rodrigues, Luana Parra, Luiz Borges, Tainara Rodrigues**

## Sumário
[1. Introdução](#c1)

[2. Requisitos Prévios](#c2)
 
[3. Configuração do Ambiente de Desenvolvimento](#c3)

[4. Como rodar localmente](#c4)

[5. AWS](#c5)

[6. Problemas comuns](#c6)

## <a name="c1"></a>1. Introdução
O manual tem como objetivo fornecer um guia detalhado sobre como executar a aplicação desenvolvida para a Azul Linhas Aéreas Brasileiras, com foco na redução do consumo de combustível por meio da manutenção preditiva. Enquanto a documentação de explanação do projeto detalha o contexto e os objetivos, este manual é direcionado para aqueles que estão encarregados de implementar e operar a aplicação em um ambiente prático. Ele abrange a utilização das tecnologias avançadas, como machine learning, análise de dados e a infraestrutura da Amazon Web Services (AWS) para suportar o projeto.

Nas próximas seções deste manual, você encontrará instruções passo a passo sobre como configurar e executar a aplicação, aproveitando os serviços da AWS para coletar, armazenar e analisar dados críticos de voo. Além disso, detalharemos como implementar o modelo preditivo treinado para identificar falhas nos componentes dos motores das aeronaves. Através deste guia, você será capaz de compreender como todo o sistema opera de maneira integrada, contribuindo para a eficiência operacional, redução de custos e, mais importante, para a segurança operacional das aeronaves da Azul.

## <a name="c2"></a>2. Requisitos prévios
Antes de prosseguir com a implementação do projeto de Manutenção Preditiva para a Redução de Consumo de Combustível em Aeronaves Embraer E2 na AWS, é fundamental garantir que todos os requisitos prévios sejam atendidos. Isso inclui:

### 2.1 Sistema Operacional
Ubuntu Server 22.04 LTS (ou versão mais recente) ou outra distribuição Linux suportada.

Recursos de Hardware:
- Tipo de Instância: t3.medium para o frontend e t2.micro para o resto.
- CPU: Pelo menos 1 vCPU.
- RAM: Mínimo de 2 GB de RAM.
- Armazenamento: Espaço em disco suficiente para armazenar o projeto e seus componentes.

### 2.2 Conta AWS
Certifique-se de possuir uma conta ativa na Amazon Web Services (AWS). Caso ainda não tenha uma, você pode criar uma conta acessando o site da AWS e seguindo o processo de inscrição.

### 2.2.1 Acesso aos Recursos do Projeto
Você deve ter acesso aos recursos provisionados para o projeto, que incluem:

#### EC2 para o Backend
Garanta que uma instância EC2 tenha sido provisionada para servir como o backend da aplicação. Certifique-se de possuir informações sobre o endereço IP ou nome de DNS dessa instância, bem como as credenciais necessárias para se conectar a ela.

#### EC2 para o Frontend
Similarmente, verifique se uma instância EC2 foi configurada para hospedar o frontend da aplicação. Anote as informações de acesso para essa instância.

#### Amazon S3
Confirme se um bucket do Amazon S3 foi criado para armazenar arquivos estáticos, como imagens, CSS e JavaScript para o frontend da aplicação. Tenha em mãos as credenciais de acesso ao S3.

#### Amazon RDS
Garanta que um banco de dados Amazon RDS tenha sido configurado para armazenar os dados da aplicação. Anote as informações de conexão, como o endpoint do banco de dados, nome de usuário e senha.

### 2.3 Conhecimento básico da AWS
Antes de prosseguir, é altamente recomendável possuir conhecimento básico da AWS, incluindo:

- Navegação no Console da AWS.
- Uso da AWS CLI (Command Line Interface) para gerenciar recursos da AWS.
- Entendimento dos serviços da AWS, como EC2, S3, RDS e Lambda.
- Noções sobre segurança na AWS, incluindo grupos de segurança e políticas de acesso.

Ao garantir que todos esses requisitos prévios sejam atendidos, você estará preparado para avançar na configuração e execução da aplicação na AWS. Este manual fornecerá orientações detalhadas sobre como realizar cada etapa do processo.

## <a name="c3"></a>3. Configuração do Ambiente de Desenvolvimento

### 3.1 Instalação da AWS CLI
A AWS CLI é uma ferramenta de linha de comando que facilita a interação com a AWS. Siga os passos abaixo para instalá-la no seu ambiente de desenvolvimento:

1. Verifique os Requisitos do Sistema:

Certifique-se de que seu sistema atenda aos requisitos para instalar a AWS CLI. Você pode verificar esses requisitos no site oficial da AWS CLI.

2. Instalação em Windows, macOS ou Linux:

  - Windows:
    - Faça o download do instalador para Windows na página de download da AWS CLI.
    - Execute o instalador e siga as instruções na tela.
  - macOS (via Homebrew):
    - Abra o Terminal.
    - Execute o comando brew install awscli.
  - Linux (via gerenciador de pacotes):
    - Use o gerenciador de pacotes do seu sistema para instalar a AWS CLI.
      Por exemplo:
        - No Ubuntu, execute sudo apt-get install awscli.
        - No CentOS, execute sudo yum install aws-cli.

3. Verificação da Instalação:

Após a instalação, abra um terminal (ou Prompt de Comando no Windows) e digite aws --version. Você deverá ver a versão da AWS CLI instalada.

## <a name="c4"></a>4. Como rodar localmente?
1. Clonar o repositório na sua máquina utilizando o comando:

`git clone https://github.com/2023M7T2-Inteli/g4-artificial-air`

2. Dentro da pasta do projeto, rode o comando abaixo para o projeto rodar:

`sudo docker compose up`

Caso tenha a necessidade de rodar os componentes separadamente, siga os seguintes passos:

 - Frontend:
    - Dentro da pasta do projeto, entre na pasta frontend e rode o comandos para gerar a imagem e lançar o container:

      `docker build -t <image-name> . `

      `docker run -p <port-to-be-used>:3000 --name <container-name> <image-name> `

 - Backend:
    - Dentro da pasta do projeto, entre na pasta backend e rode o comandos para gerar a imagem e lançar o container:

      `docker build -t <image-name> . `

      `docker run -p <port-to-be-used>:3000 --name <container-name> <image-name> `

## <a name="c5"></a>5. AWS

Como já foi supracitado, para rodar a aplicação em nuvem, recomenda-se a criação de duas máquinas virtuais no EC2, tabelas relacionais em RDS e um bucket no S3.

1. EC2: Para lançar a instância no EC2, primeiro, deve-se fazer as configurações:
   - No painel do console da AWS, pesquise pelo serviço EC2.
   - Configure e execute a instância.
     Recomendações:
     * Nome: -
     * Imagem: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
     * Tipo de instância: t3.small
     * Par de chaves: Crie um novo par de chaves
     * Configurações de segurança: Permita tráfego HTTP & HTTPS da Internet
     * Configurações de armazenamento: Mantenha o padrão
   - Volte as opções da instância criadas, procure as opções de segurança e adicione as portas dos serviços do docker compose em "Editar regras de entrada".
   - Volte ao menu de instâncias e clique em conectar e em seguida, escolha o método de conexão.
   - Dentro da máquina virtual, configure-a para rodar os comandos necessários:
``` 
sudo apt update
sudo apt upgrade

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

2. S3:
Para o armazenamento dos arquivos .parquet sem tratamento, utilizamos o Bucket S3.
   - No painel do console da AWS, pesquise pelo serviço S3.
   - No canto superior direito, clique em criar bucket.
   - Configure o Bucket e depois crie-o:
     Recomendações:
     * Nome: -
     * Região da AWS: Leste dos EUA (Norte da Virgínia) us-east-1
     * Propriedade de objeto: ACLs Desabilitadas
     * Configurações de bloqueio do acesso público deste bucket: A ser definido conforme o uso
     * Versionamento de bucket: A ser definido conforme o uso
     * Tags - Opcional: ~
     * Criptografia Padrão: Mantenha o padrão
    
3. RDS
Para salvar em tabelas relacionais, utilizamos o RDS.
   - No painel do console da AWS, pesquise por RDS.
   - Para criar um banco de dados novo, selecione a opção Criar banco de dados.
   - Configure o banco:
     Recomendações:
     * Opções do mecanismo: PostgreSQL
     * Modelos: Produção
     * Disponibilidade e durabilidade: Cluster de banco de dados Multi-AZ
     * Configurações: Preferências de configuração
     * Configuração de instância: Classes padrão
     * Armazenamento: 400GiB (min)
     * Conectividade: Conectar-se a um recurso de computação do EC2
     * Autenticação de banco de dados:
     * Monitoramento: Preferência de configuração\

## <a name="c6"></a>6. Como Diagnosticar Problemas Comuns
Nesta seção, abordaremos como diagnosticar e solucionar problemas comuns que podem surgir durante a implementação e execução do projeto de Manutenção Preditiva para a Redução de Consumo de Combustível em Aeronaves Embraer E2 na AWS.

### 6.1 Resolução de Problemas
1. Aplicação Não Está Respondendo
   - Verifique se as instâncias EC2 que hospedam o frontend e o backend estão em execução e saudáveis.
   - Revise os logs de aplicação para verificar erros específicos.
   - Use a AWS CloudWatch para monitorar o desempenho das instâncias EC2 e identificar gargalos de recursos.
   - Verifique as configurações de grupos de segurança para garantir que as portas necessárias estejam abertas.
2. Erros de Conexão com o Banco de Dados
   - Verifique se o Amazon RDS está em execução e acessível.
   - Certifique-se de que as informações de conexão, como o endpoint do banco de dados, nome de usuário e senha, estejam corretas no código da aplicação.
   - Revise as permissões de acesso do banco de dados e certifique-se de que o papel IAM associado à instância EC2 tenha permissão para se conectar ao RDS.
3. Upload de Arquivos para o Amazon S3 Falha
   - Verifique se o bucket do Amazon S3 existe e está configurado corretamente.
   - Verifique as políticas de acesso no bucket do S3 para garantir que as permissões de escrita estejam corretas.
   - Certifique-se de que o código da aplicação esteja usando as credenciais AWS corretas para autenticação com o S3.
4. Erros de Execução de Funções Lambda (se aplicável)
   - Revise o código e a configuração da função Lambda em busca de erros de sintaxe.
   - Verifique se as permissões da função Lambda incluem acesso aos recursos AWS necessários.
   - Utilize o AWS CloudWatch para visualizar logs detalhados das execuções da função Lambda e identificar problemas.

### 6.2 Encerramento do Ambiente
Ao concluir o projeto ou quando for necessário encerrar o ambiente, siga as práticas recomendadas de encerramento para evitar custos não planejados e garantir a segurança dos recursos:

1. Encerre todas as instâncias EC2 que não estão mais em uso para evitar custos contínuos.
2. Faça backups dos dados importantes armazenados no Amazon RDS antes de desligar a instância do banco de dados.
3. Limpe os recursos temporários ou de teste, como buckets S3 ou funções Lambda, que não são mais necessários.
4. Revise e ajuste as políticas de retenção de logs no CloudWatch para manter apenas os logs necessários.
5. Desative ou exclua quaisquer recursos adicionais que foram provisionados para o projeto.
