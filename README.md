# QA Project - Urban Routes ES

## Descripción del Proyecto
Este proyecto contiene una suite de pruebas automatizadas E2E (End-to-End) para la aplicación web **Urban Routes**. Se cubre el flujo completo de reservación de un taxi, desde la selección de origen y destino, configuración de tarifa Comfort, adición de teléfono, tarjeta de crédito, comentarios al conductor, pedido de accesorios (manta y pañuelos, helados) y la confirmación final de la solicitud.

## Tecnologías y Técnicas Utilizadas
- **Lenguaje:** Python 3.14
- **Framework de pruebas:** Pytest
- **Herramienta de automatización:** Selenium WebDriver
- **Patrón de diseño:** Page Object Model (POM)
- **Monitoreo de red:** Chrome DevTools Protocol (CDP) para captura de registros de rendimiento (SMS / Network logs)

## Instrucciones para Ejecutar las Pruebas

1. **Asegurar las dependencias e instalar requerimientos:**
   Asegúrate de tener un entorno virtual activo y Selenium/Pytest instalados.

2. **Configuración de datos:**
   Revisa que el archivo `data.py` contenga la URL activa del servidor en `urban_routes_url`.

3. **Ejecutar la suite completa de pruebas:**
   Abre la terminal en la raíz del proyecto y ejecuta:

   ```bash
   pytest main.py