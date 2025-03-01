-- Criar os tipos ENUM manualmente antes de usá-los
CREATE TYPE tipo_usuario AS ENUM ('cliente', 'admin');
CREATE TYPE tipo_evento AS ENUM ('casamento', 'corporativo', 'debutante', 'outro');
CREATE TYPE status_pedido AS ENUM ('pendente', 'pago', 'cancelado');
CREATE TYPE tipo_produto AS ENUM ('bebida', 'estrutura', 'serviço');
CREATE TYPE metodo_pagamento AS ENUM ('cartao_credito', 'pix', 'boleto', 'transferencia');
CREATE TYPE status_pagamento AS ENUM ('pendente', 'aprovado', 'rejeitado');

-- Tabela de Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    endereco TEXT,
    cpf_cnpj VARCHAR(20) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    tipo tipo_usuario DEFAULT 'cliente' NOT NULL
);

-- Tabela de Eventos
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo tipo_evento NOT NULL,
    data TIMESTAMP NOT NULL,
    local VARCHAR(255) NOT NULL,
    numero_convidados INT NOT NULL,
    duracao_horas INT NOT NULL,
    orcamento_aprovado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Tabela de Pedidos
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    evento_id INT NOT NULL,
    data_pedido TIMESTAMP NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    status status_pedido DEFAULT 'pendente' NOT NULL,
    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco_base DECIMAL(10,2) NOT NULL,
    tipo tipo_produto NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

-- Tabela de Itens do Pedido
CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

-- Tabela de Pagamentos
CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    metodo_pagamento metodo_pagamento NOT NULL,
    status status_pagamento DEFAULT 'pendente' NOT NULL,
    data_pagamento TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
);

-- Tabela de Notas Fiscais
CREATE TABLE notas_fiscais (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    numero_nota VARCHAR(50) UNIQUE NOT NULL,
    data_emissao TIMESTAMP NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    arquivo_pdf VARCHAR(255),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
);

-- Tabela de Contratos
CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    evento_id INT NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    arquivo_pdf VARCHAR(255),
    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
);
