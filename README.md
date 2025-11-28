# 🏎 Sistema Integral de Gestión de Alquiler de Vehículos - Formula Car

Este repositorio contiene un Sistema Integral de Gestión de Alquiler de Vehículos, desarrollado por el Grupo 13 del curso 4k1 como un proyecto full-stack en el contexto de la materia *Desarrollo de Aplicaciones con Objetos (DAO)* de la UTN.

El objetivo es gestionar todas las operaciones de la compañía, desde el ABM de entidades hasta la transacción principal de registro y finalización de alquileres, incluyendo la validación de disponibilidad y generación de reportes.

---

## 👥 Integrantes del Grupo

| Nombre y Apellido | Legajo |
| :--- | :--- |
| CHIALVA Fátima | 95147 |
| GATICA Andrea Ticiana | 94371 |
| GIAMPIERI Lucia | 96505 |
| PAEZ María Candela | 95256 |
| STEFFOLANI Nicolas | 94196 |

---
## 🚀 Funcionalidades Clave
El sistema no es solo un ABM (Alta, Baja, Modificación), incluye lógica de negocio compleja y reportes visuales:
- Gestión de Flota: ABM de vehículos con control de estados (Disponible, Alquilado, En Mantenimiento).
- Transacción de Alquiler:
    1. Validación de disponibilidad en tiempo real (evita solapamientos).
    2. Ciclo de vida completo: Reserva -> En Curso -> Finalización/Cancelación.
    3. Cálculo automático de costos y actualización de kilometraje al finalizar.
- Gestión de Mantenimiento: Registro de reparaciones y control de indisponibilidad del vehículo.
- Tablero de Control (Dashboard):
    1. KPIs en tiempo real (Ingresos del mes, Autos alquilados).
    2. Gráficos interactivos de facturación y tendencias.
    3. Ranking de vehículos más populares.

---

## 🛠️ Tecnologías Principales

| Componente | Tecnología | Lenguaje |
| :--- | :--- | :--- |
| **Backend (API REST)** | **Flask** (Micro-framework) | Python 3.12+ |
| **Bussiness Logic / Service Layer** | **SistemaDeAlquiler** (POO) | Python 3.12+ |
| **Persistencia (DAO)** | **MySQL** | SQL / Python |
| **Frontend (UI)** | **React 18** (Single Page Application) | JavaScript / JSX |
| **Visualización de Datos** | **Recharts** | Gráficos |

---

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura desacoplada para facilitar el mantenimiento y la escalabilidad:

```text
TPDAO/
├── BACK/                   # Lógica del Servidor
│   ├── modelos/            # Clases de Negocio (POO)
│   ├── SistemaDeAlquiler.py # Service Layer (Orquestador de lógica)
│   ├── routes.py           # API Endpoints (Flask)
│   └── GestorReportes.py   # Lógica específica de reportes
├── BD/                     # Persistencia
│   ├── manager/            # Data Access Objects (DAO)
│   └── db_conection.py     # Conexión a MySQL
└── FRONT/                  # Interfaz de Usuario
    ├── src/
    │   ├── pages/          # Vistas principales
    │   ├── components/     # Componentes reutilizables
    │   └── services/       # Comunicación con la API
```

---

## ⚙️ Instalación y Ejecución
1. **Backend**
  ```text
# Instalar dependencias
pip install flask pymysql

# Ejecutar servidor (desde la carpeta raíz)
    1. python -m BACK.routes
    2. flask run --port=5000
``` 

2. **Frontend**
 ```text
cd FRONT
npm install
npm run dev
```

---

## 📊 Base de Datos
El script de creación y población inicial de la base de datos `(alquiler_autos)` se encuentra disponible en la carpeta `BD/README.md` o `schema.sql`.
