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

## 🔄 Diagrama de Secuencia – Integración con Servicio de Facturación

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
