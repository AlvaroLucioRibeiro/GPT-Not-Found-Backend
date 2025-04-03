-- Inserir Clientes
INSERT INTO customers (id, full_name, email, phone, address, cpf_cnpj, password_hash, role)
VALUES 
(1001, 'Ana Souza', 'ana@example.com', '11999999991', 'Rua das Flores, 123', '12345678901', 'hash1', 'customer'),
(1002, 'Carlos Lima', 'carlos@example.com', '11999999992', 'Av. Paulista, 456', '12345678902', 'hash2', 'customer'),
(1003, 'Julia Mendes', 'julia@example.com', '11999999993', 'Rua Azul, 789', '12345678903', 'hash3', 'customer'),
(1004, 'Marcos Silva', 'marcos@example.com', '11999999994', 'Rua Verde, 321', '12345678904', 'hash4', 'admin'),
(1005, 'Fernanda Torres', 'fernanda@example.com', '11999999995', 'Av. Brasil, 654', '12345678905', 'hash5', 'customer');

-- Inserir Eventos
INSERT INTO events (id, customer_id, event_type, event_date, location, guest_count, duration_hours)
VALUES 
(2001, 1001, 'wedding', '2025-06-10 18:00:00', 'Espaço Verde', 200, 6),
(2002, 1002, 'corporate', '2025-07-15 20:00:00', 'Centro de Convenções', 300, 4),
(2003, 1003, 'debutante', '2025-08-01 21:00:00', 'Salão Real', 150, 5),
(2004, 1004, 'other', '2025-09-22 19:00:00', 'Chácara Bela Vista', 100, 3),
(2005, 1005, 'wedding', '2025-10-10 17:00:00', 'Sítio Paraíso', 250, 7);

-- Inserir Pedidos
INSERT INTO orders (id, event_id, total_amount, status)
VALUES 
(3001, 2001, 5000.00, 'paid'),
(3002, 2002, 3500.00, 'pending'),
(3003, 2003, 4200.00, 'paid'),
(3004, 2004, 2800.00, 'canceled'),
(3005, 2005, 7000.00, 'pending');

-- Inserir Produtos
INSERT INTO products (id, name, description, base_price, category)
VALUES 
(4001, 'Moscow Mule', 'Vodka com gengibre e espuma artesanal', 25.00, 'drink'),
(4002, 'Bar de Gin', 'Estrutura e especiarias para gin', 1000.00, 'structure'),
(4003, 'Bartender', 'Profissional para preparação de drinks', 500.00, 'service'),
(4004, 'Pina Descolada', 'Drink não alcoólico com leite de coco', 20.00, 'drink'),
(4005, 'Carrinho de Carajillo', 'Serviço com licor e café', 800.00, 'structure');

-- Inserir Itens do Pedido
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price, total_price)
VALUES 
(5001, 3001, 4001, 100, 25.00, 2500.00),
(5002, 3002, 4002, 1, 1000.00, 1000.00),
(5003, 3003, 4003, 4, 500.00, 2000.00),
(5004, 3004, 4004, 50, 20.00, 1000.00),
(5005, 3005, 4005, 2, 800.00, 1600.00);

-- Inserir Pagamentos
INSERT INTO payments (id, order_id, amount, payment_method, status, payment_date)
VALUES 
(6001, 3001, 5000.00, 'pix', 'approved', '2025-06-05 12:00:00'),
(6002, 3002, 3500.00, 'credit_card', 'pending', NULL),
(6003, 3003, 4200.00, 'boleto', 'approved', '2025-07-25 15:30:00'),
(6004, 3004, 2800.00, 'pix', 'rejected', '2025-08-10 10:00:00'),
(6005, 3005, 7000.00, 'bank_transfer', 'pending', NULL);

-- Inserir Notas Fiscais
INSERT INTO invoices (id, order_id, invoice_number, issue_date, total_amount, pdf_file)
VALUES 
(7001, 3001, 'NF-001', '2025-06-06 09:00:00', 5000.00, 'nf_001.pdf'),
(7002, 3002, 'NF-002', '2025-07-16 09:00:00', 3500.00, 'nf_002.pdf'),
(7003, 3003, 'NF-003', '2025-08-02 09:00:00', 4200.00, 'nf_003.pdf'),
(7004, 3004, 'NF-004', '2025-09-23 09:00:00', 2800.00, 'nf_004.pdf'),
(7005, 3005, 'NF-005', '2025-10-11 09:00:00', 7000.00, 'nf_005.pdf');

-- Inserir Contratos
INSERT INTO contracts (id, event_id, pdf_file)
VALUES 
(8001, 2001, 'contrato_001.pdf'),
(8002, 2002, 'contrato_002.pdf'),
(8003, 2003, 'contrato_003.pdf'),
(8004, 2004, 'contrato_004.pdf'),
(8005, 2005, 'contrato_005.pdf');

