
-- -------------------------------------------------
--  Тестовые данные для БД проекта "fabrik"
-- -------------------------------------------------

-- Менеджеры
INSERT INTO manager (login, password) VALUES
  ('admin',   'admin123'),
  ('manager', 'manager123'),
  ('guest',   'guest123');

-- Типы продуктов
INSERT INTO tip_product (name_product) VALUES
  ('Шкаф'),
  ('Кресло'),
  ('Стол');

-- Материалы
INSERT INTO material (name_material) VALUES
  ('Дуб'),
  ('Берёза'),
  ('Металл');

-- Цеха
INSERT INTO ceh (name_ceh, chelovek, vremya) VALUES
  ('Столярный', 25, 120),
  ('Сборочный', 15,  60),
  ('Покрасочный', 10, 45);

-- Продукты
INSERT INTO product (name, tip_product, articul, min_cena, tip_material, ceh_id) VALUES
  ('Шкаф‑купе',             1, 'SHK001', 15000, 1, 1),
  ('Кресло офисное',        2, 'KRS001',  5000, 3, 2),
  ('Стол письменный',       3, 'STL001',  8000, 2, 1),
  ('Тумбочка прикроватная', 1, 'TMB001',  3000, 2, 2),
  ('Полка настенная',       1, 'PLK001',  1200, 2, 3);
