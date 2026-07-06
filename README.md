# 🍜 NomNom UMSS

Plataforma backend para comparar puestos de comida universitaria. Los estudiantes pueden explorar, calificar y comparar puestos cercanos a la UMSS. Los dueños pueden registrar su puesto y gestionar su menú.

---

## Stack

| Tecnología | Uso |
|---|---|
| **FastAPI** | Framework web |
| **SQLAlchemy 2.0** (async) | ORM |
| **asyncpg** | Driver PostgreSQL asíncrono |
| **Pydantic v2** | Validación de datos / DTOs |
| **python-jose** | JWT (autenticación) |
| **passlib / bcrypt** | Hash de contraseñas |
| **PostgreSQL** | Base de datos |
| **Uvicorn** | Servidor ASGI |

---

## Estructura del proyecto

```
app/
├── core/
│   ├── config.py          # Variables de entorno (pydantic-settings)
│   ├── database.py        # Engine async + sesión
│   ├── dependencies.py    # get_current_user, require_role
│   ├── mapping_database.py# Importa modelos para que SQLAlchemy los registre
│   └── security.py        # Hash, JWT encode/decode
│
├── modules/
│   ├── users/             # Registro y login
│   ├── food_stalls/       # CRUD de puestos de comida
│   ├── menu/              # Ítems del menú por puesto
│   ├── reviews/           # Reseñas y calificaciones
│   ├── ranking/           # Sistema de ranking Bayesian
│   └── promotions/        # Promociones y ofertas
│
└── main.py                # Entry point, routers, CORS, lifespan
```

Cada módulo sigue el patrón:
```
routes.py → controller.py → service.py → model.py
```

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/mish-0/nomnom-umss.git
cd nomnom-umss
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate       # Linux / Mac
# .venv\Scripts\activate        # Windows

pip install -r app/requirements.txt
```

### 3. Crear el archivo `.env`

```bash
cp .env.example .env
```

Completar con tus credenciales:

```env
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nomnom_db

SECRET_KEY=una-clave-secreta-larga-y-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Correr el servidor

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000`

### 5. Documentación interactiva

| URL | Descripción |
|---|---|
| `http://localhost:8000/docs` | Swagger UI — probar endpoints en vivo |
| `http://localhost:8000/redoc` | ReDoc — documentación navegable |

---

## Endpoints

### 🔐 Auth

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/auth/register` | No | Registrar usuario (ESTUDIANTE o DUENO) |
| `POST` | `/auth/login` | No | Login → devuelve JWT Bearer token |

### 👤 Roles disponibles

| Rol | Puede hacer |
|---|---|
| `ESTUDIANTE` | Ver puestos, menú, ofertas, dejar reseñas |
| `DUENO` | Todo lo anterior + crear y gestionar su propio puesto y menú |

### 🍽️ Puestos de comida

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/food-stalls/` | No | Listar todos los puestos |
| `POST` | `/food-stalls/` | ✅ DUENO | Crear un puesto (owner_id se asigna automáticamente desde el token) |

### 🥗 Menú

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/menu/` | No | Listar todos los ítems |
| `GET` | `/menu/stall/{stall_id}` | No | Menú de un puesto específico |
| `POST` | `/menu/` | ✅ DUENO | Agregar ítem al menú |

### ⭐ Reseñas

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/reviews/` | No | Todas las reseñas |
| `GET` | `/reviews/stall/{stall_id}` | No | Reseñas de un puesto |
| `POST` | `/reviews/` | ✅ Login | Dejar reseña (1 por usuario por puesto) |

### 🏆 Ranking

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/ranking/` | No | Ranking de puestos ordenado por Bayesian score |

---

## Sistema de Ranking — Bayesian Average

El ranking **no usa promedio simple** (`AVG`). Usa **Bayesian Average**:

```
bayesian_score = (C × m + Σ ratings) / (C + n)
```

| Variable | Significado |
|---|---|
| `C` | Parámetro de confianza (= 10 en este proyecto) |
| `m` | Promedio global de **todas** las reseñas del sistema |
| `n` | Número de reseñas del puesto |
| `Σ ratings` | Suma de ratings del puesto |

### ¿Por qué no promedio simple?

| Puesto | Reseñas | Promedio simple | Bayesian score |
|---|---|---|---|
| Puesto A | 1 reseña de ⭐⭐⭐⭐⭐ | 5.00 | ~3.36 |
| Puesto B | 80 reseñas promedio 4.7 | 4.70 | ~4.67 |

Con promedio simple, el Puesto A ganaría con una sola reseña. Con Bayesian Average, el Puesto B rankea mejor porque tiene **evidencia real** detrás de su calificación.

A medida que un puesto acumula más reseñas, su `bayesian_score` converge hacia su promedio real.

---

## Seguridad

- Las contraseñas se almacenan hasheadas con **bcrypt** (nunca en texto plano)
- La autenticación usa **JWT Bearer tokens** con expiración configurable
- El `owner_id` en puestos y el `user_id` en reseñas **nunca vienen del body** — se extraen del token para evitar suplantación
- Las rutas de escritura están protegidas por rol con la dependencia `require_role`
- Un usuario solo puede dejar **una reseña por puesto** (UniqueConstraint a nivel de BD)

---

## Autor

**Michelle Delgadillo** — Postulante SCESI 2025  
Universidad Mayor de San Simón — Ingeniería Informática  
GitHub: [@mish-0](https://github.com/mish-0)
