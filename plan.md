# Plan de Implementación: Dashboard de Calificaciones para Docentes

## Fase 1: Configuración de Base de Datos y Estado Base ✅
- [x] Instalar pymongo para conexión a MongoDB
- [x] Crear estado principal con conexión a base de datos
- [x] Implementar función para obtener información del docente
- [x] Crear mapeo de grados a números (Grupo 1=1, Grupo 2=2, etc.)
- [x] Configurar estructura base del dashboard con Material Design 3

## Fase 2: Interfaz de Selección y Carga de Estudiantes ✅
- [x] Crear componente de selección de asignaciones del docente (grado, sección, materia)
- [x] Implementar lógica para manejo de sección "Ambas" (mostrar opciones A y B)
- [x] Crear botón de carga de estudiantes con validación
- [x] Implementar consulta a colección "2025-2026" con filtros de grado y sección
- [x] Mostrar lista de estudiantes en tabla con Material Design

## Fase 3: Sistema de Calificaciones Editable ✅
- [x] Crear estructura para columnas de calificaciones dinámicas
- [x] Implementar diálogos para agregar descripción de actividad y fecha
- [x] Crear tabla editable con validación (no editable hasta tener descripción/fecha)
- [x] Implementar guardado de calificaciones en base de datos
- [x] Agregar funcionalidad para agregar/eliminar columnas de actividades
- [x] Mostrar indicadores visuales de estado (guardado, editando, etc.)

## Fase 4: Verificación de UI ✅
- [x] Verificar login y carga de datos del docente
- [x] Verificar selección de asignaciones y carga de estudiantes
- [x] Verificar diálogo de agregar actividades
- [x] Verificar tabla de calificaciones editable y guardado automático
