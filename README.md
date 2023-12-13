<h1 align="center">TEC502 - ZapsZap</h1>   
  Este projeto consiste em um sistema de chat criptografado, implementado em Python, com três versões distintas: uma sem criptografia, outra com criptografia simétrica e uma terceira com criptografia assimétrica.


<h2>Índice</h2>

• <a href="#introducao">Introdução</a>

• <a href="#fundamentacao">Fundamentação Teórica</a>

• <a href="#desenvolvimento">Desenvolvimento</a>

• <a href="#funcionalidade">Funcionalidades e Interfaces</a>

• <a href="#execucao">Como Executar a Aplicação</a>

• <a href="#melhoria">Áreas para Melhorias e Expansão</a>

• <a href="#consideracoes">Considerações Finais</a>



<h2 id="introducao">Introdução</h2>

  Este projeto visa desenvolver sistemas de chat robustos e seguros, explorando diferentes métodos de criptografia e estratégias de comunicação em rede. As aplicações foram implementadas em Python, utilizando o Visual Studio Code como ambiente de desenvolvimento e os recursos computacionais do Laboratório de Redes e Sistemas Distribuídos (LARSID) para testes e simulações



<h2 id="fundamentacao">Fundamentação Teórica</h2>

<h3>Criptografia</h3>
• Criptografia Simétrica:  A abordagem utiliza uma única chave para criptografar e descriptografar mensagens, garantindo a confidencialidade e segurança das comunicações.

• Criptografia Assimétrica: Este método incorpora um par de chaves (pública e privada) para criptografar e descriptografar mensagens. No caso específico, a implementação faz uso do algoritmo RSA para garantir segurança adicional.

<h3>Sockets UDP</h3>
• A comunicação em rede é realizada através do protocolo UDP, proporcionando rapidez na transmissão de dados, embora não garanta a entrega confiável de pacotes.

<h3>Relógio de Lamport</h3>
• Um mecanismo eficaz para sincronizar a ordem dos eventos em sistemas distribuídos, crucial para manter a lógica e a consistência nas mensagens.



<h2 id="desenvolvimento">Desenvolvimento</h2>

• O código foi desenvolvido em Python, fazendo uso de bibliotecas padrão da indústria, como cryptography, pickle e threading. O Visual Studio Code proporcionou um ambiente de desenvolvimento eficiente, e os recursos do LARSID foram empregados para testar as comunicações em ambiente real.



<h2 id="funcionalidade">Funcionalidades e Interfaces</h2>

<h3>Chat sem Criptografia</h3>
• Envio e recepção de mensagens em tempo real.

• Sincronização de mensagens através do relógio de Lamport.
<h3>Chat com Criptografia Simétrica</h3>
• Todas as funcionalidades do chat sem criptografia.

• Criptografia e descriptografia de mensagens utilizando Fernet (criptografia simétrica).
<h3>Chat com Criptografia Assimétrica</h3>
• Funcionalidades básicas do chat.

• Criptografia e descriptografia de mensagens utilizando RSA (criptografia assimétrica).



<h2 id="execucao">Como Executar a Aplicação</h2>

Para executar o servidor do chat, siga as etapas abaixo utilizando o Docker. Certifique-se de ter o Docker instalado em sua máquina antes de começar.

Crie uma rede para cada chat (chat, chat2 e chat3).

```$ docker network create chat ```

Certifique-se de estar no diretório que contém seu Dockerfile e execute o seguinte comando para construir a imagem:

```$ docker build -t chat-app . ```

Agora, você pode executar o contêiner de forma interativa, conectando-o à rede

```$ docker run -it --network=chat chat-app ```

Esses comandos se aplicam aos módulos chat, chat2 e chat3.

***




<h2 id="melhoria">Áreas para Melhorias e Expansão</h2>

• Desenvolvimento de uma interface gráfica.
  
• Implementação de um sistema de autenticação via e-mail ou sms.

• Melhoria na gestão de erros e exceções.



<h2 id="consideracoes">Considerações Finais</h2>
  Este projeto resultou em um sistema de chat robusto, seguro e versátil, oferecendo diferentes níveis de criptografia para atender às necessidades específicas dos usuários. A implementação bem-sucedida de relógios de Lamport proporcionou uma sincronização eficaz, garantindo a consistência da ordem das mensagens em ambientes distribuídos. Futuras melhorias podem incluir a expansão das funcionalidades e aprimoramentos na usabilidade, proporcionando uma solução abrangente para comunicações seguras e privadas.
