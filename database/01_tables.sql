-- Criar os tipos ENUM manualmente
CREATE TYPE user_type AS ENUM ('customer', 'admin');
CREATE TYPE event_type AS ENUM ('wedding', 'corporate', 'debutante', 'other');
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'canceled');
CREATE TYPE product_type AS ENUM ('drink', 'structure', 'service');
CREATE TYPE payment_method AS ENUM ('credit_card', 'pix', 'boleto', 'bank_transfer');
CREATE TYPE payment_status AS ENUM ('pending', 'approved', 'rejected');

-- Tabela de Clientes (Customers)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(30),
    address TEXT,
    cpf_cnpj VARCHAR(30) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_type DEFAULT 'customer' NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela de Eventos (Events)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    event_type event_type NOT NULL,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(255) NOT NULL,
    guest_count INT NOT NULL,
    duration_hours INT NOT NULL,
    budget_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Tabela de Pedidos (Orders)
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT NOW(),
    total_amount DECIMAL(10,2) NOT NULL,
    status order_status DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Tabela de Produtos (Products)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    category product_type NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela de Itens do Pedido (Order_Items)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Tabela de Pagamentos (Payments)
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method payment_method NOT NULL,
    status payment_status DEFAULT 'pending' NOT NULL,
    payment_date TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Tabela de Notas Fiscais (Invoices)
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    issue_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    pdf_file VARCHAR(255),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Tabela de Contratos (Contracts)
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    pdf_file VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
