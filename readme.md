erDiagram
    USUARIO ||--o{ PEDIDO : tiene
    PEDIDO ||--o{ DETALLE_PEDIDO : contiene
    PRODUCTO ||--o{ DETALLE_PEDIDO : referencia

    USUARIO {
        int id PK
        string nombre
        string email
    }

    PEDIDO {
        int id PK
        datetime fecha
        float total
        int usuario_id FK
    }

    DETALLE_PEDIDO {
        int id PK
        int pedido_id FK
        int producto_id FK
        int cantidad
        float precio_unitario
    }

    PRODUCTO {
        int id PK
        string nombre
        float precio
        int stock
    }

## Diagrama de Secuencia – Integración con Servicio de Facturación

Este diagrama muestra cómo la aplicación interactuaría con un sistema externo para generar una factura automáticamente tras la creación de un pedido.

```mermaid
sequenceDiagram
    participant Cliente
    participant API
    participant DB
    participant ServicioFacturacion

    Cliente->>API: POST /pedidos
    API->>DB: Validar usuario y guardar pedido
    DB-->>API: Pedido creado
    API->>ServicioFacturacion: POST /facturar {pedido_id, total}
    ServicioFacturacion-->>API: 200 OK
    API-->>Cliente: Pedido creado exitosamente

## Contexto funcional

Esta API simula el backend de un sistema de e-commerce básico. Permite registrar productos, usuarios y pedidos, calculando automáticamente el total de los pedidos en base a sus productos asociados. Está diseñada con arquitectura por capas y preparada para escalar.

## Cómo usar el servicio

1. Crear un usuario vía `/auth/register`.
2. Crear productos vía `/productos/importar-csv O /productos/lote O productos/productos`.
3. Crear un pedido nuevo vía `/pedidos/v1/pedidos`.
4. Asociar productos a un pedido vía `/detalles-pedido/detalles `.
5. Consultar pedidos api/v1/pedidos/{pedido_id} y pagar por ellos en api/v1/pedidos/{pedido_id}/pagar.

## Dataset incluido

El archivo `app/seed.py` se ejecuta manualmente con: python seed_from_json.py y si hay algun problema simepre pueden usar el database cleaner: python database_cleaner.py el cual se encarga de la limpieza de datos ya sea por mal ingreso de estos o guardado de tipo de datos invalidos .

##Contexto funcional
Esta API simula el backend de un sistema de e-commerce básico. Permite registrar productos, usuarios y pedidos, calculando automáticamente el total de los pedidos en base a los productos asociados. Está diseñada con arquitectura por capas y preparada para escalar horizontalmente.

## 🔁 Diagrama de Secuencia – Simulación de Integración con Servicio de Facturación

Este diagrama muestra cómo la aplicación podría integrarse con un sistema externo para emitir una factura tras la creación de un pedido. En esta versión, simplemente se simula el cambio de estado del pedido a “Pagado” sin realizar la facturación real, lo cual es común en entornos donde la facturación se gestiona desde otro sistema.

```mermaid
sequenceDiagram
    participant Usuario
    participant API
    participant DB
    participant ServicioFacturacion

    Usuario->>API: POST /pedidos
    API->>DB: Validar usuario y guardar pedido
    DB-->>API: Pedido creado
    API->>ServicioFacturacion: POST /facturar {pedido_id, total}
    ServicioFacturacion-->>API: 200 OK
    API-->>Usuario: Pedido creado exitosamente

## Features Opcionales Implementados

Se detallan a continuación los features opcionales implementados y su ubicación o comportamiento dentro del sistema:

1. CRUD para entidades individuales y en lote (JSON/CSV): Implementado en productos, pedidos y detalles. El lote puede verse en las rutas de productos (`/productos/lote`, `/productos/importar-csv`).

2. Lock de dependencias mediante `pyproject.toml` y `poetry.lock`.

3. Logging implementado en el endpoint `GET /api/v1/pedidos` y `/api/v2/pedidos`, usando `logger.info()` para trazabilidad con `correlation_id`.

4. Manejo de errores con Problem Details (RFC 9457), centralizado en `utils/ProblemDetailsException.py`.

5. Middleware que agrega un UUID único (`X-Correlation-ID`) a cada request. Implementado en `middleware/correlation_id.py`.

6. Procesamiento de archivos CSV para la carga masiva de productos. Ruta: `POST /productos/importar-csv`.

7a. Paginación en `GET /productos`, usando parámetros `offset` y `limit`.

8a. Tests unitarios con Pytest. Incluye uso de fixtures, mocks y pruebas en archivos como `test/test_pedidos.py`.

9. Dependency Injection aplicada en toda la app: `Session`, servicios y usuarios se inyectan vía `Depends`.

11. Inversión de control aplicada al inyectar dependencias y abstraer lógica de servicios.

12. Separación de entidades de dominio vs entidades de base de datos, en línea con DDD. Ver carpetas `domain/` y `models/`.

13. Pre-commits automáticos configurados con `Ruff` en `.pre-commit-config.yaml`.

16. Filtro por fecha implementado en el endpoint `GET /api/v1/pedidos` y `GET /api/v2/pedidos`.

18. Caching aplicado en la operación `actualizar_total_pedido()` dentro del `pedido_service`mas precisamente en el `/api/v2/pedidos/{pedido_id}/pagar`, usada al crear o pagar un pedido.

19. Autenticación y autorización con JWT. Endpoints protegidos como `POST /api/v1/pedidos` requieren token válido.

20. API RESTful siguiendo Richardson Maturity Model:
    - a. Uso de recursos (`/productos`, `/pedidos`)
    - b. Verbos HTTP (`GET`, `POST`, `PUT`, `DELETE`)
    - c. HATEOAS aplicado parcialmente: la respuesta de `POST /api/v1/pedidos` incluye `_links` con operaciones relacionadas.

22. Versionado de la API implementado mediante prefijos como `/api/v1/` y `/api/v2/`.

26. Migraciones de base de datos gestionadas con Alembic (`alembic/versions/...`).

##Instrucciones para correr el proyecto con Docker

1. Ubicarse en la raíz del proyecto
Asegurate de estar en la carpeta donde está tu Dockerfile.
cd E:\proyectos\EcommercePythonChallenge
2. Guarda todos los archivos
Presioná Ctrl + K S en VS Code (guardar todo).

O asegurate que no haya archivos abiertos con un ● sin guardar.

3. Construir la imagen Docker
docker build -t ecommerce-app .
4. Ejecutá un contenedor
docker run -p 8000:8000 ecommerce-app
Esto:

Expone el puerto 8000 del contenedor en localhost:8000

Ejecuta tu FastAPI con los endpoints funcionando

5. Probalo
Ir a: http://127.0.0.1:8000/docs

Ahí vas a ver Swagger UI con todos tus endpoints

