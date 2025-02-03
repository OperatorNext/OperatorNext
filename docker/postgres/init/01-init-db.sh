#!/bin/bash
set -e

# 函数：创建用户（如果不存在）
create_user() {
    local user=$1
    local password=$2
    echo "Creating user $user..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        DO \$\$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$user') THEN
                CREATE USER $user WITH PASSWORD '$password';
            END IF;
        END
        \$\$;
EOSQL
}

# 函数：创建数据库（如果不存在）
create_database() {
    local dbname=$1
    local owner=$2
    echo "Creating database $dbname..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        SELECT 'CREATE DATABASE $dbname OWNER $owner'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$dbname')\gexec
EOSQL
}

# 函数：设置数据库权限
set_permissions() {
    local dbname=$1
    local user=$2
    echo "Setting permissions for $user on $dbname..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        GRANT ALL PRIVILEGES ON DATABASE $dbname TO $user;
EOSQL
}

# 主逻辑
main() {
    local prod_user="${PROD_USER:-operatornext_prod_user}"
    local prod_password="${PROD_PASSWORD:-op3r8t0r_n3xt_2024_pG_s3cur3}"
    local prod_db="${PROD_DB:-operatornext_production}"

    # 创建生产环境用户和数据库
    create_user "$prod_user" "$prod_password"
    create_database "$prod_db" "$prod_user"
    set_permissions "$prod_db" "$prod_user"

    echo "Database initialization completed successfully!"
}

# 执行主逻辑
main 