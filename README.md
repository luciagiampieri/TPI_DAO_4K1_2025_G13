# 🏎 Sistema Integral de Gestión de Alquiler de Vehículos

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

## 🛠️ Tecnologías Principales

| Componente | Tecnología | Lenguaje |
| :--- | :--- | :--- |
| **Backend (API)** | **Flask** (Micro-framework) | Python 3.x |
| **Bussiness Logic / Service Layer** | **SistemaDeAlquiler** (POO) | Python 3.x |
| **Persistencia (DAO)** | **SQLite3** | SQL / Python |
| **Frontend (UI)** | **React** (Single Page Application) | JavaScript / JSX |

---

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura de **capas de servicio (Service Layer)** y **persistencia (DAO)**, desacoplando la lógica de negocio de la implementación de la base de datos y la interfaz de usuario.