-- Create model Categoria
--
CREATE TABLE "orders_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "categorias" varchar(30) NOT 
NULL);
--
-- Create model DetallePedido
--
CREATE TABLE "orders_detallepedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "descripcion" varchar(50) NOT NULL, "cantidadPlatillos" integer NOT NULL, "precioPlatillos" real NOT NULL);
--
-- Create model Extra
--
CREATE TABLE "orders_extra" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(20) NOT NULL);  
--
-- Create model Pedido
--
CREATE TABLE "orders_pedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total" real NOT NULL, "fecha" datetime NOT NULL, "estado" bool NOT NULL, "cliente_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Platillo
--
CREATE TABLE "orders_platillo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(40) NOT NULL, "maxExtras" integer NOT NULL, "precio" real NOT NULL, "imagen" varchar(100) NULL, "categoria_id" integer NOT NULL REFERENCES "orders_categoria" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field extras to detallepedido
--
CREATE TABLE "orders_detallepedido_extras" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "detallepedido_id" integer NOT NULL REFERENCES "orders_detallepedido" ("id") DEFERRABLE INITIALLY DEFERRED, "extra_id" integer NOT NULL REFERENCES "orders_extra" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field pedido to detallepedido
--
ALTER TABLE "orders_detallepedido__old" RENAME TO "orders_detallepedido";
CREATE TABLE "orders_detallepedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "descripcion" varchar(50) NOT NULL, "cantidadPlatillos" integer NOT NULL, "precioPlatillos" real NOT NULL, "pedido_id" integer NOT NULL 
REFERENCES "orders_pedido" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "orders_detallepedido" ("id", "descripcion", "cantidadPlatillos", "precioPlatillos", "pedido_id") SELECT "id", "descripcion", "cantidadPlatillos", "precioPlatillos", NULL FROM "orders_detallepedido__old";      
DROP TABLE "orders_detallepedido__old";
CREATE INDEX "orders_pedido_cliente_id_aadcde6c" ON "orders_pedido" ("cliente_id");
CREATE INDEX "orders_platillo_categoria_id_f5ff970d" ON "orders_platillo" ("categoria_id");
CREATE UNIQUE INDEX orders_detallepedido_extras_detallepedido_id_extra_id_fff10c68_uniq ON "orders_detallepedido_extras" ("detallepedido_id", "extra_id");
CREATE INDEX "orders_detallepedido_extras_detallepedido_id_109a0f4a" ON "orders_detallepedido_extras" ("detallepedido_id");
CREATE INDEX "orders_detallepedido_extras_extra_id_49105b09" ON "orders_detallepedido_extras" ("extra_id");    
CREATE INDEX "orders_detallepedido_pedido_id_64edb50c" ON "orders_detallepedido" ("pedido_id");
--
-- Add field platillo to detallepedido
--
ALTER TABLE "orders_detallepedido" RENAME TO "orders_detallepedido__old";
CREATE TABLE "orders_detallepedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "descripcion" varchar(50) NOT NULL, "cantidadPlatillos" integer NOT NULL, "precioPlatillos" real NOT NULL, "pedido_id" integer NOT NULL 
REFERENCES "orders_pedido" ("id") DEFERRABLE INITIALLY DEFERRED, "platillo_id" integer NOT NULL REFERENCES "orders_platillo" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "orders_detallepedido" ("id", "descripcion", "cantidadPlatillos", "precioPlatillos", "pedido_id", "platillo_id") SELECT "id", "descripcion", "cantidadPlatillos", "precioPlatillos", "pedido_id", NULL FROM "orders_detallepedido__old";
DROP TABLE "orders_detallepedido__old";
CREATE INDEX "orders_detallepedido_pedido_id_64edb50c" ON "orders_detallepedido" ("pedido_id");
CREATE INDEX "orders_detallepedido_platillo_id_3c029398" ON "orders_detallepedido" ("platillo_id");
COMMIT;

drop table orders_pedido;
drop table orders_detallepedido_extras;
drop table orders_detallepedido;