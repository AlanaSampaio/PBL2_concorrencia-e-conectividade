#Projeto Chat ZapZaps
Este projeto consiste em um sistema de chat criptografado, implementado em Python, com três versões distintas: uma sem criptografia, outra com criptografia simétrica e uma terceira com criptografia assimétrica.

Índice
Introdução
Fundamentação Teórica
Desenvolvimento
Funcionalidades e Interfaces
Como Executar a Aplicação
Áreas para Melhorias e Expansão
Considerações Finais

Introdução
O objetivo deste projeto é desenvolver um sistema de chat robusto e seguro, que utilize diferentes métodos de criptografia. A comunicação em rede é realizada através de sockets UDP, e a sincronização de mensagens é gerenciada por relógios de Lamport.

Fundamentação Teórica
Criptografia
Criptografia Simétrica: Utiliza a mesma chave para criptografar e descriptografar mensagens.
Criptografia Assimétrica: Utiliza um par de chaves, pública e privada, para a criptografia e descriptografia.

Sockets UDP
Comunicação de rede realizada através do protocolo UDP, que é rápido, mas não garante entrega de pacotes.

Relógio de Lamport
Mecanismo para sincronizar a ordem das mensagens em um sistema distribuído.

Desenvolvimento
Descreva brevemente como o projeto foi desenvolvido, mencionando as linguagens e ferramentas utilizadas.

Funcionalidades e Interfaces
Chat sem Criptografia
Envio e recepção de mensagens em tempo real.
Sincronização de mensagens através do relógio de Lamport.
Chat com Criptografia Simétrica
Todas as funcionalidades do chat sem criptografia.
Criptografia e descriptografia de mensagens utilizando Fernet (criptografia simétrica).
Chat com Criptografia Assimétrica
Funcionalidades básicas do chat.
Criptografia e descriptografia de mensagens utilizando RSA (criptografia assimétrica).

Como Executar a Aplicação
Forneça instruções detalhadas sobre como configurar e executar cada versão do chat.

Áreas para Melhorias e Expansão
Desenvolvimento de uma interface gráfica.
Implementação de um sistema de autenticação.
Melhoria na gestão de erros e exceções.

Considerações Finais
Sumarize os resultados alcançados e as possíveis direções futuras para o projeto.
