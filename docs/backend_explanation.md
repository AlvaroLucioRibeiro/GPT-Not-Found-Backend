# 📌 Proposta para Backend - Elo Drinks

## 📖 Visão Geral
Este documento detalha a estrutura do banco de dados, os relacionamentos entre as tabelas e as rotas da API para a aplicação da **Elo Drinks**. O objetivo é criar um sistema eficiente para gerenciar eventos, pedidos, clientes, pagamentos e documentos fiscais.

---

## 📊 Estrutura do Banco de Dados

Abaixo está a estrutura completa das tabelas e seus relacionamentos.

### **1. Clientes (`clientes`)**
Guarda informações dos clientes e administradores.

| Campo          | Tipo              | Descrição |
|---------------|------------------|-----------|
| `id`         | INT (PK) AUTO_INCREMENT | Identificador único do cliente |
| `nome`       | VARCHAR(255) | Nome completo do cliente |
| `email`      | VARCHAR(255) UNIQUE | E-mail do cliente (usado para login) |
| `telefone`   | VARCHAR(20) | Telefone de contato |
| `endereco`   | TEXT | Endereço completo |
| `cpf_cnpj`   | VARCHAR(20) UNIQUE | Documento do cliente |
| `senha_hash` | VARCHAR(255) | Senha criptografada (usando bcrypt) |
| `tipo`       | ENUM('cliente', 'admin') DEFAULT 'cliente' | Indica se o usuário é cliente ou administrador |

📌 **Relacionamento:**  
- *1:N* → **Eventos (`eventos`)** → Um cliente pode criar vários eventos.  
- *1:N* → **Pedidos (`pedidos`)** → Um cliente pode ter vários pedidos.

---

### **2. Eventos (`eventos`)**
Representa os eventos organizados pelos clientes.

| Campo            | Tipo        | Descrição |
|-----------------|------------|-----------|
| `id`           | INT (PK) AUTO_INCREMENT | Identificador do evento |
| `cliente_id`   | INT (FK → clientes.id) | Cliente que criou o evento |
| `tipo_evento`  | ENUM('casamento', 'corporativo', 'debutante', 'outro') | Tipo do evento |
| `data`         | DATETIME | Data do evento |
| `local`        | VARCHAR(255) | Localização do evento |
| `numero_convidados` | INT | Número de convidados |
| `duracao_horas` | INT | Tempo de duração do evento |
| `orcamento_aprovado` | BOOLEAN | Indica se o orçamento foi aprovado |

📌 **Relacionamento:**  
- *1:N* → **Pedidos (`pedidos`)** → Um evento pode ter vários pedidos.  
- *1:1* → **Contratos (`contratos`)** → Cada evento pode ter um contrato associado.

---

### **3. Pedidos (`pedidos`)**
Representa os pedidos de serviços e produtos para um evento.

| Campo         | Tipo         | Descrição |
|--------------|-------------|-----------|
| `id`        | INT (PK) AUTO_INCREMENT | Identificador do pedido |
| `evento_id` | INT (FK → eventos.id) | Evento relacionado ao pedido |
| `data_pedido` | DATETIME | Data do pedido |
| `valor_total` | DECIMAL(10,2) | Valor total do pedido |
| `status` | ENUM('pendente', 'pago', 'cancelado') | Status do pedido |

📌 **Relacionamento:**  
- *1:N* → **Itens do Pedido (`itens_pedido`)** → Um pedido pode conter vários produtos.  
- *1:1* → **Pagamentos (`pagamentos`)** → Cada pedido tem um pagamento.  
- *1:1* → **Nota Fiscal (`notas_fiscais`)** → Cada pedido gera uma nota fiscal.

---

### **4. Itens do Pedido (`itens_pedido`)**
Produtos e serviços adicionados a um pedido.

| Campo        | Tipo         | Descrição |
|-------------|-------------|-----------|
| `id`       | INT (PK) AUTO_INCREMENT | Identificador único do item |
| `pedido_id` | INT (FK → pedidos.id) | Pedido ao qual o item pertence |
| `produto_id` | INT (FK → produtos.id) | Produto referenciado |
| `quantidade` | INT | Quantidade do produto solicitado |
| `preco_unitario` | DECIMAL(10,2) | Preço por unidade |
| `total` | DECIMAL(10,2) | Preço total do item |

