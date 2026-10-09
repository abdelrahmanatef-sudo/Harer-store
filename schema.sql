-- =============================================
-- حرير Store — Supabase Schema
-- =============================================

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- -----------------------------------------------
-- CATEGORIES
-- -----------------------------------------------
create table if not exists categories (
  id   serial primary key,
  slug text unique not null,
  name text not null,
  icon text
);

insert into categories (slug, name, icon) values
  ('charger',  'شواحن',        '🔌'),
  ('cable',    'كابلات',       '🔗'),
  ('earbuds',  'سماعات',       '🎧'),
  ('case',     'أكفار',        '📱'),
  ('powerbank','باور بانك',    '🔋')
on conflict (slug) do nothing;

-- -----------------------------------------------
-- PRODUCTS
-- -----------------------------------------------
create table if not exists products (
  id          uuid primary key default uuid_generate_v4(),
  name        text not null,
  description text,
  price       numeric(10,2) not null,
  old_price   numeric(10,2),
  image_url   text,
  category_id int references categories(id),
  brand       text,            -- Anker / Apple / Samsung / ThreeTech
  stock       int default 0,
  is_featured boolean default false,
  created_at  timestamptz default now()
);

-- Sample products
insert into products (name, description, price, old_price, image_url, category_id, brand, stock, is_featured)
values
  ('شاحن Anker 20W', 'شاحن سريع USB-C 20 واط أصلي من Anker', 299, 350,
   'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400',
   (select id from categories where slug='charger'), 'Anker', 50, true),

  ('كابل Apple Lightning أصلي', 'كابل Lightning MFi معتمد من Apple — 1 متر', 199, 250,
   'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400',
   (select id from categories where slug='cable'), 'Apple', 80, true),

  ('شاحن Samsung 25W', 'شاحن سريع Samsung Super Fast Charging', 349, 400,
   'https://images.unsplash.com/photo-1585338107379-7b5c4ab65a32?w=400',
   (select id from categories where slug='charger'), 'Samsung', 40, false),

  ('كابل USB-C ThreeTech', 'كابل شحن سريع 3A — 1.5 متر', 89, 120,
   'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
   (select id from categories where slug='cable'), 'ThreeTech', 120, false),

  ('Anker Soundcore A20i', 'سماعة لاسلكية بصوت نقي وعزل ضوضاء', 599, 699,
   'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400',
   (select id from categories where slug='earbuds'), 'Anker', 30, true),

  ('كفر iPhone 15 Pro شفاف', 'حماية كاملة مع ظهر شفاف', 79, null,
   'https://images.unsplash.com/photo-1601972599720-36938d4ecd31?w=400',
   (select id from categories where slug='case'), 'ThreeTech', 200, false),

  ('Anker PowerCore 10000', 'باور بانك 10000 mAh شحن سريع', 499, 599,
   'https://images.unsplash.com/photo-1609592806596-b186e8d58310?w=400',
   (select id from categories where slug='powerbank'), 'Anker', 25, true),

  ('شاحن Apple 20W أصلي', 'شاحن USB-C أصلي من Apple', 399, 450,
   'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400',
   (select id from categories where slug='charger'), 'Apple', 60, false);

-- -----------------------------------------------
-- ORDERS
-- -----------------------------------------------
create table if not exists orders (
  id           uuid primary key default uuid_generate_v4(),
  order_number text unique not null default 'ORD-' || extract(epoch from now())::bigint,
  customer_name text not null,
  customer_phone text not null,
  customer_city  text,
  customer_address text,
  notes        text,
  total        numeric(10,2) not null,
  status       text default 'pending'
                check (status in ('pending','confirmed','shipped','delivered','cancelled')),
  source       text default 'website',  -- website / whatsapp / facebook / instagram
  created_at   timestamptz default now()
);

-- -----------------------------------------------
-- ORDER ITEMS
-- -----------------------------------------------
create table if not exists order_items (
  id         serial primary key,
  order_id   uuid references orders(id) on delete cascade,
  product_id uuid references products(id),
  name       text not null,
  price      numeric(10,2) not null,
  qty        int not null default 1
);

-- -----------------------------------------------
-- NEWSLETTER
-- -----------------------------------------------
create table if not exists newsletter (
  id         serial primary key,
  email      text unique not null,
  subscribed_at timestamptz default now()
);

-- -----------------------------------------------
-- ROW LEVEL SECURITY
-- -----------------------------------------------
alter table products   enable row level security;
alter table categories enable row level security;
alter table orders     enable row level security;
alter table order_items enable row level security;
alter table newsletter  enable row level security;

-- Public can READ products and categories
create policy "public read products"    on products    for select using (true);
create policy "public read categories"  on categories  for select using (true);

-- Anyone can INSERT orders (guest checkout)
create policy "public insert orders"      on orders      for insert with check (true);
create policy "public insert order_items" on order_items for insert with check (true);
create policy "public insert newsletter"  on newsletter  for insert with check (true);

-- Only authenticated users (admin) can manage everything
create policy "admin all products"    on products    for all using (auth.role() = 'authenticated');
create policy "admin all orders"      on orders      for all using (auth.role() = 'authenticated');
create policy "admin all order_items" on order_items for select using (auth.role() = 'authenticated');

-- -----------------------------------------------
-- HELPER: auto-generate readable order number
-- -----------------------------------------------
create or replace function set_order_number()
returns trigger language plpgsql as $$
begin
  new.order_number := 'HAR-' || to_char(now(), 'YYYYMMDD') || '-' ||
                      lpad((nextval('order_seq'))::text, 4, '0');
  return new;
end;
$$;

create sequence if not exists order_seq start 1;

create trigger trg_order_number
  before insert on orders
  for each row execute function set_order_number();
