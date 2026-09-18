# Índice automático para MdF

Paquete para https://nfueyo.github.io/MdF/. Python 3.9 o posterior, sin librerías externas. No necesitas instalar Python para usar la automatización de GitHub.

## Instalación (una sola vez)

1. Descomprime el ZIP y copia su contenido **en la raíz del repositorio `nfueyo/MdF`**, junto a los HTML actuales. Incluye la carpeta oculta `.github`. No subas el ZIP ni la carpeta que lo contiene. Conserva tus recursos existentes. Si ya existe un `index.html`, guarda una copia fuera del repositorio antes de sustituirlo.
2. Deben quedar estos archivos:
   ```text
   index.html
   README-indice.md
   tools/mdf-index/generate.py
   tools/mdf-index/template.html
   .github/workflows/mdf-pages.yml
   ```
3. En GitHub abre **Settings → Pages → Build and deployment → Source** y selecciona **GitHub Actions**. Si otro workflow publica este mismo sitio, desactívalo para evitar que dos despliegues compitan. Este paquete publica desde la raíz de la rama predeterminada; no requiere una rama `gh-pages` ni una carpeta `docs`.
4. Confirma los archivos y haz push a la rama predeterminada. Si usas Git local, desde la raíz:
   ```sh
   git add index.html README-indice.md tools/mdf-index .github/workflows/mdf-pages.yml
   git commit -m "Añadir índice visual automático"
   git push
   ```
5. En **Actions → Índice docente y GitHub Pages**, espera a que `build` y `deploy` terminen en verde. Abre https://nfueyo.github.io/MdF/. Si instalaste los archivos antes de cambiar el ajuste de Pages, utiliza **Run workflow** en esa misma pantalla.

## Uso diario

Añade, elimina o renombra HTML, HTM o PDF y haz push a la rama predeterminada. Cada push vuelve a examinar el contenido y publica el sitio completo con el índice actualizado. Los cambios en otras ramas no se publican. También puedes lanzar el workflow manualmente desde la rama predeterminada.

El índice se genera en cada despliegue: la automatización **no hace commits ni modifica la copia de `index.html` guardada en Git**. La versión publicada siempre usa el resultado nuevo. Para actualizar también tu copia local, ejecuta desde la raíz:

```sh
python3 tools/mdf-index/generate.py
```

Después puedes confirmar `index.html` si quieres conservar esa instantánea en Git. El script también admite `--root /ruta/al/repositorio`.

## Qué aparece

- HTML/HTM: tarjetas verdes «App HTML».
- PDF: tarjetas de documento en naranja.
- Carpetas con recursos: tarjetas azules que saltan a su sección dentro del índice. Se muestran rutas completas para distinguir carpetas con el mismo nombre. No se depende del listado de directorios de GitHub Pages.
- Títulos derivados del nombre del archivo: guiones y guiones bajos se convierten en espacios; se mantienen siglas y números. `cinema-` se presenta como «Cinemática» y `festat-` como «Estática de fluidos». No se añaden acentos por adivinación.
- Enlaces relativos, con codificación de espacios, acentos y caracteres especiales. Sin fuentes, scripts ni servicios externos.

Se omiten `index.html`/`index.htm` (también los de subcarpetas), `404.html`, archivos ocultos, README, código, configuraciones y formatos distintos de HTML/HTM/PDF. También se omiten recursos dentro de carpetas auxiliares como `.git`, `.github`, `tools`, `scripts`, `assets`, `static`, `images`, `img`, `css`, `js`, `node_modules`, `vendor`, `venv`, `tests`, `dist`, `build`, `work` y `outputs`. Las carpetas vacías no aparecen. No se siguen enlaces simbólicos.

Los recursos auxiliares habituales (CSS, JavaScript, imágenes, datos) siguen publicándose para que funcionen las aplicaciones, aunque no tengan tarjetas. El workflow excluye del despliegue herramientas, configuraciones y carpetas de desarrollo; no almacenes allí archivos que una aplicación necesite servir. El sitio es estático, sin procesamiento Jekyll. Si añades una aplicación con entrada `index.html` en una carpeta, renómbrala (por ejemplo, `app.html`) para que tenga tarjeta o modifica `EXCLUDED_FILES` en el generador.

## Personalización

Edita `TITLE`, `PREFIXES`, `EXCLUDED_DIRS` o `EXCLUDED_FILES` en `tools/mdf-index/generate.py`. Para cambiar colores, textos o columnas, edita `tools/mdf-index/template.html`. No edites a mano el índice generado: la siguiente ejecución lo reemplaza.

## Índice incluido y comprobaciones

El `index.html` incluido es una instantánea generada con los cuatro nombres de aplicaciones presentes en el repositorio público el 18 de septiembre de 2026. No se incluyen copias de esas aplicaciones; sus enlaces funcionan al colocar el paquete junto a los archivos originales. Al generar dentro de una carpeta sin recursos, se muestra un estado vacío, sin enlaces ficticios.

Se han comprobado generación determinista, altas/bajas/renombrados, carpetas, PDF, exclusiones, escape HTML y enlaces con espacios/acentos. El despliegue remoto se ejecutará después de instalar el paquete y activar Pages; no se ha modificado tu repositorio.

Si falla el despliegue, comprueba Source = GitHub Actions, que Actions esté habilitado y que el entorno `github-pages` permita desplegar desde la rama predeterminada. Si una tarjeta abre un 404, verifica el nombre exacto (incluidas mayúsculas) y que el archivo esté confirmado en Git.

Referencia oficial: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