📌 **Relacionamento:**  
- *N:M* → **Produtos (`produtos`)** → Um produto pode estar em vários pedidos.

---

### **5. Produtos (`produtos`)**
Bebidas, serviços e itens disponíveis para venda.

| Campo       | Tipo        | Descrição |
|------------|------------|-----------|
| `id`      | INT (PK) AUTO_INCREMENT | Identificador do produto |
| `nome`    | VARCHAR(255) | Nome do produto |
| `descricao` | TEXT | Descrição do produto |
| `preco_base` | DECIMAL(10,2) | Preço base do produto |
| `tipo` | ENUM('bebida', 'estrutura', 'serviço') | Tipo do item |
| `ativo` | BOOLEAN | Indica se está disponível para compra |

📌 **Relacionamento:**  
- *N:M* → **Pedidos (`itens_pedido`)** → Um produto pode estar em vários pedidos.


### **6. Pagamentos (`pagamentos`)**
Registra pagamentos de pedidos.

| Campo         | Tipo        | Descrição |
|--------------|------------|-----------|
| `id`        | INT (PK) AUTO_INCREMENT | Identificador do pagamento |
| `pedido_id` | INT (FK → pedidos.id) | Pedido pago |
| `valor`     | DECIMAL(10,2) | Valor pago |
| `metodo_pagamento` | ENUM('cartao_credito', 'pix', 'boleto', 'transferencia') | Método de pagamento |
| `status` | ENUM('pendente', 'aprovado', 'rejeitado') | Status do pagamento |
| `data_pagamento` | DATETIME | Data do pagamento |

---

### **7. Notas Fiscais (`notas_fiscais`)**
Armazena as notas fiscais dos pedidos.

| Campo         | Tipo        | Descrição |
|--------------|------------|-----------|
| `id`        | INT (PK) AUTO_INCREMENT | Identificador da nota fiscal |
| `pedido_id` | INT (FK → pedidos.id) | Pedido relacionado |
| `numero_nota` | VARCHAR(50) UNIQUE | Número da nota fiscal |
| `data_emissao` | DATETIME | Data de emissão |
| `valor_total` | DECIMAL(10,2) | Valor total da nota fiscal |
| `arquivo_pdf` | VARCHAR(255) | Caminho do arquivo PDF |

---

### **8. Contratos (`contratos`)**
Contrato gerado para proteção da empresa e do cliente.

| Campo         | Tipo        | Descrição |
|--------------|------------|-----------|
| `id`        | INT (PK) AUTO_INCREMENT | Identificador do contrato |
| `evento_id` | INT (FK → eventos.id) | Evento relacionado |
| `data_criacao` | DATETIME | Data de criação |
| `arquivo_pdf` | VARCHAR(255) | Caminho do arquivo PDF |

---

## 🔹 Rotas da API

### **🔹 Autenticação**
- `POST /auth/register` → Registro de cliente
- `POST /auth/login` → Login (gera JWT Token)
- `GET /clientes/me` → Retorna dados do usuário logado

### **🔹 Clientes**
- `GET /clientes`
- `GET /clientes/{id}`
- `PUT /clientes/{id}`
- `DELETE /clientes/{id}`

### **🔹 Eventos**
- `GET /eventos`
- `POST /eventos`
- `GET /eventos/{id}`
- `PUT /eventos/{id}`
- `DELETE /eventos/{id}`

### **🔹 Pedidos**
- `GET /pedidos`
- `POST /pedidos`
- `GET /pedidos/{id}`
- `PUT /pedidos/{id}`
- `DELETE /pedidos/{id}`

### **🔹 Produtos**
- `GET /produtos`
- `POST /produtos`
- `GET /produtos/{id}`
- `PUT /produtos/{id}`
- `DELETE /produtos/{id}`

### **🔹 Pagamentos**
- `POST /pagamentos`
- `GET /pagamentos/{id}`
- `PUT /pagamentos/{id}`

### **🔹 Notas Fiscais**
- `GET /notas-fiscais/{pedido_id}`
- `GET /notas-fiscais/download/{nota_id}`

### **🔹 Contratos**
- `GET /contratos/{evento_id}`
- `GET /contratos/download/{contrato_id}`

---