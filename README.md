### Дискреционная модель доступа
Платформа для проведения CTF-соревнований.

Вначале окно - Выберите пользователя - Введите пароль
Затем показываются файлы.

Информация о пользователях и об объектах должна храниться в базе данных.
```bash
brew install postgresql
pip3 install flask
pip3 install psycopg2-binary
```

```bash
docker run --name db_ctf -p 5432:5432    -e POSTGRES_USER=ctf   -e POSTGRES_PASSWORD=ctf  -e POSTGRES_DB=db_ctf    -e PGDATA=/var/lib/postgresql/data/pgdata    -d -v "$(pwd)/postgres_data":/var/lib/postgresql/data postgres
```

```postgres
-- Create sequence for user ID
CREATE SEQUENCE IF NOT EXISTS userid_seq START WITH 1;

-- Create users table
CREATE TABLE users (
    userid INT PRIMARY KEY DEFAULT nextval('userid_seq'),
    "user" VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL
);

-- Create sequence for category ID
CREATE SEQUENCE IF NOT EXISTS categoryid_seq START WITH 1;

-- Create categories table
CREATE TABLE categories (
    category_id INT PRIMARY KEY DEFAULT nextval('categoryid_seq'),
    category VARCHAR NOT NULL
);

-- Create sequence for task ID
CREATE SEQUENCE IF NOT EXISTS taskid_seq START WITH 1;

-- Create tasks table
CREATE TABLE tasks (
    task_id INT PRIMARY KEY DEFAULT nextval('taskid_seq'),
    task_name TEXT NOT NULL,
    content TEXT NOT NULL,
    directory VARCHAR
);

-- Create task_categories table (many-to-many relationship)
CREATE TABLE task_categories (
    task_id INT REFERENCES tasks(task_id),
    category_id INT REFERENCES categories(category_id),
    PRIMARY KEY (task_id, category_id)
);

-- Create user_tasks table (many-to-many relationship)
CREATE TABLE user_tasks (
    user_id INT REFERENCES users(userid),
    task_id INT REFERENCES tasks(task_id),
    rights INT NOT NULL,
    PRIMARY KEY (user_id, task_id)
);
```

4) Матрица доступа

Первый пользователь - Администратор
Второй пользователь - Разработчик тасков
Третий пользователь - Разработчик тасков 2
Четвертый пользователь - Участник соревнования
Пятый пользователь - Веб-дизайнер
0b1 - Read
0b10 - Write
0b100 - Execute
0b1000 - Tag and Grant
0b10000 - Own
5 - RX
15 - RWXT
31 - RWXTO

|       | admin | dev1 | dev2 | participant | designer |
| ----- | ----- | ---- | ---- | ----------- | -------- |
| task1 | 15    | 31   | 5    | 5           | 0        |
| task2 | 15    | 31   | 5    | 5           | 0        |
| task3 | 15    | 5    | 31   | 5           | 0        |
| task4 | 15    | 5    | 31   | 5           | 0        |
| task5 | 15    | 5    | 31   | 5           | 0        |
| test1 | 31    | 0    | 0    | 0           | 1        |
| test2 | 31    | 0    | 0    | 0           | 1        |
| test3 | 31    | 0    | 0    | 0           | 1        |
| test4 | 31    | 0    | 0    | 0           | 1        |
| test5 | 31    | 0    | 0    | 0           | 1        |
