# Система управления производством для мебельной фабрики

**Стек:** PyQt6 + MySQL (PyMySQL)

## Возможности
* Авторизация пользователей
* Управление цехами (CRUD)
* Управление продукцией (CRUD)
* Хранение данных в MySQL

## Запуск
1. Установите зависимости

   ```bash
   pip install -r requirements.txt
   ```

2. Создайте базу `fabrik` и таблицы:

   ```sql
   -- пример схемы
   CREATE TABLE manager (
     id INT PRIMARY KEY AUTO_INCREMENT,
     login VARCHAR(50) NOT NULL UNIQUE,
     password VARCHAR(128) NOT NULL
   );

   CREATE TABLE tip_product (
     id INT PRIMARY KEY AUTO_INCREMENT,
     name_product VARCHAR(100)
   );

   CREATE TABLE material (
     id INT PRIMARY KEY AUTO_INCREMENT,
     name_material VARCHAR(100)
   );

   CREATE TABLE ceh (
     id INT PRIMARY KEY AUTO_INCREMENT,
     name_ceh VARCHAR(100),
     chelovek INT,
     vremya INT
   );

   CREATE TABLE product (
     id INT PRIMARY KEY AUTO_INCREMENT,
     name VARCHAR(100),
     tip_product INT,
     articul VARCHAR(50),
     min_cena DECIMAL(10,2),
     tip_material INT,
     ceh_id INT,
     FOREIGN KEY (tip_product) REFERENCES tip_product(id),
     FOREIGN KEY (tip_material) REFERENCES material(id),
     FOREIGN KEY (ceh_id) REFERENCES ceh(id)
   );
   ```

3. Запустите приложение

   ```bash
   python main.py
   ```

## Сборка EXE
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
