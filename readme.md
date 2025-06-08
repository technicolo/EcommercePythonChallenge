```mermaid
erDiagram
    USUARIO ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ DETALLE_PEDIDO : contiene
    PRODUCTO ||--o{ DETALLE_PEDIDO : esta_en

    USUARIO {
        int id
        string nombre
        string email
    }

    PEDIDO {
        int id
        datetime fecha
        float total
        int usuario_id
    }

    PRODUCTO {
        int id
        string nombre
        float precio
        int stock
    }

    DETALLE_PEDIDO {
        int id
        int pedido_id
        int producto_id
        int cantidad
        float precio_unitario
    }
