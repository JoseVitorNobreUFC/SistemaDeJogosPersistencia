# SistemaDeJogosPersistencia

Neste trabalho será desenvolvido um CRUD para um sistema de jogos digitais. As entidades principais desse sistema são:

- Jogo

<table> <thead> <tr> <th>Campo</th> <th>Tipo de dado</th> <th>Restrições</th> <th>Descrição</th> </tr> </thead> <tbody> <tr> <td>id</td> <td>Inteiro</td> <td>Chave primária, não nulo, auto incremento</td> <td>Identificador único do jogo</td> </tr> <tr> <td>titulo</td> <td>Texto (string)</td> <td>Não nulo</td> <td>Título do jogo</td> </tr> <tr> <td>descricao</td> <td>Texto longo</td> <td>Opcional</td> <td>Descrição detalhada do jogo</td> </tr> <tr> <td>data_lancamento</td> <td>Data</td> <td>Não nulo</td> <td>Data oficial de lançamento do jogo</td> </tr> <tr> <td>preco</td> <td>Decimal</td> <td>Não nulo</td> <td>Preço atual do jogo</td> </tr> <tr> <td>desenvolvedora</td> <td>Texto (string)</td> <td>Não nulo</td> <td>Nome do estúdio desenvolvedor do jogo</td> </tr> </tbody> </table>

- Usuário

<table> <thead> <tr> <th>Campo</th> <th>Tipo de dado</th> <th>Restrições</th> <th>Descrição</th> </tr> </thead> <tbody> <tr> <td>id</td> <td>Inteiro</td> <td>Chave primária, não nulo, auto incremento</td> <td>Identificador único do usuário</td> </tr> <tr> <td>nome</td> <td>Texto (string)</td> <td>Não nulo</td> <td>Nome do usuário</td> </tr> <tr> <td>email</td> <td>Texto (string)</td> <td>Não nulo, único</td> <td>E-mail utilizado no cadastro</td> </tr> <tr> <td>senha_hash</td> <td>Texto (string)</td> <td>Não nulo</td> <td>Hash da senha do usuário</td> </tr> <tr> <td>data_cadastro</td> <td>Timestamp</td> <td>Não nulo</td> <td>Data e hora do cadastro do usuário</td> </tr> <tr> <td>pais</td> <td>Texto (string)</td> <td>Não nulo</td> <td>País de origem do usuário</td> </tr> </tbody> </table>

- Compra

<table> <thead> <tr> <th>Campo</th> <th>Tipo de dado</th> <th>Restrições</th> <th>Descrição</th> </tr> </thead> <tbody> <tr> <td>usuario_id</td> <td>Inteiro</td> <td>Chave estrangeira, não nulo</td> <td>ID do usuário comprador (referencia <code>usuario.id</code>)</td> </tr> <tr> <td>jogo_id</td> <td>Inteiro</td> <td>Chave estrangeira, não nulo</td> <td>ID do jogo adquirido (referencia <code>jogo.id</code>)</td> </tr> <tr> <td>data_compra</td> <td>Timestamp</td> <td>Não nulo</td> <td>Data e hora em que a compra foi realizada</td> </tr> <tr> <td>preco_pago</td> <td>Decimal</td> <td>Não nulo</td> <td>Valor pago pelo jogo no momento da compra</td> </tr> <tr> <td>forma_pagamento</td> <td>Texto (string) ou ENUM</td> <td>Não nulo</td> <td>Forma de pagamento utilizada (ex: cartão, pix, boleto)</td> </tr> </tbody> </table>

- Avaliação

<table> <thead> <tr> <th>Campo</th> <th>Tipo de dado</th> <th>Restrições</th> <th>Descrição</th> </tr> </thead> <tbody> <tr> <td>usuario_id</td> <td>Inteiro</td> <td>Chave estrangeira, não nulo</td> <td>ID do usuário que avaliou (referencia <code>usuario.id</code>)</td> </tr> <tr> <td>jogo_id</td> <td>Inteiro</td> <td>Chave estrangeira, não nulo</td> <td>ID do jogo avaliado (referencia <code>jogo.id</code>)</td> </tr> <tr> <td>nota</td> <td>Inteiro</td> <td>Não nulo, de 1 a 10</td> <td>Nota atribuída ao jogo</td> </tr> <tr> <td>comentario</td> <td>Texto longo</td> <td>Opcional</td> <td>Comentário sobre o jogo</td> </tr> <tr> <td>data_avaliacao</td> <td>Timestamp</td> <td>Não nulo</td> <td>Data e hora da avaliação</td> </tr> </tbody> </table>

- Família

<table> <thead> <tr> <th>Campo</th> <th>Tipo de dado</th> <th>Restrições</th> <th>Descrição</th> </tr> </thead> <tbody> <tr> <td>id</td> <td>Inteiro</td> <td>Chave primária, não nulo, auto incremento</td> <td>Identificador único da família</td> </tr> <tr> <td>nome_familia</td> <td>Texto (string)</td> <td>Não nulo</td> <td>Nome atribuído à família</td> </tr> <tr> <td>descricao</td> <td>Texto longo</td> <td>Opcional</td> <td>Descrição ou regras do grupo familiar</td> </tr> <tr> <td>criador_id</td> <td>Inteiro</td> <td>Chave estrangeira, não nulo</td> <td>ID do usuário que criou a família (referencia <code>usuario.id</code>)</td> </tr> <tr> <td>data_criacao</td> <td>Timestamp</td> <td>Não nulo</td> <td>Data de criação da família</td> </tr> <tr> <td>publicidade</td> <td>Texto (string) ou ENUM</td> <td>Não nulo</td> <td>Nível de visibilidade da família (ex: pública, privada)</td> </tr> </tbody> </table>

# Atribuições

<table> <tr> <td align="center"><a href="https://github.com/JoseVitorNobreUFC"><img src="https://avatars.githubusercontent.com/u/62249331?v=4" width="100px;" alt="José Vitor"/><br /><sub><b>José Vitor</b></sub></a><br /><a href="https://github.com/JoseVitorNobreUFC" title="BackEnd"> </a><br/> <span>CRUD Jogo, Usuário, tarefas f2, f3, f5, f7 e documentação</span> </td> <td align="center"><a href="https://github.com/alexsonalmeida"><img src="https://avatars.githubusercontent.com/u/101877352?v=4" width="100px;" alt="Alexson Almeida"/><br /><sub><b>Alexson Almeida</b></sub></a><br /><a href="https://github.com/alexsonalmeida" title="FrontEnd"> </a><br/> <span>CRUD Compras, Avaliações, Família, tarefas f2, f4, f6, f8 e testes</span> </td> </tr> </table>
