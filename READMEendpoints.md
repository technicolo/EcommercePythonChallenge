# 📘 API - E-commerce Backend

Esta es la documentación de los endpoints principales de la API desarrollada en FastAPI.

---

## 🔐 Autenticación

- `POST /auth/login`: Inicia sesión con email y contraseña.
- `POST /auth/register`: registrate para luego ingresar.


---

## 👤 Usuarios

- `GET /usuarios`: Listar todos los usuarios.
- `GET /usuarios/{usuario_id}`: Obtener un usuario por su ID.
- `PUT /usuarios/{usuario_id}`: Actualizar los datos de un usuario.
- `DELETE /usuarios/{usuario_id}`: Eliminar un usuario por ID.
- `GET /usuarios/{usuario_id}/pedidos`: Listar todos los pedidos con detalles de un usuario.

---

## 📦 Productos

- `GET /productos`: Listar productos con paginación (`offset`, `limit`).
- `GET /productos/{producto_id}`: Obtener un producto por ID.
- `POST /productos`: Crear un nuevo producto.
- `PUT /productos/{producto_id}`: Actualizar un producto por ID.
- `DELETE /productos/{producto_id}`: Eliminar un producto por ID.

### 🔁 Lotes y CSV

- `POST /productos/lote`: Crear productos en lote.
- `PUT /productos/actualizar-lote`: Actualizar productos en lote.
- `DELETE /productos/lote`: Eliminar productos en lote (IDs en body).
- `POST /productos/importar-csv`: Importar productos desde un archivo CSV.

---

## 🧾 Pedidos

- `GET /pedidos`: Listar todos los pedidos (con filtros opcionales por fecha).
- `GET /pedidos/{pedido_id}`: Obtener un pedido con sus detalles.
- `POST /pedidos`: Crear un nuevo pedido.
- `PUT /pedidos/{pedido_id}`: Actualizar un pedido.
- `DELETE /pedidos/{pedido_id}`: Eliminar un pedido.

### 💳 Pago

- `POST /pedidos/{pedido_id}/pagar`: Marcar un pedido como pagado y calcular su total.

---

## 📋 Detalles de Pedido

- `GET /detalles`: Listar todos los detalles de pedido.
- `GET /detalles/{detalle_id}`: Obtener un detalle por ID.
- `POST /detalles`: Crear un nuevo detalle de pedido (producto en pedido).
- `PUT /detalles/{detalle_id}`: Actualizar un detalle (actualiza también el total del pedido).
- `DELETE /detalles/{detalle_id}`: Eliminar un detalle (no recalcula total automáticamente).

---

## ⚙️ Sistema

- `GET /health`: Verifica que la API está corriendo.
- `GET /version`: Devuelve la versión actual de la API.

---

### 📝 Notas

- La API utiliza JWT para autenticación (bearer token).
- Para probar los endpoints interactivos, acceder a: [http://localhost:8000/docs](http://localhost:8000/docs)
