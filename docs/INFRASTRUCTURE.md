# Capítulo 1 - Creación del VPS

## Objetivo

El primer paso para poner en funcionamiento TimeBoard Time Service (TBTS) consiste en disponer de un servidor virtual privado (VPS) conectado permanentemente a Internet.

Este capítulo documenta el proceso de selección del proveedor, la configuración inicial del servidor y las decisiones tomadas durante la creación de la infraestructura.

El objetivo es que cualquier persona pueda recrear un entorno equivalente siguiendo únicamente este documento.

---

# ¿Por qué un VPS?

TBTS debía cumplir una serie de requisitos desde su concepción:

- Disponibilidad las 24 horas del día.
- Dirección IP pública fija.
- Bajo costo de mantenimiento.
- Acceso completo al sistema operativo.
- Posibilidad de instalar cualquier software necesario.
- Facilidad para migrar el servicio a otro proveedor en el futuro.

Existen numerosas alternativas para alojar una aplicación web, como plataformas PaaS, servicios serverless o hosting compartido. Sin embargo, un VPS ofrece un excelente equilibrio entre flexibilidad, simplicidad y costo.

Además, disponer de acceso completo al sistema operativo permite comprender en profundidad cómo funciona toda la infraestructura, evitando depender de servicios administrados o configuraciones opacas.

---

# Proveedor elegido

Para este proyecto se eligió **Hetzner Cloud** como proveedor de infraestructura.

https://www.hetzner.com/cloud

La elección se basó en varios factores:

- Excelente relación precio/rendimiento.
- Centros de datos confiables.
- Excelente reputación dentro de la comunidad Linux.
- API disponible para automatización futura.
- Muy buena documentación oficial.
- Posibilidad de ampliar recursos sin reinstalar el servidor.

Hasta el momento de escribir este documento, Hetzner ha demostrado una excelente estabilidad y disponibilidad.

No obstante, el diseño de TBTS procura evitar cualquier dependencia específica del proveedor. Si en el futuro fuera necesario migrar a otro servicio, la aplicación debería poder trasladarse sin modificaciones significativas.

---

# Especificaciones del servidor

Las características elegidas para el servidor fueron deliberadamente modestas.

TBTS consume muy pocos recursos debido a la simplicidad de la aplicación.

La configuración inicial fue suficiente para alojar simultáneamente:

- Portfolio personal.
- TimeBoard Time Service.
- Nginx.
- Gunicorn.
- Flask.
- Certbot.
- Servicios básicos del sistema operativo.

En caso de que el proyecto creciera considerablemente, bastaría con aumentar los recursos del VPS sin modificar la arquitectura del software.

---

# Sistema operativo

Se eligió **Ubuntu Server LTS** como sistema operativo.

Las razones principales fueron:

- Amplio soporte de la comunidad.
- Gran cantidad de documentación disponible.
- Excelente compatibilidad con Python.
- Ciclos de soporte prolongados (Long Term Support).
- Gran disponibilidad de paquetes mediante APT.

Elegir una versión LTS reduce significativamente la frecuencia de actualizaciones mayores del sistema operativo y mejora la estabilidad del entorno de producción.

---

# Ubicación del servidor

Al momento de crear el VPS es conveniente seleccionar el centro de datos más cercano a la mayor parte de los usuarios del servicio.

En el caso de TBTS, la latencia no representa un aspecto crítico debido al pequeño tamaño de las respuestas intercambiadas.

Aun así, se recomienda elegir una ubicación geográfica estable y con buena conectividad internacional.

---

# Nombre del servidor

Durante la creación del VPS se asignó un nombre descriptivo al servidor.

Hostname utilizado:

```
coloratura
```

Elegir nombres significativos facilita la administración cuando existen varios servidores.

Aunque actualmente el proyecto utiliza un único VPS, mantener una convención de nombres desde el comienzo ayuda a escalar la infraestructura en el futuro.

---

# Dirección IP

Una vez creado el servidor, el proveedor asignó una dirección IPv4 pública.

Esta dirección constituye el punto de entrada hacia toda la infraestructura y posteriormente será utilizada para:

- Configurar Cloudflare.
- Configurar el dominio.
- Establecer conexiones SSH.
- Emitir certificados TLS.
- Publicar el sitio web.
- Publicar la API de TBTS.

Es recomendable documentar la dirección IP actual en un lugar seguro.

No obstante, este documento evita registrar información que pueda cambiar con el tiempo.

---

# Acceso inicial

Una vez disponible el VPS, Hetzner proporciona acceso mediante SSH.

Durante el primer inicio de sesión aún no existe ninguna configuración personalizada.

El servidor se encuentra prácticamente en estado de fábrica.

A partir de este momento comenzará el proceso de preparación del sistema operativo.

Los siguientes capítulos describen dicho proceso en detalle.

---

# Consideraciones de diseño

Aunque crear un VPS es una tarea sencilla, esta decisión condiciona toda la infraestructura posterior.

Por ese motivo se procuró elegir una plataforma que cumpliera los siguientes principios:

- Simplicidad.
- Bajo costo.
- Alta disponibilidad.
- Independencia del proveedor.
- Facilidad de mantenimiento.
- Posibilidad de reconstrucción completa.

Estos principios acompañarán todas las decisiones técnicas documentadas en este manual.

---

# Resumen

Al finalizar este capítulo se dispone de:

- Un VPS operativo.
- Ubuntu Server instalado.
- Acceso SSH inicial.
- Una dirección IP pública.
- Un hostname definido.

Todavía no existe ninguna aplicación instalada.

El servidor únicamente ejecuta el sistema operativo recién instalado y constituye la base sobre la cual se construirá toda la infraestructura de TBTS.

En el siguiente capítulo se documentará la preparación inicial del sistema operativo, incluyendo la actualización de paquetes, configuración básica, usuarios, acceso SSH y medidas iniciales de seguridad.

---

# Capítulo 2 - Preparación inicial del servidor

## Objetivo

Una vez creado el VPS, el siguiente paso consiste en preparar el sistema operativo para convertirlo en un entorno de producción estable, seguro y fácilmente mantenible.

El servidor recién instalado proporciona únicamente una instalación básica de Ubuntu Server. Antes de desplegar cualquier aplicación es recomendable realizar una serie de tareas iniciales que servirán como base para toda la infraestructura.

Este capítulo documenta dichas tareas y explica la razón detrás de cada una de ellas.

---

# Estado inicial del servidor

Al completar la creación del VPS, el sistema operativo se encuentra prácticamente en estado de fábrica.

En este momento todavía no existen:

- aplicaciones instaladas;
- servicios web;
- certificados TLS;
- dominios configurados;
- usuarios personalizados;
- firewall configurado.

El único objetivo durante esta etapa consiste en preparar un entorno limpio sobre el cual construir el resto de la infraestructura.

---

# Primer acceso mediante SSH

El acceso inicial al servidor se realiza utilizando SSH.

Este mecanismo permite administrar el servidor de forma remota mediante una conexión cifrada.

Desde este momento, prácticamente toda la administración del servidor se realizará utilizando la terminal.

Se recomienda evitar el uso de herramientas gráficas de administración siempre que sea posible.

Esto facilita la automatización, mejora la reproducibilidad y reduce el consumo de recursos.

---

# Actualización del sistema

Antes de instalar cualquier software adicional es recomendable actualizar completamente el sistema operativo.

Esto garantiza que todos los paquetes instalados correspondan a las últimas versiones disponibles para la distribución utilizada.

La actualización inicial reduce la probabilidad de encontrar errores ya corregidos y permite comenzar el proyecto sobre una base estable.

Durante esta etapa también pueden instalarse actualizaciones del kernel.

En ese caso será necesario reiniciar el servidor una vez finalizado el proceso.

---

# Sincronización horaria

Uno de los aspectos más importantes de cualquier servidor es mantener la hora del sistema correctamente sincronizada.

Aunque TBTS proporciona la hora UTC a otros dispositivos, la propia aplicación depende de que el sistema operativo mantenga un reloj preciso.

Ubuntu incorpora mecanismos automáticos de sincronización horaria que normalmente no requieren intervención manual.

No obstante, resulta conveniente verificar que el servicio correspondiente se encuentre activo y funcionando correctamente.

Una hora incorrecta puede provocar problemas con certificados TLS, registros del sistema y tareas programadas.

---

# Configuración regional

Se recomienda revisar los siguientes parámetros del sistema:

- zona horaria;
- configuración regional (locale);
- distribución del teclado;
- formato de fechas y horas.

En el caso de TBTS, la aplicación siempre trabaja internamente utilizando UTC.

Sin embargo, el servidor puede utilizar la zona horaria que resulte más cómoda para las tareas de administración.

Lo importante es mantener un criterio consistente durante toda la vida útil del servidor.

---

# Nombre del equipo

Durante la creación del VPS se definió el hostname:

```
coloratura
```

Es recomendable verificar que dicho nombre haya quedado correctamente configurado.

El hostname aparecerá frecuentemente en:

- sesiones SSH;
- registros del sistema;
- archivos de configuración;
- mensajes de diagnóstico.

Mantener un nombre descriptivo facilita enormemente la administración cuando existen múltiples servidores.

---

# Verificación de conectividad

Antes de continuar conviene comprobar que el servidor posee conectividad completa hacia Internet.

Esta comprobación permitirá posteriormente:

- instalar paquetes;
- descargar dependencias;
- clonar repositorios;
- emitir certificados TLS;
- resolver nombres DNS.

Si el servidor no dispone de conectividad adecuada, cualquier problema debería resolverse antes de continuar con la instalación.

---

# Organización del sistema

Desde el comienzo del proyecto es recomendable mantener una estructura organizada.

Todas las aplicaciones instaladas manualmente deberían ubicarse en directorios claramente identificables.

En el caso de TBTS se adoptó la siguiente estructura:

```
/opt/
└── timeboard-time-service/
```

El directorio `/opt` se utiliza tradicionalmente para aplicaciones instaladas manualmente y separadas del software distribuido por el sistema operativo.

Mantener esta organización simplifica las tareas de mantenimiento y facilita futuras migraciones.

---

# Filosofía de administración

Desde el inicio del proyecto se adoptó una política muy simple:

> Mantener el servidor lo más sencillo posible.

Cada componente adicional implica:

- más mantenimiento;
- mayor superficie de ataque;
- más actualizaciones;
- mayor complejidad.

Por ese motivo se evita instalar software que no aporte un beneficio claro al proyecto.

La simplicidad constituye una de las principales características de la infraestructura de TBTS.

---

# Buenas prácticas

Durante esta etapa conviene adoptar algunas normas que se mantendrán durante toda la vida útil del servidor.

## Documentar cada cambio

Toda modificación realizada sobre el servidor debería quedar reflejada en este manual.

La documentación debe evolucionar junto con la infraestructura.

---

## Evitar cambios innecesarios

No modificar configuraciones únicamente por seguir tendencias o recomendaciones genéricas.

Cada cambio debe tener una justificación técnica concreta.

---

## Mantener una arquitectura consistente

Es preferible seguir una estructura simple y bien conocida antes que incorporar tecnologías adicionales que el proyecto realmente no necesita.

---

# Resumen

Al finalizar este capítulo se dispone de un servidor completamente actualizado y preparado para comenzar la instalación de la infraestructura de TBTS.

Todavía no existe ninguna aplicación desplegada, pero el sistema operativo ya constituye una base sólida sobre la cual instalar el resto de los componentes.

En el próximo capítulo se abordará la configuración inicial de seguridad del servidor, incluyendo usuarios, autenticación mediante SSH, firewall y otras medidas destinadas a proteger el entorno de producción desde el primer momento.

---

# Capítulo 3 - Configuración inicial del sistema

## Objetivo

Una vez instalado y actualizado el sistema operativo, el siguiente paso consiste en preparar el servidor para su utilización en un entorno de producción.

Aunque Ubuntu Server puede utilizarse inmediatamente después de su instalación, dedicar unos minutos a configurar correctamente el sistema evita numerosos problemas futuros y proporciona una base mucho más sólida para el resto de la infraestructura.

Las tareas descritas en este capítulo deberían realizarse antes de instalar cualquier aplicación.

---

# Filosofía

El servidor que aloja TBTS sigue un principio muy simple:

> Todo aquello que no sea necesario para el funcionamiento del servicio no debería instalarse.

Reducir la cantidad de software instalado disminuye:

- la superficie de ataque;
- la cantidad de actualizaciones;
- el consumo de recursos;
- la complejidad administrativa.

La simplicidad constituye uno de los pilares fundamentales de este proyecto.

---

# Usuario administrativo

Aunque Ubuntu permite administrar inicialmente el servidor utilizando el usuario creado durante la instalación (o el usuario proporcionado por el proveedor del VPS), es importante evitar trabajar de forma permanente como superusuario.

Las tareas administrativas deberán ejecutarse únicamente cuando resulte necesario mediante privilegios elevados.

Este criterio reduce considerablemente la posibilidad de cometer errores accidentales.

---

# Acceso mediante SSH

Toda la administración del servidor se realiza utilizando SSH.

No se instalaron herramientas de administración remota con interfaz gráfica.

Las razones son las siguientes:

- menor consumo de recursos;
- mayor seguridad;
- facilidad para automatizar tareas;
- posibilidad de trabajar desde cualquier sistema operativo.

SSH constituye el único mecanismo habitual de administración del servidor.

---

# Autenticación

Siempre que sea posible, se recomienda utilizar autenticación basada en claves SSH en lugar de contraseñas.

Las claves públicas ofrecen un nivel de seguridad considerablemente superior y eliminan la necesidad de recordar contraseñas complejas.

En entornos de producción también resulta recomendable deshabilitar el acceso mediante contraseña una vez verificado el correcto funcionamiento de las claves.

---

# Firewall

Todo servidor conectado permanentemente a Internet debería utilizar un firewall.

Ubuntu incorpora UFW (Uncomplicated Firewall), una herramienta sencilla que facilita la administración de reglas sin necesidad de interactuar directamente con iptables.

El firewall debe configurarse siguiendo el principio de mínimo privilegio.

Es decir:

> Permitir únicamente el tráfico estrictamente necesario.

En el caso de TBTS, los únicos servicios que requieren acceso público son:

- HTTP (80)
- HTTPS (443)
- SSH (22)

Cualquier otro puerto debería permanecer cerrado.

---

# Actualizaciones

Mantener el sistema operativo actualizado constituye una de las tareas de mantenimiento más importantes.

Sin embargo, las actualizaciones deben realizarse de forma controlada.

Antes de aplicar cambios importantes se recomienda:

- verificar que existan copias de seguridad recientes;
- revisar las notas de la actualización cuando corresponda;
- confirmar que el servicio funciona correctamente una vez finalizado el proceso.

Actualizar indiscriminadamente todos los paquetes sin realizar verificaciones posteriores puede provocar interrupciones inesperadas.

---

# Sincronización de hora

Aunque Ubuntu sincroniza automáticamente la hora del sistema, conviene verificar periódicamente que dicho mecanismo continúe funcionando correctamente.

TBTS obtiene la hora directamente del sistema operativo.

Por ese motivo, cualquier desviación del reloj afectará inmediatamente a todos los clientes que utilicen la API.

Mantener una hora precisa constituye un requisito esencial para el correcto funcionamiento del servicio.

---

# Organización del sistema de archivos

Con el objetivo de mantener una estructura ordenada, el proyecto adopta la siguiente convención.

Aplicación:

```
/opt/timeboard-time-service
```

Archivos de configuración de Nginx:

```
/etc/nginx/
```

Servicios de systemd:

```
/etc/systemd/system/
```

Registros del sistema:

```
journalctl
```

Esta distribución sigue las convenciones habituales de Linux y facilita la localización de cada componente.

---

# Política de instalación de software

Antes de instalar cualquier paquete nuevo conviene responder una pregunta sencilla.

> ¿Este software aporta un beneficio real al proyecto?

Si la respuesta es negativa, probablemente no debería instalarse.

Evitar dependencias innecesarias simplifica las tareas de mantenimiento y reduce la probabilidad de conflictos futuros.

---

# Convenciones utilizadas

Desde el comienzo del proyecto se adoptaron algunas convenciones destinadas a mantener la infraestructura consistente.

## Una aplicación por servicio

Cada servicio debe tener una única responsabilidad.

Por ejemplo:

- Nginx actúa como reverse proxy.
- Gunicorn ejecuta la aplicación.
- Flask implementa la lógica del servicio.

No deben mezclarse responsabilidades entre componentes.

---

## Configuración explícita

Siempre que sea posible, las configuraciones deben ser claras y fáciles de entender.

Es preferible un archivo ligeramente más extenso pero bien documentado que una configuración extremadamente compacta y difícil de mantener.

---

## Evitar configuraciones "mágicas"

Toda modificación importante debería poder justificarse técnicamente.

Las configuraciones copiadas de Internet sin comprender su funcionamiento terminan convirtiéndose en una fuente de problemas a largo plazo.

---

# Consideraciones de seguridad

Aunque TBTS no almacena información sensible ni dispone de una base de datos, continúa siendo un servicio expuesto a Internet.

Por ese motivo resulta conveniente asumir que cualquier endpoint público será eventualmente analizado por bots automatizados.

La infraestructura debe diseñarse teniendo presente esta realidad.

Las medidas de seguridad incorporadas posteriormente (Cloudflare, Flask-Limiter, HTTPS para el portfolio, firewall y actualizaciones periódicas) forman parte de una estrategia de defensa en profundidad.

Ninguna de ellas resulta suficiente por sí sola.

Su combinación proporciona un nivel de protección significativamente superior.

---

# Resumen

Al finalizar este capítulo el servidor dispone de una configuración básica adecuada para un entorno de producción.

El sistema operativo se encuentra organizado, actualizado y preparado para comenzar la instalación de los componentes que darán soporte a TBTS.

En el siguiente capítulo se abordará la preparación del entorno de desarrollo de Python, incluyendo la instalación de las herramientas necesarias, la creación del entorno virtual y la estructura definitiva del proyecto.

---

# Capítulo 4 - Preparación del entorno Python

## Objetivo

Una vez preparado el sistema operativo, el siguiente paso consiste en instalar el entorno necesario para ejecutar aplicaciones desarrolladas en Python.

TBTS fue desarrollado utilizando Flask, un framework web ligero que se ejecuta sobre el intérprete oficial de Python.

Aunque Ubuntu incluye Python instalado por defecto, resulta recomendable preparar un entorno independiente para cada aplicación.

Esta decisión evita conflictos entre proyectos, simplifica las actualizaciones y permite mantener un mejor control sobre las dependencias instaladas.

---

# ¿Por qué Python?

La elección de Python fue consecuencia de varios factores.

Entre ellos:

- lenguaje moderno y ampliamente adoptado;
- excelente ecosistema de librerías;
- gran documentación;
- curva de aprendizaje reducida;
- excelente integración con Linux;
- muy buena compatibilidad con servidores WSGI.

Para un servicio pequeño como TBTS, Python ofrece una excelente relación entre simplicidad y productividad.

---

# ¿Por qué Flask?

Existen numerosos frameworks web para Python.

Entre los más conocidos se encuentran:

- Django
- Flask
- FastAPI
- Bottle
- Pyramid

Para TBTS se eligió Flask debido a su filosofía minimalista.

La aplicación únicamente necesita responder unas pocas solicitudes HTTP.

No requiere:

- autenticación compleja;
- administración de usuarios;
- paneles administrativos;
- ORM;
- plantillas avanzadas;
- sesiones.

Flask proporciona exactamente las herramientas necesarias sin incorporar funcionalidades que el proyecto no necesita.

---

# Entorno virtual

Una de las primeras decisiones del proyecto consistió en utilizar un entorno virtual de Python.

Un entorno virtual permite instalar todas las dependencias de una aplicación de forma completamente aislada del resto del sistema operativo.

Esto evita modificar el Python global instalado por Ubuntu y elimina conflictos entre proyectos.

Cada aplicación mantiene así su propio conjunto de librerías y versiones.

---

# Ventajas del entorno virtual

Utilizar un entorno virtual aporta numerosas ventajas.

Entre ellas:

- aislamiento de dependencias;
- facilidad para actualizar paquetes;
- posibilidad de utilizar versiones diferentes entre proyectos;
- mayor estabilidad;
- despliegues reproducibles.

Actualmente constituye una práctica estándar dentro del ecosistema Python.

---

# Ubicación del proyecto

La aplicación se instaló bajo el directorio:

```
/opt/timeboard-time-service
```

La estructura general del proyecto es la siguiente.

```
/opt
└── timeboard-time-service
    ├── app.py
    ├── requirements.txt
    ├── static/
    ├── templates/
    ├── venv/
    ├── README.md
    └── ...
```

Mantener todos los archivos relacionados con la aplicación dentro de un único directorio simplifica enormemente las tareas de mantenimiento.

---

# El archivo requirements.txt

Todas las dependencias utilizadas por TBTS se registran en un único archivo denominado:

```
requirements.txt
```

Este archivo constituye una pieza fundamental del proyecto.

Permite reconstruir el entorno Python completo utilizando un único comando.

Gracias a este mecanismo cualquier servidor puede instalar exactamente las mismas versiones de todas las librerías utilizadas durante el desarrollo.

---

# Dependencias del proyecto

A medida que el proyecto fue evolucionando, se incorporaron diversas librerías.

Entre las más importantes se encuentran:

## Flask

Framework principal utilizado para implementar la aplicación.

---

## Gunicorn

Servidor WSGI encargado de ejecutar Flask en producción.

Aunque forma parte del entorno Python, su función será explicada en detalle en un capítulo posterior.

---

## Flask-Limiter

Incorporado posteriormente para proteger la API frente a abusos.

Esta librería permite limitar automáticamente la cantidad de solicitudes que un cliente puede realizar durante un período determinado.

Su incorporación respondió a la necesidad de proteger el servicio frente a escaneos automatizados y ataques de fuerza bruta.

---

## Otras dependencias

Además de las librerías principales, el proyecto utiliza diversas dependencias auxiliares instaladas automáticamente por pip.

En general, estas librerías no se utilizan directamente desde el código fuente, sino que forman parte del funcionamiento interno de Flask y sus extensiones.

---

# Organización del código

Desde el comienzo del proyecto se procuró mantener una estructura simple.

TBTS no pretende convertirse en una aplicación monolítica.

Cada archivo debe tener una responsabilidad claramente definida.

A medida que el proyecto crezca, podrán incorporarse nuevos módulos sin alterar la arquitectura general.

---

# Actualización de dependencias

Las librerías utilizadas por el proyecto deberían mantenerse razonablemente actualizadas.

Sin embargo, no resulta recomendable actualizar versiones importantes directamente sobre el servidor de producción.

Siempre que sea posible:

- actualizar primero el entorno de desarrollo;
- ejecutar las pruebas correspondientes;
- verificar la compatibilidad;
- recién entonces desplegar la nueva versión.

Este procedimiento reduce considerablemente el riesgo de interrupciones inesperadas.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS quedó demostrado que mantener un entorno virtual independiente simplificó enormemente las tareas de mantenimiento.

Fue posible incorporar nuevas dependencias, como Flask-Limiter, sin afectar otras aplicaciones instaladas en el servidor.

Asimismo, cualquier desarrollador puede recrear exactamente el mismo entorno ejecutando la instalación de dependencias especificadas en `requirements.txt`.

Esta decisión resultó especialmente valiosa al configurar un segundo entorno de desarrollo en Windows, donde bastó con crear un nuevo entorno virtual e instalar las dependencias para obtener un entorno idéntico al del servidor Linux.

---

# Resumen

Al finalizar este capítulo se dispone de un entorno Python completamente preparado para ejecutar TBTS.

El proyecto cuenta con una estructura organizada, un entorno virtual independiente y un mecanismo reproducible para instalar todas sus dependencias.

En el siguiente capítulo se documentará el despliegue de la aplicación propiamente dicha, incluyendo la obtención del código fuente, la organización del repositorio y la preparación para su ejecución en producción.

---

# Capítulo 5 - Despliegue de la aplicación

## Objetivo

Con el sistema operativo preparado y el entorno Python completamente configurado, el siguiente paso consiste en desplegar la aplicación TimeBoard Time Service sobre el servidor.

Este capítulo documenta la organización del proyecto, la obtención del código fuente y la estructura definitiva utilizada en producción.

El objetivo es conseguir que la aplicación pueda mantenerse, actualizarse y desplegarse de forma sencilla durante toda su vida útil.

---

# Repositorio Git

Desde sus primeras versiones, TBTS se desarrolló utilizando Git como sistema de control de versiones.

El código fuente se aloja en GitHub, lo que proporciona numerosas ventajas.

Entre ellas:

- historial completo de cambios;
- posibilidad de volver a versiones anteriores;
- respaldo remoto;
- colaboración futura;
- despliegues reproducibles.

La infraestructura de producción siempre debe ejecutarse utilizando una copia obtenida desde el repositorio oficial.

Esto garantiza que el servidor permanezca sincronizado con el estado real del proyecto.

---

# Ubicación del proyecto

Se decidió alojar el código fuente dentro del siguiente directorio:

```
/opt/timeboard-time-service
```

Esta ubicación presenta varias ventajas.

- mantiene separadas las aplicaciones instaladas manualmente del resto del sistema operativo;
- simplifica las copias de seguridad;
- facilita futuras migraciones;
- sigue las convenciones habituales de Linux.

Toda la aplicación queda contenida dentro de un único directorio.

---

# Organización del repositorio

La estructura del proyecto fue diseñada para resultar sencilla de comprender.

Una distribución típica es la siguiente.

```
timeboard-time-service/

├── app.py
├── requirements.txt
├── README.md
├── DEPLOY.md
├── static/
├── templates/
├── venv/
└── ...
```

Cada archivo posee una responsabilidad claramente definida.

Evitar estructuras innecesariamente complejas facilita el mantenimiento del proyecto.

---

# Gestión de dependencias

El archivo `requirements.txt` constituye la referencia oficial de todas las librerías utilizadas por la aplicación.

Durante el despliegue, todas las dependencias deben instalarse utilizando dicho archivo.

De esta forma se garantiza que los entornos de desarrollo y producción utilicen exactamente las mismas versiones.

Esta práctica evita numerosos problemas relacionados con diferencias entre equipos.

---

# Evolución del proyecto

A diferencia de muchas aplicaciones que nacen completamente definidas, TBTS fue evolucionando de forma incremental.

Las primeras versiones únicamente devolvían la fecha y hora UTC.

Posteriormente fueron incorporándose nuevas funcionalidades y mejoras, entre ellas:

- endpoint de estado (`/api/health`);
- documentación de la API;
- landing page del servicio;
- integración con el portfolio personal;
- protección mediante Flask-Limiter;
- separación entre sitio web y API;
- mejoras de seguridad.

Cada incorporación respondió a una necesidad concreta detectada durante la evolución del proyecto.

---

# Filosofía de despliegue

Durante el desarrollo se adoptó una política muy simple.

> El servidor nunca debe contener modificaciones manuales que no existan también en Git.

Toda modificación permanente debe incorporarse al repositorio.

Este criterio ofrece numerosas ventajas.

- cualquier servidor puede reconstruirse desde cero;
- todas las modificaciones quedan registradas;
- es posible volver a versiones anteriores;
- el código desplegado coincide con el código versionado.

En otras palabras:

> Git constituye la única fuente de verdad del proyecto.

---

# Actualización del código

Cuando se publica una nueva versión, el procedimiento consiste simplemente en actualizar el repositorio del servidor.

Posteriormente se reinstalan las dependencias únicamente si resulta necesario y finalmente se reinicia el servicio.

Mantener este procedimiento simple reduce considerablemente la probabilidad de errores durante un despliegue.

---

# Archivos que nunca deben modificarse directamente

Aunque técnicamente es posible editar cualquier archivo directamente sobre el servidor, esta práctica debe evitarse.

Las modificaciones permanentes deben realizarse siempre sobre el repositorio local de desarrollo.

El flujo recomendado es:

Desarrollo

↓

Commit

↓

Push a GitHub

↓

Actualización del servidor

↓

Reinicio del servicio

Este procedimiento mantiene un historial completo de todas las modificaciones realizadas sobre el proyecto.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS surgieron numerosas oportunidades para realizar pequeñas modificaciones directamente sobre el servidor.

Sin embargo, mantener el repositorio como única fuente de verdad simplificó enormemente el mantenimiento.

Cada cambio quedó registrado, documentado y disponible para cualquier instalación futura.

Esta decisión también permitió preparar un segundo entorno de desarrollo en Windows utilizando exactamente el mismo código fuente.

---

# Consideraciones sobre el entorno de producción

Aunque el servidor ejecuta el mismo código que el entorno de desarrollo, existen algunas diferencias importantes.

En producción:

- Flask nunca se ejecuta utilizando su servidor de desarrollo.
- La aplicación se ejecuta mediante Gunicorn.
- Nginx actúa como reverse proxy.
- systemd administra el ciclo de vida del servicio.
- Cloudflare protege el acceso público.

Estas diferencias serán desarrolladas en detalle en los capítulos siguientes.

---

# Resumen

Al finalizar este capítulo el código fuente de TBTS ya se encuentra desplegado sobre el servidor.

La aplicación dispone de una estructura organizada, todas sus dependencias están correctamente definidas y el proyecto puede evolucionar mediante Git sin introducir modificaciones manuales sobre el entorno de producción.

En el próximo capítulo comenzará la configuración del primer componente de producción: Gunicorn, el servidor WSGI encargado de ejecutar la aplicación Flask de forma estable y eficiente.

---
# Capítulo 6 - Gunicorn: el servidor de aplicaciones

## Objetivo

Hasta este momento, TBTS dispone de un sistema operativo correctamente configurado, un entorno Python preparado y el código fuente desplegado sobre el servidor.

Sin embargo, la aplicación todavía no está preparada para ejecutarse en un entorno de producción.

Este capítulo describe el componente encargado de ejecutar la aplicación Flask de forma estable, eficiente y segura: **Gunicorn**.

También explica por qué se eligió esta tecnología y cuál es su función dentro de la arquitectura general del sistema.

---

# ¿Qué es Gunicorn?

Gunicorn (Green Unicorn) es un servidor WSGI para aplicaciones desarrolladas en Python.

Su función consiste en ejecutar la aplicación Flask y atender las solicitudes que posteriormente serán enviadas por Nginx.

Es importante comprender que Gunicorn **no es un servidor web**.

Gunicorn únicamente ejecuta la aplicación Python.

La comunicación con Internet continúa siendo responsabilidad de Nginx.

---

# ¿Por qué no utilizar "python app.py"?

Durante el desarrollo resulta habitual ejecutar una aplicación Flask mediante:

```bash
python app.py
```

Este mecanismo utiliza el servidor de desarrollo incorporado por Flask.

Aunque resulta muy cómodo para programar, **no fue diseñado para producción**.

Presenta varias limitaciones importantes.

- rendimiento reducido;
- ausencia de gestión avanzada de procesos;
- recuperación limitada frente a errores;
- menor robustez;
- advertencia explícita del propio proyecto Flask indicando que no debe utilizarse en producción.

Por este motivo se decidió utilizar Gunicorn.

---

# Arquitectura

A partir de este punto, la aplicación deja de comunicarse directamente con los clientes.

La arquitectura pasa a ser la siguiente.

```
Internet

↓

Cloudflare

↓

Nginx

↓

Gunicorn

↓

Flask

↓

TBTS
```

Cada componente posee una única responsabilidad.

Esta separación simplifica enormemente la administración del servidor.

---

# Flujo de una petición

Cuando un cliente realiza una solicitud al servicio ocurre el siguiente proceso.

1. El cliente resuelve el nombre del dominio.

2. La petición llega a Cloudflare.

3. Cloudflare la reenvía al VPS.

4. Nginx recibe la conexión.

5. Nginx reenvía la petición hacia Gunicorn.

6. Gunicorn ejecuta Flask.

7. Flask genera la respuesta.

8. La respuesta vuelve siguiendo el camino inverso.

Esta arquitectura permite que cada componente se especialice en una única tarea.

---

# ¿Por qué Gunicorn?

Durante el diseño del proyecto se evaluaron diferentes alternativas.

Entre ellas:

- Gunicorn
- uWSGI
- Waitress
- Hypercorn

Finalmente se eligió Gunicorn debido a:

- simplicidad;
- excelente documentación;
- enorme adopción dentro de la comunidad Python;
- integración perfecta con Flask;
- configuración mínima;
- gran estabilidad.

Para un servicio pequeño como TBTS, Gunicorn ofrece todas las características necesarias sin añadir complejidad innecesaria.

---

# Independencia respecto de Flask

Una de las ventajas más importantes de Gunicorn consiste en desacoplar completamente la aplicación del servidor HTTP.

Flask únicamente implementa la lógica de negocio.

Gunicorn administra:

- procesos;
- workers;
- ejecución de la aplicación;
- manejo de errores.

La aplicación permanece completamente ajena a estos aspectos.

Esto facilita enormemente el mantenimiento.

---

# Número de workers

Gunicorn permite ejecutar múltiples procesos de trabajo (workers).

Cada worker puede atender solicitudes de manera independiente.

TBTS presenta una carga extremadamente reducida.

La API únicamente responde solicitudes muy pequeñas y realiza muy poco procesamiento.

Por este motivo no resulta necesario utilizar un número elevado de workers.

Mantener una configuración sencilla reduce el consumo de memoria y simplifica el diagnóstico de problemas.

En caso de que el tráfico aumente considerablemente en el futuro, esta configuración podrá modificarse sin alterar la aplicación.

---

# Reinicio del servicio

Una ventaja importante de Gunicorn consiste en que puede reiniciarse independientemente del resto de la infraestructura.

Por ejemplo:

- actualizar la aplicación;
- instalar nuevas dependencias;
- modificar variables de entorno.

En todos estos casos únicamente será necesario reiniciar Gunicorn.

Ni Cloudflare ni Nginx requieren modificaciones.

---

# Integración con systemd

Gunicorn no se ejecuta manualmente.

Su ciclo de vida es administrado por **systemd**.

Esto proporciona numerosas ventajas.

- inicio automático al arrancar el servidor;
- reinicio automático ante determinados errores;
- administración uniforme de servicios;
- integración con los registros del sistema.

La configuración completa de systemd será desarrollada en el siguiente capítulo.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS nunca fue necesario modificar la configuración básica de Gunicorn.

La combinación Flask + Gunicorn resultó extremadamente estable desde el primer despliegue.

Las únicas intervenciones posteriores estuvieron relacionadas con la evolución de la propia aplicación y no con el servidor WSGI.

Esta estabilidad confirmó que la elección de Gunicorn fue adecuada para un proyecto de estas características.

---

# Filosofía

Uno de los objetivos principales del proyecto consiste en mantener la infraestructura tan simple como sea posible.

Gunicorn representa perfectamente esta filosofía.

No intenta reemplazar a Nginx.

No administra certificados.

No implementa un firewall.

No realiza funciones que corresponden a otros componentes.

Simplemente ejecuta aplicaciones Python de forma eficiente y estable.

---

# Resumen

Al finalizar este capítulo queda definido el componente responsable de ejecutar la aplicación Flask en producción.

Gunicorn constituye el puente entre la lógica de negocio implementada por TBTS y la infraestructura web proporcionada por Nginx.

En el próximo capítulo se documentará la integración entre Gunicorn y systemd, incluyendo la creación del servicio que permitirá iniciar automáticamente la aplicación al arrancar el servidor.

---

# Capítulo 7 - Systemd: administración del servicio

## Objetivo

Una aplicación destinada a ejecutarse en un entorno de producción no debería iniciarse manualmente desde una terminal.

Debe existir un mecanismo que permita administrar automáticamente su ciclo de vida.

En Linux moderno, esa responsabilidad recae sobre **systemd**.

Este capítulo describe cómo TBTS se integra con systemd y por qué esta integración constituye una pieza fundamental de la infraestructura.

---

# ¿Qué es systemd?

Systemd es el sistema de inicialización y administración de servicios utilizado por Ubuntu.

Su función consiste en controlar procesos que deben permanecer ejecutándose en segundo plano.

Entre otras tareas, systemd permite:

- iniciar servicios automáticamente durante el arranque del sistema;
- detenerlos de forma ordenada;
- reiniciarlos cuando sea necesario;
- consultar su estado;
- acceder a sus registros;
- definir dependencias entre servicios.

Actualmente constituye el estándar de facto en la mayoría de las distribuciones Linux.

---

# ¿Por qué utilizar systemd?

Sin systemd, Gunicorn debería iniciarse manualmente después de cada reinicio del servidor.

Además, si el proceso finalizara inesperadamente, la aplicación dejaría de estar disponible hasta que un administrador la iniciara nuevamente.

Systemd elimina estos problemas.

El servicio pasa a formar parte del propio sistema operativo.

---

# Flujo de funcionamiento

Una vez configurado systemd, el ciclo de vida de la aplicación queda completamente automatizado.

```
Servidor inicia

↓

systemd

↓

Gunicorn

↓

Flask

↓

TBTS disponible
```

La aplicación comienza a ejecutarse sin intervención del administrador.

---

# Ventajas obtenidas

La utilización de systemd aporta numerosas ventajas.

## Inicio automático

Después de un reinicio del VPS, TBTS vuelve a iniciarse automáticamente.

No es necesario ejecutar ningún comando manual.

---

## Administración uniforme

Todos los servicios del servidor utilizan la misma interfaz de administración.

Esto permite consultar fácilmente:

- estado;
- reinicios;
- errores;
- registros.

---

## Integración con journalctl

Los mensajes generados por Gunicorn quedan registrados automáticamente en el journal del sistema.

Esto elimina la necesidad de crear archivos de log específicos para la aplicación.

Toda la información relevante puede consultarse desde un único lugar.

---

## Reinicios controlados

Cuando se despliega una nueva versión de TBTS, únicamente es necesario reiniciar el servicio correspondiente.

No es necesario reiniciar el servidor completo.

Esto reduce considerablemente el tiempo de indisponibilidad.

---

# Configuración utilizada en producción

La infraestructura de TBTS utiliza un servicio dedicado para Gunicorn.

Su configuración sigue la filosofía de mantener todos los parámetros importantes explícitamente definidos.

Entre ellos:

- usuario bajo el cual se ejecuta la aplicación;
- directorio de trabajo;
- entorno virtual;
- comando de inicio;
- política de reinicio;
- integración con journalctl.

Mantener toda esta configuración en un único archivo facilita enormemente el mantenimiento del sistema.

> **Nota:** En una futura revisión de este documento podrá incorporarse el contenido completo del archivo `.service`, comentado línea por línea, ya que constituye la configuración exacta utilizada por el servidor de producción.

---

# Operaciones habituales

Una vez registrado el servicio, la administración diaria resulta muy sencilla.

Las operaciones más habituales son:

- iniciar el servicio;
- detenerlo;
- reiniciarlo;
- consultar su estado;
- habilitar el inicio automático;
- visualizar los registros mediante `journalctl`.

Gracias a systemd, todas estas operaciones siguen una interfaz uniforme compartida por el resto de los servicios del sistema.

---

# Despliegue de nuevas versiones

Cada vez que se publica una nueva versión de TBTS, el procedimiento habitual consiste en:

1. actualizar el repositorio local del servidor;
2. instalar nuevas dependencias si fuera necesario;
3. reiniciar el servicio de Gunicorn.

La aplicación vuelve a quedar disponible pocos segundos después.

Este procedimiento resulta mucho más seguro que ejecutar manualmente la aplicación desde una terminal.

---

# Diagnóstico de problemas

Cuando la aplicación presenta algún inconveniente, systemd constituye el primer lugar donde buscar información.

Los registros permiten identificar rápidamente problemas como:

- errores de sintaxis;
- excepciones durante el arranque;
- dependencias faltantes;
- errores de configuración;
- reinicios inesperados.

Centralizar toda esta información simplifica considerablemente las tareas de diagnóstico.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS fue necesario reiniciar el servicio en numerosas oportunidades para desplegar nuevas versiones.

La utilización de systemd convirtió este proceso en una operación rutinaria, rápida y predecible.

Asimismo, la integración con `journalctl` permitió localizar errores de configuración y problemas de arranque sin necesidad de implementar mecanismos adicionales de registro.

Con el paso del tiempo quedó demostrado que delegar completamente la administración del ciclo de vida de la aplicación en systemd fue una decisión acertada.

---

# Filosofía

Systemd representa uno de los principios fundamentales adoptados durante el desarrollo de TBTS.

Cada componente debe especializarse en una única responsabilidad.

En este caso:

- Flask implementa la lógica del servicio.
- Gunicorn ejecuta la aplicación.
- Systemd administra el proceso.
- Nginx recibe las conexiones HTTP.
- Cloudflare protege la infraestructura expuesta a Internet.

Esta separación hace que el sistema sea más fácil de comprender, mantener y ampliar.

---

# Resumen

Al finalizar este capítulo, TBTS deja de ser una aplicación que debe iniciarse manualmente y pasa a convertirse en un servicio plenamente integrado con el sistema operativo.

Systemd garantiza que la aplicación se inicie automáticamente, facilita su administración diaria y proporciona una plataforma robusta para el despliegue de nuevas versiones.

En el próximo capítulo se incorporará el componente encargado de recibir las conexiones HTTP y HTTPS desde Internet: **Nginx**, el servidor web que actúa como puerta de entrada a toda la infraestructura.

---

# Capítulo 8 - Nginx: la puerta de entrada a la infraestructura

## Objetivo

Hasta este punto, la aplicación TBTS puede ejecutarse correctamente mediante Gunicorn y su ciclo de vida es administrado por systemd.

Sin embargo, Gunicorn no está diseñado para exponerse directamente a Internet.

El componente encargado de recibir todas las conexiones HTTP y HTTPS es **Nginx**.

Este capítulo describe el papel de Nginx dentro de la arquitectura de TBTS, la organización adoptada para los distintos sitios alojados en el servidor y las decisiones de diseño tomadas durante el despliegue.

---

# ¿Qué es Nginx?

Nginx es un servidor web y proxy inverso de alto rendimiento.

Su función consiste en recibir todas las conexiones provenientes de Internet y decidir qué hacer con cada una de ellas.

Dependiendo del dominio solicitado, Nginx puede:

- servir archivos estáticos;
- reenviar peticiones a Gunicorn;
- redireccionar URLs;
- finalizar conexiones HTTPS;
- aplicar reglas de seguridad.

En otras palabras, Nginx constituye la puerta de entrada de toda la infraestructura.

---

# Arquitectura

La arquitectura final del proyecto quedó definida de la siguiente forma.

```
                    Internet
                         │
                         ▼
                   Cloudflare
                         │
                         ▼
                      Nginx
               ┌─────────┴─────────┐
               │                   │
               ▼                   ▼
        Portfolio Web        Gunicorn
                                  │
                                  ▼
                               Flask
                                  │
                                  ▼
                                 TBTS
```

Cada componente posee una única responsabilidad.

Esta separación facilita enormemente el mantenimiento del sistema.

---

# ¿Por qué utilizar Nginx?

Existen numerosos servidores web disponibles para Linux.

Entre ellos:

- Apache HTTP Server
- Caddy
- Lighttpd
- OpenLiteSpeed
- Nginx

Para este proyecto se eligió Nginx por diversas razones.

- excelente rendimiento;
- enorme estabilidad;
- configuración clara;
- amplia documentación;
- integración perfecta con Gunicorn;
- gran adopción dentro del ecosistema Linux.

Para un servidor pequeño como TBTS representa una solución simple y muy robusta.

---

# Dos sitios, un mismo servidor

Uno de los aspectos más interesantes de esta infraestructura consiste en que el VPS aloja dos servicios completamente diferentes.

## Portfolio personal

Disponible mediante:

```
https://coloraturip.com
https://www.coloraturip.com
```

Este sitio está destinado a navegadores modernos.

Utiliza HTTPS y certificados TLS.

---

## TimeBoard Time Service

Disponible mediante:

```
http://tbts.coloraturip.com
```

Este servicio está pensado para clientes extremadamente antiguos, incluyendo dispositivos Palm OS.

Por motivos de compatibilidad, permanece disponible mediante HTTP.

---

# Separación de configuraciones

Durante el desarrollo inicialmente se evaluó mantener ambos sitios dentro de un único archivo de configuración.

Sin embargo, posteriormente se decidió separarlos.

Actualmente existen dos configuraciones independientes.

```
portfolio.conf
```

y

```
tbts.conf
```

Esta decisión aporta varias ventajas.

- cada sitio puede modificarse de forma independiente;
- las configuraciones son más fáciles de comprender;
- futuras ampliaciones resultan más sencillas;
- se reduce el riesgo de introducir errores al modificar un sitio.

Con el paso del tiempo esta decisión demostró ser acertada.

---

# Reverse Proxy

Nginx no ejecuta directamente la aplicación Flask.

Su función consiste en reenviar las solicitudes hacia Gunicorn.

Este mecanismo recibe el nombre de **Reverse Proxy**.

Gracias a esta arquitectura:

- Gunicorn permanece inaccesible desde Internet;
- Flask nunca recibe conexiones directas;
- Nginx puede aplicar reglas antes de reenviar la petición.

Esta separación constituye una práctica estándar para aplicaciones Python en producción.

---

# HTTPS para el portfolio

El sitio principal utiliza HTTPS.

Esto proporciona:

- cifrado;
- autenticidad;
- integridad;
- mejor posicionamiento en buscadores;
- mayor confianza para los visitantes.

Todos los accesos mediante HTTP son redireccionados automáticamente hacia HTTPS.

---

# HTTP para TBTS

Durante el diseño del proyecto surgió una decisión importante.

Los clientes Palm OS poseen limitaciones importantes respecto del soporte TLS moderno.

Después de diversas pruebas se decidió mantener TBTS accesible mediante HTTP.

Esto garantiza la máxima compatibilidad con dispositivos antiguos.

Como medida adicional, el dominio permanece protegido por Cloudflare, ocultando la dirección IP pública del VPS.

Las pruebas realizadas posteriormente demostraron que los dispositivos Palm OS utilizados durante el desarrollo funcionan correctamente incluso con el proxy de Cloudflare habilitado.

---

# Configuración utilizada en producción

La configuración de Nginx sigue una estructura muy sencilla.

Se utilizan dos Virtual Hosts independientes.

## Portfolio

Responsabilidades.

- HTTPS.
- Redirección desde HTTP.
- Certificados TLS.
- Archivos estáticos.

---

## TBTS

Responsabilidades.

- HTTP.
- Reverse Proxy hacia Gunicorn.
- Exposición exclusiva de la API.

Mantener ambas configuraciones separadas facilita enormemente la administración.

> **Nota:** En una futura revisión de este documento se incorporarán los archivos `portfolio.conf` y `tbts.conf` completos, comentados línea por línea, ya que representan exactamente la configuración utilizada en producción.

---

# Experiencia del proyecto

Durante el despliegue inicial ambas configuraciones compartían un mismo archivo.

A medida que el proyecto evolucionó se comprobó que mantener sitios independientes simplificaba considerablemente las modificaciones.

También fue necesario adaptar la configuración para permitir la convivencia entre un sitio HTTPS moderno y una API HTTP destinada a dispositivos Palm OS.

Finalmente, la utilización del proxy de Cloudflare sobre `tbts.coloraturip.com` permitió ocultar la dirección IP pública del servidor sin afectar el funcionamiento de los clientes utilizados durante las pruebas.

---

# Auditoría

Antes de considerar finalizada la configuración de Nginx debería verificarse lo siguiente.

- ✔ `nginx -t` no informa errores.
- ✔ El servicio inicia automáticamente.
- ✔ El portfolio responde mediante HTTPS.
- ✔ `http://coloraturip.com` redirecciona correctamente a HTTPS.
- ✔ `https://www.coloraturip.com` funciona correctamente.
- ✔ `http://tbts.coloraturip.com` responde correctamente.
- ✔ La API devuelve información válida.
- ✔ Gunicorn permanece inaccesible directamente desde Internet.
- ✔ Cloudflare puede comunicarse correctamente con el servidor.

---

# Filosofía

Nginx constituye un excelente ejemplo de uno de los principios fundamentales adoptados durante el desarrollo de TBTS.

Cada componente debe realizar una única tarea.

Nginx recibe conexiones.

Gunicorn ejecuta aplicaciones.

Flask implementa la lógica.

Cloudflare protege el perímetro.

Esta separación hace que la infraestructura resulte sencilla de comprender y extremadamente fácil de mantener.

---

# Resumen

Con la incorporación de Nginx queda completa la infraestructura interna del servidor.

A partir de este momento el VPS dispone de un servidor web profesional capaz de servir el portfolio personal y actuar como proxy inverso para TBTS.

En el próximo capítulo se documentará la integración con Cloudflare, incluyendo DNS, proxy, protección del servidor y las decisiones de diseño adoptadas durante el despliegue.

---

# Capítulo 9 - Cloudflare: DNS, proxy y protección del perímetro

## Objetivo

Hasta este momento toda la infraestructura se encuentra funcionando dentro del VPS.

Sin embargo, exponer directamente un servidor a Internet no constituye la mejor práctica.

Con el objetivo de mejorar la seguridad, simplificar la administración del DNS y añadir una capa adicional de protección, se decidió utilizar Cloudflare como proveedor de DNS autoritativo y proxy inverso.

Este capítulo documenta la configuración adoptada para el proyecto y las decisiones tomadas durante su evolución.

---

# ¿Qué es Cloudflare?

Cloudflare es una plataforma que ofrece múltiples servicios relacionados con Internet.

Entre ellos:

- DNS autoritativo.
- Proxy inverso.
- CDN.
- Protección frente a ataques.
- Certificados TLS.
- Caché.
- Reglas de seguridad.

TBTS únicamente utiliza una parte de estas funcionalidades.

El objetivo principal consiste en proteger el servidor y administrar el DNS del dominio.

---

# Papel dentro de la arquitectura

Cloudflare constituye el primer componente que recibe las conexiones provenientes de Internet.

La arquitectura completa queda de la siguiente forma.

```
Cliente

↓

Cloudflare

↓

VPS

↓

Nginx

↓

Gunicorn

↓

Flask

↓

TBTS
```

El VPS nunca recibe directamente las solicitudes de los clientes cuando el proxy se encuentra habilitado.

---

# Gestión del DNS

Todos los registros DNS del dominio se administran desde Cloudflare.

Esto centraliza completamente la resolución de nombres.

Entre los registros utilizados por el proyecto se encuentran:

- dominio principal (`@`);
- subdominio `www`;
- subdominio `tbts`;
- registros MX;
- SPF;
- DMARC;
- registros utilizados para la emisión de certificados.

Mantener todos los registros en un único proveedor simplifica enormemente la administración.

---

# Configuración utilizada en producción

Actualmente el proyecto utiliza la siguiente organización lógica.

## Portfolio

```
coloraturip.com
www.coloraturip.com
```

Ambos registros utilizan el proxy de Cloudflare.

---

## TBTS

```
tbts.coloraturip.com
```

Después de las pruebas realizadas durante el desarrollo, este subdominio también permanece protegido mediante el proxy de Cloudflare.

Las pruebas realizadas con dispositivos Palm OS demostraron que la API continúa funcionando correctamente utilizando esta configuración.

Esta decisión permite ocultar la dirección IP pública del VPS.

---

# Proxy de Cloudflare

Cuando el proxy se encuentra habilitado:

- los clientes no conocen la dirección IP real del servidor;
- Cloudflare recibe primero todas las conexiones;
- determinadas amenazas pueden mitigarse antes de llegar al VPS;
- resulta posible aprovechar funcionalidades adicionales de seguridad.

Esta capa adicional constituye una mejora importante respecto a exponer directamente el servidor.

---

# Evolución del proyecto

Durante el diseño inicial de la infraestructura se evaluó dejar el subdominio de TBTS utilizando únicamente resolución DNS.

El motivo era maximizar la compatibilidad con clientes muy antiguos.

Posteriormente se realizaron pruebas utilizando dispositivos Palm OS reales y emuladores.

Los resultados demostraron que el servicio continuaba funcionando correctamente incluso con el proxy habilitado.

Como consecuencia, la configuración definitiva mantiene protegido también el subdominio de TBTS.

Esta constituye una de las decisiones arquitectónicas que evolucionó a medida que avanzó el proyecto.

---

# Registros de correo

Aunque TBTS no implementa servicios de correo electrónico, el dominio sí dispone de registros relacionados con email.

Entre ellos:

- MX;
- SPF;
- DMARC.

Estos registros permanecen completamente independientes del funcionamiento de TBTS.

Sin embargo, forman parte de la configuración general del dominio y deben conservarse durante futuras migraciones.

---

# Consideraciones sobre DMARC

Durante el despliegue se adoptó inicialmente una política DMARC de observación.

```
v=DMARC1; p=none;
```

Esta configuración permite supervisar el comportamiento del dominio sin rechazar mensajes legítimos.

Para un dominio recientemente configurado constituye una política prudente y recomendable.

Una vez analizado el comportamiento del correo electrónico podrá evaluarse la adopción de políticas más restrictivas.

---

# Beneficios obtenidos

La incorporación de Cloudflare aportó múltiples ventajas.

- Ocultamiento de la IP pública del VPS.
- Administración centralizada del DNS.
- Mayor facilidad para futuras migraciones.
- Protección adicional frente a tráfico no deseado.
- Integración sencilla con certificados TLS.
- Posibilidad de incorporar nuevas medidas de seguridad sin modificar el servidor.

---

# Experiencia del proyecto

Cloudflare demostró ser una herramienta extremadamente sencilla de administrar.

Uno de los cambios más relevantes ocurrió durante las pruebas de compatibilidad con Palm OS.

Inicialmente se consideró mantener el subdominio `tbts` sin proxy.

Sin embargo, las pruebas realizadas demostraron que el servicio continuaba funcionando correctamente con el proxy activado.

Como resultado, la infraestructura ganó una capa adicional de protección sin afectar la compatibilidad con los clientes utilizados durante el desarrollo.

---

# Auditoría

Antes de considerar finalizada la configuración de Cloudflare debería verificarse lo siguiente.

- ✔ El dominio apunta al VPS correcto.
- ✔ Los registros `@`, `www` y `tbts` resuelven correctamente.
- ✔ El proxy permanece habilitado para los sitios previstos.
- ✔ El portfolio continúa funcionando mediante HTTPS.
- ✔ TBTS responde correctamente mediante HTTP.
- ✔ La dirección IP pública del VPS no queda expuesta a través de los registros protegidos.
- ✔ Los registros MX, SPF y DMARC permanecen configurados correctamente.

---

# Filosofía

Cloudflare representa una decisión coherente con uno de los principios fundamentales del proyecto.

Siempre que resulte posible, conviene añadir capas de protección delante del servidor en lugar de exponer directamente la infraestructura a Internet.

Esta filosofía reduce riesgos y facilita futuras ampliaciones sin necesidad de modificar la aplicación.

---

# Resumen

Con la incorporación de Cloudflare queda definido el perímetro exterior de la infraestructura.

A partir de este punto el dominio dispone de una administración centralizada del DNS, una capa adicional de protección y una arquitectura preparada para evolucionar sin alterar el funcionamiento interno del servidor.

En el próximo capítulo se documentará la emisión y administración de certificados TLS mediante Let's Encrypt, completando la configuración segura del sitio web principal.

---

# Capítulo 10 - Let's Encrypt y certificados TLS

## Objetivo

Una parte fundamental de cualquier sitio web moderno consiste en garantizar que las comunicaciones entre el cliente y el servidor se encuentren cifradas.

Para ello, el proyecto utiliza certificados digitales emitidos por **Let's Encrypt**, administrados mediante **Certbot** e integrados con Nginx.

Este capítulo documenta la estrategia adoptada para la emisión, instalación y renovación de certificados TLS.

---

# ¿Qué es TLS?

TLS (Transport Layer Security) es el protocolo responsable de proteger las comunicaciones entre un cliente y un servidor.

Cuando un navegador accede a un sitio mediante HTTPS:

- la información viaja cifrada;
- se garantiza la identidad del servidor;
- se evita la modificación del contenido durante la transmisión.

Actualmente constituye un requisito indispensable para cualquier sitio web público.

---

# ¿Qué es Let's Encrypt?

Let's Encrypt es una autoridad certificadora (CA) gratuita y ampliamente reconocida.

Permite emitir certificados digitales válidos sin coste económico.

Entre sus principales ventajas se encuentran:

- certificados gratuitos;
- amplia compatibilidad;
- automatización;
- renovación automática;
- enorme adopción en Internet.

Estas características la convirtieron en la opción ideal para este proyecto.

---

# ¿Qué es Certbot?

Certbot es la herramienta encargada de comunicarse con Let's Encrypt.

Sus responsabilidades incluyen:

- solicitar certificados;
- validar la propiedad del dominio;
- instalar certificados en Nginx;
- renovar certificados automáticamente.

De esta manera, la administración de TLS queda prácticamente automatizada.

---

# Papel dentro de la arquitectura

La infraestructura completa queda organizada de la siguiente forma.

```
Cliente

↓

Cloudflare

↓

HTTPS

↓

Nginx

↓

Gunicorn

↓

Flask

↓

TBTS
```

En el caso del portfolio, la conexión HTTPS termina en Nginx.

A partir de ese punto la comunicación continúa internamente dentro del servidor.

---

# Certificados utilizados

El sitio principal dispone de certificados válidos para:

```
coloraturip.com
```

y

```
www.coloraturip.com
```

Ambos nombres se encuentran protegidos mediante el mismo certificado.

---

# ¿Por qué TBTS continúa utilizando HTTP?

Durante el desarrollo del proyecto surgió una decisión importante.

Los clientes previstos para consumir TBTS incluyen dispositivos Palm OS con soporte extremadamente limitado para protocolos criptográficos modernos.

Después de numerosas pruebas se decidió mantener el servicio accesible mediante HTTP.

Esta decisión prioriza la compatibilidad con los dispositivos objetivo.

El portfolio personal, en cambio, utiliza HTTPS para cumplir con los estándares actuales de la Web.

---

# Renovación automática

Una de las principales ventajas de Let's Encrypt consiste en la renovación automática de certificados.

Certbot verifica periódicamente la fecha de vencimiento.

Cuando corresponde, solicita un nuevo certificado sin intervención manual.

Esto reduce considerablemente las tareas de mantenimiento.

---

# Configuración utilizada en producción

La infraestructura utiliza Certbot integrado directamente con Nginx.

El certificado protege:

- coloraturip.com
- www.coloraturip.com

Durante el proceso de emisión, Certbot actualiza automáticamente la configuración correspondiente de Nginx.

Una vez finalizado el procedimiento, el sitio comienza a responder mediante HTTPS utilizando el nuevo certificado.

> **Nota:** En una futura revisión de este documento podrán incorporarse los comandos utilizados para la emisión inicial, la renovación manual y la verificación del estado de los certificados.

---

# Evolución del proyecto

Durante el despliegue inicial fue necesario reorganizar la configuración de Nginx antes de completar correctamente la emisión de certificados.

Inicialmente ambos sitios compartían una única configuración.

Posteriormente se decidió separar completamente el portfolio y TBTS en archivos independientes.

Esta reorganización simplificó notablemente la administración de los certificados y redujo la complejidad de futuras modificaciones.

Con el paso del tiempo, esta decisión demostró ser mucho más mantenible.

---

# Beneficios obtenidos

La incorporación de HTTPS proporciona numerosas ventajas.

- Confidencialidad de la información.
- Integridad de las comunicaciones.
- Autenticidad del servidor.
- Mayor confianza para los visitantes.
- Compatibilidad con navegadores modernos.
- Mejor posicionamiento en buscadores.

Aunque TBTS permanezca accesible mediante HTTP por razones de compatibilidad, el portfolio cumple completamente con las prácticas actuales de seguridad.

---

# Experiencia del proyecto

Una de las decisiones más importantes consistió en separar claramente las necesidades del portfolio y de TBTS.

En lugar de intentar imponer HTTPS a todos los servicios, se optó por analizar los requisitos reales de cada uno.

El resultado fue una infraestructura híbrida.

El sitio web utiliza HTTPS moderno.

La API destinada a Palm OS permanece disponible mediante HTTP.

Ambos servicios conviven en el mismo servidor sin interferir entre sí.

---

# Auditoría

Antes de considerar finalizada la configuración de TLS deberían verificarse los siguientes puntos.

- ✔ `https://coloraturip.com` responde correctamente.
- ✔ `https://www.coloraturip.com` responde correctamente.
- ✔ HTTP redirecciona automáticamente hacia HTTPS.
- ✔ El certificado corresponde al dominio correcto.
- ✔ El certificado no se encuentra próximo a vencer.
- ✔ La renovación automática se encuentra habilitada.
- ✔ `http://tbts.coloraturip.com` continúa funcionando correctamente.

---

# Filosofía

Durante el desarrollo del proyecto se evitó aplicar una solución única para todos los servicios.

Cada componente fue configurado de acuerdo con sus necesidades reales.

El portfolio debía cumplir con los estándares actuales de la Web.

TBTS debía mantener la máxima compatibilidad con dispositivos históricos.

Esta separación permitió satisfacer ambos objetivos sin comprometer la simplicidad de la infraestructura.

---

# Resumen

Con la incorporación de Let's Encrypt queda completada la infraestructura pública del servidor.

El portfolio dispone de comunicaciones cifradas mediante HTTPS, mientras que TBTS conserva la compatibilidad necesaria con los clientes Palm OS.

La combinación de Nginx, Cloudflare y Let's Encrypt proporciona una plataforma segura, moderna y preparada para evolucionar en el futuro.

---

# Capítulo 11 - Operación y mantenimiento

## Objetivo

Una vez desplegada la infraestructura, comienza una nueva etapa en el ciclo de vida del proyecto: la operación diaria.

Este capítulo documenta las tareas habituales de administración del servidor, las verificaciones periódicas recomendadas y el procedimiento general para desplegar nuevas versiones de TBTS.

El objetivo es disponer de una rutina de mantenimiento simple, predecible y fácilmente reproducible.

---

# Filosofía

Durante el desarrollo del proyecto se adoptó una política muy sencilla.

> Una infraestructura estable requiere pocas intervenciones.

El objetivo no consiste en modificar constantemente el servidor, sino en mantenerlo funcionando correctamente con la menor cantidad posible de cambios.

Las actualizaciones deben realizarse únicamente cuando exista un beneficio concreto.

---

# Supervisión del servicio

La primera comprobación habitual consiste en verificar que el servicio permanezca en ejecución.

Para ello debe comprobarse periódicamente el estado de:

- Gunicorn
- Nginx

Si ambos servicios se encuentran activos, la aplicación debería estar disponible para los clientes.

---

# Supervisión de registros

Los registros constituyen la principal fuente de información para detectar problemas.

Durante la operación normal resulta recomendable revisar periódicamente los mensajes registrados por:

- Gunicorn
- Nginx
- systemd

La aparición de errores repetitivos puede indicar un problema antes de que los usuarios lleguen a percibirlo.

---

# Actualización de la aplicación

Cuando se desarrolla una nueva versión de TBTS, el procedimiento de despliegue es deliberadamente simple.

## Paso 1

Actualizar el repositorio local del servidor.

---

## Paso 2

Instalar nuevas dependencias únicamente si la nueva versión las incorpora.

En la mayoría de las actualizaciones este paso no resulta necesario.

---

## Paso 3

Reiniciar el servicio de Gunicorn.

La nueva versión comenzará a atender solicitudes inmediatamente.

---

## Paso 4

Verificar el correcto funcionamiento.

Como mínimo deberían comprobarse:

- la página principal;
- `/api`;
- `/api/health`;
- `/api/v1/utc`.

---

# Actualización del sistema operativo

Periódicamente Ubuntu publica actualizaciones de seguridad y mantenimiento.

Antes de instalarlas se recomienda:

- comprobar el estado actual del servidor;
- disponer de una copia de seguridad reciente;
- revisar los cambios importantes cuando corresponda.

Después de actualizar el sistema operativo conviene verificar nuevamente el funcionamiento completo de la infraestructura.

---

# Certificados

Aunque Certbot renueva automáticamente los certificados TLS, resulta recomendable comprobar periódicamente:

- fecha de vencimiento;
- estado del servicio de renovación;
- funcionamiento del sitio HTTPS.

Detectar un problema con varias semanas de anticipación evita interrupciones innecesarias.

---

# Cloudflare

La configuración DNS cambia muy pocas veces.

Aun así, conviene verificar ocasionalmente que:

- los registros continúan apuntando al VPS correcto;
- el proxy permanece configurado según lo previsto;
- el dominio responde correctamente.

---

# Recursos del servidor

Aunque TBTS consume muy pocos recursos, resulta recomendable supervisar periódicamente:

- utilización de CPU;
- memoria disponible;
- espacio libre en disco;
- carga del sistema.

Estas comprobaciones permiten detectar problemas antes de que afecten al servicio.

---

# Copias de seguridad

Toda infraestructura de producción debería disponer de una estrategia de respaldo.

En el caso de TBTS, los elementos más importantes son:

- código fuente;
- archivos de configuración;
- configuración DNS;
- documentación.

Gracias al uso de Git, una parte importante del proyecto ya dispone de una copia de seguridad externa.

Sin embargo, los archivos específicos del servidor también deberían preservarse.

---

# Procedimiento de mantenimiento

Las intervenciones habituales sobre el servidor deberían seguir siempre el mismo orden.

1. Analizar el cambio a realizar.
2. Crear una copia de seguridad si corresponde.
3. Aplicar la modificación.
4. Reiniciar únicamente los servicios necesarios.
5. Verificar el funcionamiento.
6. Documentar el cambio.

Mantener una metodología consistente reduce considerablemente la probabilidad de errores.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS quedó demostrado que una infraestructura simple también resulta mucho más sencilla de mantener.

La mayoría de las actualizaciones consistieron únicamente en:

- actualizar el repositorio;
- reiniciar Gunicorn;
- verificar los endpoints.

Gracias a la separación entre componentes, muy pocas veces fue necesario modificar Nginx, Cloudflare o la configuración del sistema operativo.

---

# Auditoría

Periódicamente debería comprobarse lo siguiente.

- ✔ Gunicorn se encuentra en ejecución.
- ✔ Nginx se encuentra en ejecución.
- ✔ El portfolio responde correctamente.
- ✔ TBTS responde correctamente.
- ✔ Los certificados HTTPS son válidos.
- ✔ El espacio libre en disco es suficiente.
- ✔ No existen errores relevantes en los registros.
- ✔ El repositorio del servidor coincide con la versión esperada.

---

# Filosofía de mantenimiento

Uno de los principios fundamentales adoptados durante el desarrollo de TBTS consiste en evitar cambios innecesarios.

Un servidor estable no requiere modificaciones constantes.

Cuando una configuración demuestra ser fiable, resulta preferible conservarla antes que incorporar nuevas tecnologías únicamente por seguir tendencias.

La estabilidad constituye un objetivo tan importante como el rendimiento.

---

# Resumen

Con este capítulo concluye la documentación correspondiente a la operación cotidiana del servidor.

La infraestructura ya dispone de procedimientos claros para supervisión, mantenimiento y despliegue de nuevas versiones.

En el próximo capítulo se documentarán los procedimientos de recuperación ante fallos, permitiendo reconstruir completamente el servicio en caso de pérdida del servidor.

---

# Capítulo 12 - Recuperación del servidor (Disaster Recovery)

## Objetivo

Toda infraestructura de producción debería asumir que, tarde o temprano, algún componente fallará.

El objetivo de este capítulo es documentar el procedimiento necesario para reconstruir completamente la infraestructura de TBTS ante la pérdida total del servidor.

La premisa es deliberadamente exigente.

Se asume que el VPS original ha dejado de existir y que únicamente se conservan:

- el repositorio Git;
- el dominio;
- la cuenta de Cloudflare;
- esta documentación.

Si estos elementos se encuentran disponibles, la infraestructura debe poder reconstruirse completamente.

---

# Filosofía

Durante el desarrollo del proyecto se adoptó un principio muy claro.

> Ningún conocimiento crítico debe permanecer únicamente dentro del servidor.

Toda la información necesaria para reconstruir la infraestructura debe encontrarse:

- documentada;
- versionada;
- fácilmente accesible.

Este documento constituye una parte esencial de esa estrategia.

---

# Escenarios de recuperación

No todos los incidentes requieren el mismo procedimiento.

## Recuperación parcial

Ejemplos.

- actualización fallida;
- error de configuración;
- eliminación accidental de un archivo.

En estos casos normalmente basta con restaurar la configuración afectada.

---

## Recuperación completa

Ejemplos.

- pérdida definitiva del VPS;
- corrupción completa del sistema operativo;
- migración hacia un nuevo proveedor.

En estos casos será necesario reconstruir completamente la infraestructura.

Este capítulo se centra principalmente en este segundo escenario.

---

# Recursos necesarios

Para reconstruir el servidor deberían encontrarse disponibles los siguientes elementos.

## Infraestructura

- acceso a Hetzner (o proveedor equivalente);
- dominio registrado;
- cuenta de Cloudflare.

---

## Código fuente

- repositorio GitHub;
- historial completo del proyecto.

---

## Documentación

- este manual;
- archivos de configuración documentados en los apéndices.

---

# Procedimiento general

La recuperación completa debería seguir el siguiente orden.

## Paso 1

Crear un nuevo VPS.

---

## Paso 2

Instalar Ubuntu Server.

---

## Paso 3

Actualizar completamente el sistema operativo.

---

## Paso 4

Repetir la configuración inicial descrita en los primeros capítulos.

---

## Paso 5

Instalar Python.

---

## Paso 6

Clonar el repositorio oficial.

---

## Paso 7

Crear el entorno virtual.

---

## Paso 8

Instalar las dependencias.

---

## Paso 9

Configurar Gunicorn.

---

## Paso 10

Configurar systemd.

---

## Paso 11

Configurar Nginx.

---

## Paso 12

Emitir nuevamente los certificados TLS.

---

## Paso 13

Actualizar los registros DNS si la dirección IP del nuevo VPS fuera diferente.

---

## Paso 14

Verificar el funcionamiento completo.

---

# Elementos persistentes

Uno de los objetivos del proyecto consiste en minimizar la cantidad de información almacenada exclusivamente dentro del servidor.

Los elementos realmente importantes son:

- código fuente;
- configuración;
- documentación.

La aplicación no utiliza una base de datos.

Tampoco almacena información generada por los usuarios.

Como consecuencia, la recuperación resulta considerablemente más sencilla que en otros tipos de aplicaciones.

---

# Tiempo estimado de recuperación

La simplicidad de la infraestructura permite reducir notablemente el tiempo necesario para reconstruir el servicio.

Una vez disponible un nuevo VPS, la mayor parte del trabajo consiste simplemente en repetir los procedimientos documentados en este manual.

Gracias a la utilización de Git, Gunicorn, systemd y Nginx, la reconstrucción completa puede realizarse de forma ordenada y predecible.

---

# Validación posterior

Una vez reconstruido el servidor deberán verificarse todos los componentes.

## Sistema operativo

- actualizado;
- sincronización horaria correcta;
- firewall activo.

---

## Aplicación

- Gunicorn activo;
- systemd funcionando correctamente;
- entorno virtual operativo.

---

## Servidor web

- Nginx activo;
- Virtual Hosts correctos;
- reverse proxy operativo.

---

## Red

- Cloudflare correctamente configurado;
- resolución DNS correcta;
- dominio accesible.

---

## Certificados

- HTTPS operativo para el portfolio;
- renovación automática configurada.

---

## API

Comprobar:

- `/`
- `/api`
- `/api/health`
- `/api/v1/utc`

Todos los endpoints deberían responder correctamente.

---

# Recuperación del código

Gracias a Git, el código fuente nunca depende del servidor.

El procedimiento recomendado consiste siempre en obtener una copia limpia del repositorio.

No resulta recomendable reconstruir manualmente archivos individuales.

Git constituye la fuente oficial del proyecto.

---

# Recuperación de la configuración

Los archivos específicos del servidor deberían reconstruirse utilizando la documentación incluida en este manual.

Entre ellos:

- archivos de Nginx;
- servicio de systemd;
- configuración de Gunicorn;
- configuración DNS.

El objetivo consiste en evitar depender de copias manuales almacenadas únicamente dentro del VPS.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS se procuró evitar cualquier configuración difícil de reproducir.

Cada decisión arquitectónica fue orientada a simplificar una futura reconstrucción del servidor.

La utilización de componentes ampliamente adoptados, junto con una documentación detallada, permite reducir considerablemente el riesgo asociado a la pérdida del entorno de producción.

---

# Auditoría

Una recuperación puede considerarse finalizada cuando se verifican los siguientes puntos.

- ✔ El VPS responde mediante SSH.
- ✔ Gunicorn se encuentra activo.
- ✔ Systemd administra correctamente el servicio.
- ✔ Nginx responde correctamente.
- ✔ El portfolio funciona mediante HTTPS.
- ✔ TBTS responde mediante HTTP.
- ✔ Cloudflare apunta al nuevo servidor.
- ✔ Todos los endpoints de la API responden correctamente.
- ✔ Los certificados TLS son válidos.
- ✔ Los registros del sistema no muestran errores relevantes.

---

# Filosofía

Una infraestructura verdaderamente robusta no es aquella que nunca falla.

Es aquella que puede reconstruirse completamente utilizando procedimientos documentados y reproducibles.

El objetivo final de este proyecto consiste precisamente en eso.

Que el conocimiento permanezca en la documentación y no exclusivamente en la memoria del administrador.

---

# Resumen

Con este capítulo concluye la documentación correspondiente a la infraestructura del servidor.

A partir de este punto existe un procedimiento completo para desplegar, operar, mantener y reconstruir íntegramente el entorno de producción de TBTS.

Los capítulos siguientes dejarán de centrarse en la infraestructura y documentarán el proceso de desarrollo del proyecto y las principales decisiones arquitectónicas que condujeron a su diseño actual.

---

# Capítulo 13 - Ciclo de vida del proyecto

## Objetivo

El desarrollo de una aplicación no finaliza cuando el servidor entra en funcionamiento.

Por el contrario, la infraestructura existe precisamente para facilitar la incorporación de nuevas funcionalidades, la corrección de errores y la evolución continua del proyecto.

Este capítulo documenta el ciclo de vida completo de una modificación en TBTS, desde que surge una nueva idea hasta que la versión correspondiente queda desplegada en producción.

---

# Filosofía

Durante el desarrollo de TBTS se adoptó un principio sencillo.

> Cada cambio debe ser pequeño, verificable y fácilmente reversible.

En lugar de realizar grandes modificaciones simultáneamente, resulta preferible introducir cambios incrementales, comprobando el funcionamiento de la aplicación después de cada etapa.

Esta metodología simplifica el diagnóstico de problemas y reduce considerablemente el riesgo durante los despliegues.

---

# Etapas del ciclo de vida

Cada modificación sigue, en términos generales, el mismo recorrido.

```
Idea

↓

Desarrollo

↓

Pruebas

↓

Commit

↓

Push

↓

Despliegue

↓

Verificación

↓

Producción
```

Esta secuencia constituye el flujo de trabajo habitual del proyecto.

---

# Desarrollo local

Toda nueva funcionalidad comienza en el entorno de desarrollo.

En esta etapa pueden realizarse:

- incorporación de nuevas características;
- corrección de errores;
- refactorización;
- mejoras de rendimiento;
- actualización de documentación.

Ningún cambio debería desplegarse sin haber sido probado previamente.

---

# Pruebas

Antes de considerar finalizada una modificación resulta recomendable comprobar, como mínimo:

- que la aplicación inicia correctamente;
- que los endpoints existentes continúan funcionando;
- que no se introducen regresiones;
- que los registros no muestran errores inesperados.

Aunque TBTS sea un proyecto relativamente pequeño, las pruebas continúan siendo una parte esencial del desarrollo.

---

# Control de versiones

Una vez verificada la modificación, los cambios deben registrarse mediante Git.

El repositorio constituye la fuente oficial del proyecto.

Cada commit representa un punto identificable en la evolución del software.

Gracias al historial de Git resulta posible:

- conocer cuándo se realizó un cambio;
- identificar su autor;
- recuperar versiones anteriores;
- comprender la evolución del proyecto.

---

# Publicación del código

Después de realizar el commit local, los cambios se publican en el repositorio remoto.

De esta forma, GitHub mantiene una copia actualizada del estado del proyecto.

El repositorio remoto constituye además una copia de seguridad del código fuente.

---

# Despliegue

Una vez publicada la nueva versión comienza el despliegue en el servidor.

El procedimiento habitual consiste en:

1. actualizar el repositorio del VPS;
2. instalar nuevas dependencias únicamente si fueran necesarias;
3. reiniciar Gunicorn;
4. comprobar el funcionamiento de la aplicación.

La simplicidad del proceso constituye una de las principales ventajas de la arquitectura adoptada.

---

# Verificación posterior

Después de cada despliegue resulta recomendable comprobar:

- página principal;
- `/api`;
- `/api/health`;
- `/api/v1/utc`.

Asimismo conviene revisar los registros de Gunicorn y Nginx para detectar posibles errores durante el inicio de la nueva versión.

---

# Gestión de dependencias

La incorporación de nuevas bibliotecas debe realizarse con criterio.

Cada dependencia adicional incrementa la complejidad del proyecto.

Siempre que resulte posible debería priorizarse el uso de la biblioteca estándar de Python.

Cuando una dependencia resulte realmente necesaria, deberá incorporarse al archivo `requirements.txt`, permitiendo reproducir exactamente el mismo entorno tanto en desarrollo como en producción.

---

# Actualización de la documentación

Una modificación no finaliza cuando el código funciona correctamente.

También debe evaluarse si el cambio afecta a la documentación del proyecto.

Entre los documentos susceptibles de actualización se encuentran:

- README;
- DEPLOY.md;
- documentación técnica;
- comentarios relevantes dentro del código.

Mantener la documentación sincronizada con el software evita que ambas evolucionen por caminos diferentes.

---

# Corrección de errores

Cuando se detecta un problema en producción, el procedimiento recomendado consiste en:

1. reproducir el error;
2. identificar su causa;
3. implementar la corrección;
4. verificar la solución;
5. desplegar una nueva versión;
6. documentar el incidente cuando corresponda.

Evitar correcciones improvisadas directamente sobre el servidor facilita la trazabilidad del proyecto.

---

# Evolución del proyecto

TBTS nació como un servicio muy pequeño.

Con el tiempo fueron incorporándose nuevas funcionalidades, mejoras en la infraestructura y componentes adicionales.

La utilización de Git permitió que esa evolución quedara registrada de manera cronológica, facilitando comprender cómo y por qué fue creciendo la aplicación.

---

# Experiencia del proyecto

Durante el desarrollo de TBTS quedó demostrado que mantener un flujo de trabajo constante resulta mucho más importante que incorporar herramientas complejas.

La combinación de Git, GitHub, Gunicorn y un procedimiento de despliegue sencillo permitió publicar nuevas versiones con rapidez y con un riesgo muy reducido.

La mayor parte de los despliegues consistió simplemente en actualizar el repositorio, reiniciar el servicio y verificar el funcionamiento de la API.

---

# Auditoría

Antes de considerar finalizado un despliegue deberían verificarse los siguientes puntos.

- ✔ Todos los cambios se encuentran versionados en Git.
- ✔ El repositorio remoto contiene la última versión.
- ✔ El servidor ejecuta el código actualizado.
- ✔ Las dependencias se encuentran sincronizadas.
- ✔ Gunicorn se reinició correctamente.
- ✔ Los endpoints responden según lo esperado.
- ✔ No aparecen errores relevantes en los registros.
- ✔ La documentación permanece actualizada.

---

# Filosofía

El ciclo de vida de un proyecto no termina con el primer despliegue.

Cada nueva funcionalidad recorre el mismo camino desde su concepción hasta su puesta en producción.

Mantener un proceso repetible, documentado y predecible reduce la probabilidad de errores y facilita la evolución del software a largo plazo.

---

# Resumen

Con este capítulo queda documentado el proceso completo mediante el cual evoluciona TBTS.

La combinación de desarrollo local, control de versiones, despliegues controlados y verificación posterior proporciona un flujo de trabajo simple, reproducible y adecuado para un proyecto de estas características.

El próximo capítulo recopilará las principales decisiones arquitectónicas adoptadas durante el desarrollo y las lecciones aprendidas a lo largo del proyecto.

---

# Capítulo 14 - Decisiones arquitectónicas y lecciones aprendidas

## Objetivo

A lo largo del desarrollo de TBTS se tomaron numerosas decisiones técnicas que definieron la arquitectura final del proyecto.

Algunas fueron evidentes desde el comienzo.

Otras surgieron como consecuencia de la experiencia obtenida durante el desarrollo y las pruebas.

Este capítulo recopila las principales decisiones de diseño, sus fundamentos y las lecciones aprendidas durante la construcción de la infraestructura y de la aplicación.

Su objetivo es preservar el razonamiento detrás de la arquitectura para facilitar futuras modificaciones y comprender la evolución del proyecto.

---

# Filosofía general

Desde el inicio del proyecto se adoptó una idea muy simple.

> Elegir la solución más sencilla que resolviera correctamente el problema.

En ningún momento el objetivo fue incorporar tecnologías únicamente por su popularidad.

Cada componente debía justificar su presencia aportando un beneficio concreto.

Esta filosofía permitió construir una infraestructura pequeña, fácil de comprender y sencilla de mantener.

---

# ¿Por qué Python?

Python permitió desarrollar el servicio rápidamente utilizando un lenguaje ampliamente conocido y con un excelente ecosistema de bibliotecas.

Para una API de complejidad reducida, el rendimiento ofrecido por Python resulta más que suficiente.

La prioridad del proyecto nunca fue exprimir el máximo rendimiento posible, sino obtener una solución clara, mantenible y confiable.

---

# ¿Por qué Flask?

Flask fue elegido por su simplicidad.

TBTS expone un conjunto muy reducido de endpoints.

No resultaba necesario utilizar un framework más complejo.

La escasa cantidad de dependencias y la flexibilidad de Flask facilitaron el desarrollo y el mantenimiento de la aplicación.

---

# ¿Por qué Gunicorn?

El servidor de desarrollo incluido en Flask no está diseñado para producción.

Gunicorn proporciona:

- estabilidad;
- gestión de procesos;
- integración con systemd;
- facilidad de configuración.

Su adopción permitió separar claramente el desarrollo del entorno de producción.

---

# ¿Por qué Nginx?

Nginx fue incorporado como servidor web frontal.

Entre sus responsabilidades se encuentran:

- recibir las conexiones HTTP y HTTPS;
- actuar como reverse proxy;
- servir el portfolio;
- redirigir las solicitudes hacia Gunicorn.

Separar estas funciones permitió simplificar la configuración de la aplicación.

---

# ¿Por qué Cloudflare?

Cloudflare aporta dos beneficios principales.

- Administración centralizada del DNS.
- Protección adicional del servidor.

Las pruebas realizadas demostraron que incluso los clientes Palm OS podían comunicarse correctamente con TBTS utilizando el proxy habilitado.

Como consecuencia, el proyecto obtuvo una mejora de seguridad sin sacrificar compatibilidad.

---

# ¿Por qué HTTP para TBTS?

La decisión más particular del proyecto consiste en mantener la API disponible mediante HTTP.

Los clientes previstos incluyen dispositivos Palm OS muy antiguos.

Muchos de ellos presentan limitaciones importantes respecto a protocolos criptográficos modernos.

Mantener HTTP garantiza la compatibilidad con el objetivo principal del proyecto.

El riesgo asociado resulta aceptable debido a la naturaleza de la información transmitida.

TBTS únicamente publica la hora UTC.

No existen usuarios autenticados, información personal ni operaciones sensibles.

---

# ¿Por qué HTTPS para el portfolio?

El portfolio representa la presencia pública del proyecto.

Los navegadores modernos esperan que los sitios web utilicen HTTPS.

Además de proporcionar comunicaciones cifradas, HTTPS incrementa la confianza de los visitantes y evita advertencias de seguridad.

Por este motivo el portfolio utiliza certificados emitidos por Let's Encrypt.

---

# ¿Por qué Git?

Desde el comienzo se decidió que Git fuera la única fuente oficial del código.

Esto proporciona múltiples ventajas.

- Historial completo.
- Recuperación de versiones anteriores.
- Copias de seguridad remotas.
- Trazabilidad de los cambios.

Gracias a esta decisión, el servidor nunca constituye la copia principal del proyecto.

---

# ¿Por qué una infraestructura tan simple?

La aplicación resuelve un problema muy concreto.

Publicar la hora UTC mediante una API extremadamente ligera.

No existen bases de datos.

No existen colas de mensajes.

No existen múltiples microservicios.

No existen procesos distribuidos.

Agregar componentes innecesarios únicamente incrementaría la complejidad sin aportar beneficios reales.

---

# La documentación como parte de la arquitectura

Una de las decisiones menos visibles, pero probablemente más importantes, consistió en documentar exhaustivamente el proyecto.

La documentación no se considera un elemento accesorio.

Forma parte de la arquitectura.

Permite:

- reconstruir el servidor;
- comprender las decisiones adoptadas;
- facilitar futuras modificaciones;
- reducir la dependencia del conocimiento individual.

---

# Lecciones aprendidas

El desarrollo del proyecto permitió confirmar varias ideas importantes.

## La simplicidad suele ser suficiente

Muchas soluciones complejas resultan innecesarias cuando el problema está bien definido.

---

## La documentación tiene un enorme valor

Las decisiones técnicas tienden a olvidarse con el tiempo.

Documentarlas evita repetir análisis ya realizados.

---

## Git simplifica mucho más que el desarrollo

Además de controlar versiones, Git facilita la recuperación del proyecto y actúa como respaldo permanente del código fuente.

---

## La infraestructura debe ser reproducible

Todo el entorno puede reconstruirse siguiendo procedimientos documentados.

Esta característica reduce considerablemente el riesgo operativo.

---

## La compatibilidad también es un requisito

En este proyecto la compatibilidad con Palm OS constituye uno de los objetivos principales.

En consecuencia, algunas decisiones difieren de las que probablemente se adoptarían para una aplicación web convencional.

---

# ¿Qué cambiaría en el futuro?

Toda arquitectura puede evolucionar.

Si en algún momento los requisitos del proyecto cambian, podrían evaluarse mejoras como:

- automatización completa del despliegue;
- integración continua;
- pruebas automatizadas;
- monitorización avanzada;
- métricas de rendimiento.

Sin embargo, ninguna de estas mejoras resulta actualmente imprescindible.

La infraestructura satisface adecuadamente las necesidades del proyecto.

---

# ¿Qué volvería a hacer exactamente igual?

Si el proyecto comenzara nuevamente desde cero, probablemente se repetirían las siguientes decisiones.

- Utilizar Python.
- Utilizar Flask.
- Utilizar Gunicorn.
- Utilizar Nginx.
- Utilizar Git como fuente oficial del proyecto.
- Documentar exhaustivamente toda la infraestructura.
- Mantener la arquitectura sencilla.
- Priorizar la compatibilidad con Palm OS.

Estas decisiones demostraron ser adecuadas durante todo el desarrollo.

---

# Reflexión final

TBTS nació como una herramienta destinada a resolver un problema muy específico.

Con el tiempo terminó convirtiéndose también en un ejercicio completo de diseño de infraestructura, administración de servidores y documentación técnica.

La arquitectura obtenida demuestra que un proyecto pequeño puede beneficiarse de aplicar buenas prácticas de ingeniería sin necesidad de incorporar tecnologías innecesariamente complejas.

---

# Resumen

Las decisiones arquitectónicas documentadas en este capítulo representan la experiencia acumulada durante el desarrollo del proyecto.

Más allá de las tecnologías concretas utilizadas, el principal aprendizaje consiste en que una infraestructura sencilla, bien documentada y completamente reproducible suele proporcionar mejores resultados que una solución excesivamente compleja.

Este documento constituye, por lo tanto, no solo una guía para desplegar TBTS, sino también un registro del razonamiento técnico que permitió construir su arquitectura.

---

# Apéndice A - Inventario del servidor

## Objetivo

Este apéndice documenta el estado del entorno de producción de TimeBoard Time Service en un momento determinado.

Su finalidad es servir como referencia rápida durante tareas de administración, auditoría, mantenimiento o recuperación del servidor.

A diferencia de los capítulos anteriores, este inventario describe el estado real de la infraestructura y deberá actualizarse siempre que exista una modificación significativa en el entorno de producción.

---

# A.1 Identificación del sistema

| Campo | Valor |
|--------|-------|
| Proyecto | TimeBoard Time Service (TBTS) |
| Entorno | Producción |
| Hostname | `coloratura` |
| Proveedor VPS | Hetzner |
| Sistema operativo | Ubuntu Server LTS |
| Lenguaje | Python |
| Framework | Flask |
| Servidor WSGI | Gunicorn |
| Servidor Web | Nginx |
| DNS | Cloudflare |
| Certificados | Let's Encrypt |
| Control de versiones | Git |

---

# A.2 Dominios publicados

| Dominio | Protocolo | Función |
|---------|-----------|---------|
| coloraturip.com | HTTPS | Portfolio |
| www.coloraturip.com | HTTPS | Portfolio |
| tbts.coloraturip.com | HTTP | API TBTS |

---

# A.3 Servicios del sistema

| Servicio | Estado esperado | Función |
|-----------|-----------------|---------|
| nginx | Activo | Servidor Web |
| tbts.service | Activo | Gunicorn / Flask |

---

# A.4 Arquitectura

```
Internet

↓

Cloudflare

↓

Nginx

├── Portfolio

└── TBTS

↓

Gunicorn

↓

Flask

↓

TimeBoard Time Service
```

---

# A.5 Organización del proyecto

Ubicación del proyecto.

```text
/opt/timeboard-time-service
```

La estructura completa del directorio se documenta en el Apéndice B.

---

# A.6 Endpoints

| Endpoint | Función |
|-----------|---------|
| / | Página principal |
| /api | Información de la API |
| /api/health | Estado del servicio |
| /api/v1/utc | Hora UTC |

---

# A.7 Componentes principales

| Componente | Responsabilidad |
|------------|-----------------|
| Cloudflare | DNS y Proxy |
| Nginx | Reverse Proxy |
| Gunicorn | Servidor WSGI |
| Flask | API |
| GitHub | Repositorio oficial |

---

# A.8 Versiones instaladas

Esta sección documenta las versiones existentes en el servidor de producción.

Deberá actualizarse después de cualquier actualización importante.

| Componente | Versión |
|------------|----------|
| Ubuntu Server | *(completar)* |
| Python | *(completar)* |
| Flask | *(completar)* |
| Gunicorn | *(completar)* |
| Nginx | *(completar)* |
| Git | *(completar)* |
| Certbot | *(completar)* |

---

# A.9 Estado esperado

Una instalación correctamente configurada deberá cumplir todas las condiciones siguientes.

- Gunicorn activo.
- Nginx activo.
- Cloudflare correctamente configurado.
- Certificados HTTPS válidos.
- Portfolio accesible.
- API accesible.
- Todos los endpoints responden correctamente.
- Sin errores relevantes en los registros.

---

# A.10 Historial del inventario

| Fecha | Versión | Observaciones |
|--------|----------|---------------|
| 2026 | 1.0 | Inventario inicial del servidor |

---

# Resumen

Este inventario constituye la referencia oficial del entorno de producción.

Su objetivo consiste en proporcionar una visión rápida y precisa de la infraestructura, facilitando tareas de administración, mantenimiento y recuperación del sistema.

---

# Apéndice B - Configuración completa

## Objetivo

Este apéndice reúne los principales archivos de configuración utilizados por la infraestructura de producción.

A diferencia del resto del documento, aquí se documentan las configuraciones reales del servidor.

Siempre que sea posible deberán incluirse exactamente los archivos utilizados en producción, evitando ejemplos simplificados o configuraciones genéricas.

Este apéndice constituye la referencia oficial para reconstruir la infraestructura.

---

# Organización

Cada configuración se presenta siguiendo la misma estructura.

- Propósito.
- Ubicación.
- Archivo completo.
- Explicación.
- Observaciones.

De esta manera resulta sencillo localizar cualquier componente de la infraestructura.

---

# B.1 Árbol del proyecto

## Ubicación

```
/opt/timeboard-time-service
```

## Contenido

> **Completar con la salida real del comando:**

```bash
tree /opt/timeboard-time-service
```

Este árbol documenta la organización completa del proyecto en producción.

---

# B.2 requirements.txt

## Ubicación

```
/opt/timeboard-time-service/requirements.txt
```

## Archivo

```text
(Pegar aquí el archivo real)
```

## Explicación

Cada dependencia debería documentarse brevemente.

Por ejemplo.

| Dependencia | Motivo |
|-------------|--------|
| Flask | Framework web |
| Gunicorn | Servidor WSGI |
| Flask-Limiter | Protección contra abuso |

Esta sección facilita comprender por qué existe cada biblioteca instalada.

---

# B.3 Servicio systemd

## Ubicación

```
/etc/systemd/system/tbts.service
```

## Archivo

```ini
(Pegar aquí el archivo real)
```

## Explicación

Documentar:

- usuario utilizado;
- directorio de trabajo;
- entorno virtual;
- comando de inicio;
- reinicio automático;
- integración con journalctl.

---

# B.4 Configuración de Gunicorn

Si Gunicorn utiliza parámetros adicionales o scripts específicos, documentarlos aquí.

En caso contrario indicar expresamente que la configuración se encuentra definida directamente desde systemd.

---

# B.5 portfolio.conf

## Ubicación

```
/etc/nginx/sites-available/portfolio.conf
```

## Archivo

```nginx
verla: sudo nginx -T
comprobar: sudo nginx -t
```

## Explicación

Describir:

- Server Name.
- HTTPS.
- Certificados.
- Root.
- Archivos estáticos.
- Redirecciones.
- Logging.

---

# B.6 tbts.conf

## Ubicación

```
/etc/nginx/sites-available/tbts.conf
```

## Archivo

```nginx
(Pegar aquí la configuración real)
```

## Explicación

Documentar especialmente.

- reverse proxy;
- proxy_pass;
- cabeceras;
- compatibilidad con Palm OS.

---

# B.7 Enlaces simbólicos

Documentar la salida de.

```bash
ls -l /etc/nginx/sites-enabled
```

Esto permite verificar rápidamente qué sitios se encuentran habilitados.

---

# B.8 Certificados

Documentar.

- dominios protegidos;
- ubicación de certificados;
- método de renovación.

No resulta necesario copiar los certificados.

Únicamente documentar su ubicación.

---

# B.9 Variables de entorno

Si en el futuro el proyecto incorpora variables de entorno, documentarlas aquí.

Actualmente indicar expresamente que la aplicación no depende de variables externas.

---

# B.10 DNS

Documentar todos los registros existentes.

Por ejemplo.

| Tipo | Nombre | Destino | Proxy |
|------|---------|----------|-------|
| A | @ | ... | Sí |
| A | www | ... | Sí |
| A | tbts | ... | Sí |

Esta sección debería reflejar exactamente la configuración existente en Cloudflare.

---

# B.11 Estado de los servicios

Incluir la salida real de.

```bash
systemctl status tbts
```

y

```bash
systemctl status nginx
```

Esto facilita comparar rápidamente el comportamiento esperado con el estado del servidor.

---

# B.12 Verificación de Nginx

Documentar la salida de.

```bash
nginx -t
```

Una verificación exitosa constituye una referencia útil durante futuras modificaciones.

---

# B.13 Versiones instaladas

Documentar la salida de comandos como.

```bash
python --version
```

```bash
pip freeze
```

```bash
nginx -v
```

```bash
gunicorn --version
```

Esto permite reproducir con precisión el entorno original.

---

# B.14 Observaciones

Toda modificación importante en la configuración del servidor debería reflejarse en este apéndice.

Mantener esta información sincronizada con el entorno de producción resulta esencial para preservar la utilidad del documento.

---

# Resumen

Este apéndice reúne las configuraciones reales utilizadas por la infraestructura de producción.

Constituye la referencia principal para reconstruir el servidor, verificar su estado o auditar cualquier componente de la plataforma.

---

# Apéndice C - Runbook de operación

## Objetivo

Este apéndice reúne los comandos y procedimientos habituales para administrar el servidor de producción de TimeBoard Time Service.

Su finalidad consiste en disponer de una referencia rápida para realizar tareas de operación, mantenimiento y diagnóstico, evitando la necesidad de recordar comandos o consultar documentación externa.

Todos los procedimientos aquí documentados corresponden al entorno de producción.

---

# C.1 Estado general del sistema

## Verificar el estado del servicio

```bash
sudo systemctl status tbts
```

Permite comprobar si Gunicorn se encuentra ejecutándose correctamente.

---

## Verificar el estado de Nginx

```bash
sudo systemctl status nginx
```

Comprueba el estado del servidor web.

---

## Verificar ambos servicios

```bash
sudo systemctl status tbts nginx
```

---

# C.2 Gestión de servicios

## Reiniciar TBTS

```bash
sudo systemctl restart tbts
```

Debe utilizarse después de actualizar el código o modificar la configuración del servicio.

---

## Detener TBTS

```bash
sudo systemctl stop tbts
```

---

## Iniciar TBTS

```bash
sudo systemctl start tbts
```

---

## Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

---

## Recargar configuración de Nginx

```bash
sudo systemctl reload nginx
```

Recarga la configuración sin interrumpir las conexiones existentes.

---

# C.3 Visualización de registros

## Registros del servicio

```bash
journalctl -u tbts
```

---

## Seguir registros en tiempo real

```bash
journalctl -u tbts -f
```

---

## Registros recientes

```bash
journalctl -u tbts --since "1 hour ago"
```

---

## Registros de Nginx

```bash
sudo tail -f /var/log/nginx/access.log
```

```bash
sudo tail -f /var/log/nginx/error.log
```

---

# C.4 Despliegue de una nueva versión

## Acceder al proyecto

```bash
cd /opt/timeboard-time-service
```

---

## Obtener la última versión

```bash
git pull
```

---

## Actualizar dependencias

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Reiniciar la aplicación

```bash
sudo systemctl restart tbts
```

---

## Verificar funcionamiento

```bash
curl http://tbts.coloraturip.com/api/health
```

Confirmar que la respuesta sea correcta antes de dar por finalizado el despliegue.

---

# C.5 Verificación de Nginx

## Comprobar sintaxis

```bash
sudo nginx -t
```

Siempre debe ejecutarse antes de reiniciar Nginx tras modificar su configuración.

---

## Recargar configuración

```bash
sudo systemctl reload nginx
```

---

# C.6 Certificados HTTPS

## Mostrar certificados instalados

```bash
sudo certbot certificates
```

---

## Renovación manual

```bash
sudo certbot renew
```

---

## Simulación de renovación

```bash
sudo certbot renew --dry-run
```

Permite verificar el correcto funcionamiento de la renovación automática.

---

# C.7 Monitorización del servidor

## Espacio disponible

```bash
df -h
```

---

## Uso de memoria

```bash
free -h
```

---

## Procesos activos

```bash
htop
```

---

## Carga del sistema

```bash
uptime
```

---

## Información del sistema

```bash
hostnamectl
```

---

# C.8 Red

## Ver puertos en escucha

```bash
sudo ss -tulpn
```

---

## Comprobar conectividad

```bash
ping tbts.coloraturip.com
```

---

## Probar la API

```bash
curl http://tbts.coloraturip.com/api/v1/utc
```

---

# C.9 Git

## Estado del repositorio

```bash
git status
```

---

## Historial reciente

```bash
git log --oneline --decorate -10
```

---

## Rama actual

```bash
git branch
```

---

# C.10 Actualización del sistema

## Actualizar índices

```bash
sudo apt update
```

---

## Instalar actualizaciones

```bash
sudo apt upgrade
```

---

## Actualización completa

```bash
sudo apt full-upgrade
```

---

# C.11 Procedimiento recomendado de despliegue

El siguiente procedimiento resume el flujo recomendado para publicar una nueva versión del servicio.

1. Verificar el estado actual del servidor.
2. Obtener la última versión desde GitHub.
3. Actualizar dependencias si corresponde.
4. Reiniciar el servicio TBTS.
5. Verificar que Gunicorn se encuentre activo.
6. Comprobar la sintaxis de Nginx.
7. Recargar Nginx si hubo cambios en la configuración.
8. Verificar el endpoint `/api/health`.
9. Revisar los registros del servicio.
10. Confirmar el correcto funcionamiento de la aplicación.

---

# C.12 Diagnóstico rápido

| Problema | Acción recomendada |
|----------|--------------------|
| La API no responde | Verificar `tbts.service` |
| Error 502 | Comprobar Gunicorn |
| Error 404 | Revisar `tbts.conf` |
| Error de configuración | Ejecutar `nginx -t` |
| Error de despliegue | Revisar `journalctl -u tbts` |
| Problemas de DNS | Verificar Cloudflare |
| Certificados vencidos | Ejecutar `certbot certificates` |

---

# C.13 Lista de comprobación posterior a un despliegue

Después de cada despliegue deberían verificarse los siguientes puntos.

- La aplicación inicia correctamente.
- Gunicorn permanece activo.
- Nginx responde sin errores.
- `/api/health` devuelve un estado correcto.
- `/api/v1/utc` responde correctamente.
- No existen errores en los registros.
- Cloudflare continúa resolviendo correctamente los dominios.

---

# Resumen

Este runbook constituye la referencia operativa oficial para la administración del servidor de producción.

Su objetivo es estandarizar las tareas de mantenimiento y proporcionar un conjunto único de procedimientos para operar la infraestructura de forma segura y consistente.

---

# Apéndice D - Cronología del proyecto

## Objetivo

Este apéndice documenta la evolución técnica de TimeBoard Time Service desde su concepción hasta la versión actual de la infraestructura.

Su finalidad consiste en registrar las principales decisiones arquitectónicas, facilitando la comprensión del crecimiento del proyecto y el contexto en el que fueron adoptadas determinadas soluciones.

---

# Línea temporal

## Fase 1 - Concepción

- Definición del objetivo del proyecto.
- Diseño de una API para obtener la hora UTC.
- Compatibilidad como requisito principal.

---

## Fase 2 - Desarrollo inicial

- Desarrollo en Python.
- Adopción de Flask.
- Primeros endpoints.

---

## Fase 3 - Infraestructura

- Contratación del VPS.
- Instalación de Ubuntu.
- Configuración del entorno Python.

---

## Fase 4 - Producción

- Incorporación de Gunicorn.
- Configuración de systemd.
- Configuración de Nginx.

---

## Fase 5 - Publicación

- Registro del dominio.
- Configuración de Cloudflare.
- Obtención de certificados HTTPS.

---

## Fase 6 - Endurecimiento

- Incorporación de Flask-Limiter.
- Separación entre Portfolio y TBTS.
- Protección mediante Cloudflare.

---

## Fase 7 - Documentación

- Elaboración del manual técnico.
- Inventario del servidor.
- Runbook.
- Procedimientos de recuperación.

---

# Estado actual

La infraestructura se considera estable y preparada para futuras ampliaciones sin necesidad de modificar su arquitectura principal.

---

# Resumen

La evolución del proyecto refleja un crecimiento gradual basado en decisiones técnicas simples, priorizando siempre la mantenibilidad, la compatibilidad y la reproducibilidad.

---

# Apéndice E - Glosario

## Objetivo

Este glosario reúne los principales términos técnicos utilizados a lo largo del presente documento.

Su finalidad consiste en facilitar la lectura del manual, proporcionando definiciones breves de los conceptos empleados durante el diseño, despliegue y operación de la infraestructura.

Las definiciones incluidas no pretenden ser exhaustivas, sino ofrecer el contexto necesario para comprender la arquitectura de TimeBoard Time Service.

---

# Términos

| Término | Definición |
|----------|------------|
| API | Interfaz que permite la comunicación entre aplicaciones mediante solicitudes y respuestas estructuradas. |
| Cloudflare | Plataforma utilizada para administrar el DNS del dominio y actuar como proxy inverso, proporcionando protección y optimización del tráfico. |
| Certbot | Herramienta utilizada para solicitar, instalar y renovar automáticamente certificados TLS emitidos por Let's Encrypt. |
| DNS | Sistema encargado de traducir nombres de dominio, como `tbts.coloraturip.com`, en direcciones IP. |
| Endpoint | Dirección específica de una API a la que los clientes envían solicitudes para obtener un recurso o ejecutar una operación. |
| Flask | Framework web desarrollado en Python utilizado para implementar la API de TimeBoard Time Service. |
| Flask-Limiter | Biblioteca utilizada para limitar la cantidad de solicitudes que un cliente puede realizar en un determinado período de tiempo. |
| Git | Sistema distribuido de control de versiones utilizado para gestionar el código fuente del proyecto. |
| GitHub | Plataforma donde se aloja el repositorio oficial del proyecto y su historial de cambios. |
| Gunicorn | Servidor WSGI encargado de ejecutar la aplicación Flask en producción. |
| HTTP | Protocolo de comunicación utilizado por TBTS para mantener compatibilidad con clientes Palm OS. |
| HTTPS | Versión segura de HTTP que incorpora cifrado mediante TLS. Utilizada por el portfolio del proyecto. |
| Hostname | Nombre asignado al servidor dentro de la red. En este proyecto corresponde a `coloratura`. |
| Let's Encrypt | Autoridad certificadora que emite gratuitamente los certificados TLS utilizados por el portfolio. |
| Nginx | Servidor web y reverse proxy responsable de recibir las conexiones externas y reenviarlas a Gunicorn cuando corresponde. |
| Palm OS | Sistema operativo para dispositivos PDA con el que TimeBoard mantiene compatibilidad. |
| Proxy | Servidor intermediario que recibe solicitudes de un cliente y las reenvía hacia otro servidor. |
| Reverse Proxy | Tipo de proxy que recibe solicitudes desde Internet y las distribuye hacia uno o varios servicios internos. En este proyecto esta función es realizada por Nginx. |
| Repository (Repositorio) | Directorio gestionado por Git que contiene el código fuente y el historial completo del proyecto. |
| REST | Estilo arquitectónico utilizado para diseñar APIs basadas en recursos accesibles mediante HTTP. |
| systemd | Sistema de inicialización y administración de servicios utilizado por Ubuntu para controlar la ejecución de Gunicorn. |
| TLS | Protocolo criptográfico que protege las comunicaciones realizadas mediante HTTPS. |
| Ubuntu Server | Distribución de Linux utilizada como sistema operativo del servidor de producción. |
| UTC | Tiempo Universal Coordinado. Es la referencia horaria publicada por TimeBoard Time Service. |
| Virtual Host | Configuración de Nginx que permite servir distintos sitios o aplicaciones desde un mismo servidor utilizando diferentes dominios o subdominios. |
| VPS | Servidor Privado Virtual. Máquina virtual utilizada para alojar la infraestructura del proyecto. |
| WSGI | Especificación que define la comunicación entre aplicaciones web escritas en Python y los servidores que las ejecutan. |

---

# Acrónimos

| Acrónimo | Significado |
|-----------|-------------|
| API | Application Programming Interface |
| DNS | Domain Name System |
| HTTP | Hypertext Transfer Protocol |
| HTTPS | Hypertext Transfer Protocol Secure |
| REST | Representational State Transfer |
| TLS | Transport Layer Security |
| UTC | Coordinated Universal Time |
| VPS | Virtual Private Server |
| WSGI | Web Server Gateway Interface |

---

# Convenciones utilizadas en este documento

A lo largo del manual se utilizan las siguientes convenciones tipográficas.

| Formato | Significado |
|----------|-------------|
| `comando` | Comandos que deben ejecutarse en una terminal. |
| `archivo.conf` | Archivos de configuración o nombres de archivos. |
| `/ruta/del/sistema` | Directorios o rutas del sistema de archivos. |
| `https://ejemplo.com` | Direcciones web o endpoints. |
| **Negrita** | Conceptos importantes o elementos que requieren especial atención. |

---

# Resumen

Este glosario proporciona una referencia rápida de los conceptos fundamentales utilizados en el manual.

Su objetivo es facilitar la comprensión de la documentación, unificando la terminología empleada y evitando ambigüedades durante la administración y el mantenimiento de la infraestructura.

---

# Apéndice F - Cronología del proyecto

## Objetivo

Este apéndice documenta la evolución de TimeBoard Time Service desde su concepción hasta la versión actual de la infraestructura.

Su propósito consiste en registrar las principales decisiones técnicas y arquitectónicas adoptadas durante el desarrollo del proyecto, preservando el contexto en el que fueron tomadas y facilitando la comprensión de la evolución del sistema.

La cronología no pretende registrar cada cambio realizado, sino únicamente aquellos hitos que modificaron de forma significativa la arquitectura, la infraestructura o la organización del proyecto.

---

# Fase 1 - Idea inicial

El proyecto nació con el objetivo de proporcionar una fuente de hora UTC para dispositivos Palm OS.

Desde el comienzo se establecieron dos requisitos fundamentales.

- Compatibilidad con dispositivos antiguos.
- Infraestructura sencilla y fácilmente mantenible.

Estos principios guiaron todas las decisiones posteriores.

---

# Fase 2 - Desarrollo de la API

Se seleccionó Python como lenguaje de programación debido a su simplicidad y amplio ecosistema.

Para implementar la API se adoptó Flask, ya que el reducido número de endpoints no justificaba el uso de un framework de mayor complejidad.

Durante esta etapa se desarrollaron los primeros endpoints y se realizaron las pruebas iniciales de funcionamiento.

---

# Fase 3 - Preparación del entorno de producción

Con la aplicación funcionando correctamente, se contrató un VPS y se instaló Ubuntu Server LTS como sistema operativo.

También se preparó el entorno Python y se organizó el proyecto dentro del servidor.

En esta etapa la prioridad consistió en obtener una plataforma estable para alojar la aplicación.

---

# Fase 4 - Publicación del servicio

La aplicación dejó de utilizar el servidor de desarrollo de Flask y comenzó a ejecutarse mediante Gunicorn.

Posteriormente se incorporó Nginx como servidor web y reverse proxy.

La utilización de systemd permitió automatizar el inicio del servicio y garantizar su reinicio en caso de fallos.

Con esta etapa quedó definida la arquitectura básica del entorno de producción.

---

# Fase 5 - Presencia pública

Se registró el dominio principal y se configuró Cloudflare como proveedor de DNS.

También se publicó el portfolio personal utilizando HTTPS mediante certificados emitidos por Let's Encrypt.

El servicio TBTS, en cambio, permaneció utilizando HTTP para preservar la compatibilidad con clientes Palm OS.

---

# Fase 6 - Fortalecimiento de la infraestructura

Con el entorno funcionando de manera estable se incorporaron mejoras destinadas a incrementar la robustez del sistema.

Entre ellas.

- Separación entre el portfolio y TBTS mediante Virtual Hosts independientes.
- Protección mediante Flask-Limiter.
- Habilitación del proxy de Cloudflare.
- Organización definitiva de la infraestructura.

Estas modificaciones mejoraron la seguridad sin incrementar innecesariamente la complejidad del proyecto.

---

# Fase 7 - Documentación técnica

Una vez estabilizada la infraestructura se inició la elaboración de la documentación completa del proyecto.

Además de describir el procedimiento de despliegue, el manual pasó a documentar.

- La arquitectura.
- Las decisiones de diseño.
- La operación diaria.
- La recuperación ante desastres.
- El inventario del servidor.
- Las configuraciones de producción.
- El runbook operativo.

La documentación pasó a formar parte de la propia arquitectura del proyecto.

---

# Estado actual

En la actualidad TimeBoard Time Service dispone de una infraestructura estable, documentada y completamente reproducible.

La arquitectura responde adecuadamente a los objetivos iniciales del proyecto.

- Compatibilidad con Palm OS.
- Simplicidad.
- Facilidad de mantenimiento.
- Recuperación documentada.
- Bajo costo operativo.

---

# Próximas posibilidades de evolución

Si en el futuro los requisitos del proyecto cambian, podrían incorporarse nuevas capacidades sin modificar los principios fundamentales de la arquitectura.

Entre ellas.

- Integración continua (CI).
- Despliegue automatizado.
- Monitorización avanzada.
- Métricas de rendimiento.
- Nuevos endpoints.
- Nuevas versiones de TimeBoard.

La incorporación de estas mejoras deberá evaluarse únicamente cuando exista una necesidad concreta que las justifique.

---

# Línea temporal resumida

| Etapa | Hito |
|--------|------|
| 1 | Definición del proyecto |
| 2 | Desarrollo de la API con Flask |
| 3 | Contratación del VPS |
| 4 | Gunicorn + systemd + Nginx |
| 5 | Dominio, Cloudflare y HTTPS |
| 6 | Hardening de la infraestructura |
| 7 | Documentación técnica completa |

---

# Lecciones de la evolución

La experiencia adquirida durante el desarrollo permitió confirmar varias ideas fundamentales.

- Una arquitectura sencilla puede ser suficiente para resolver problemas reales.
- La documentación reduce significativamente el costo de mantenimiento.
- Git constituye la fuente oficial del proyecto y simplifica la recuperación ante desastres.
- La compatibilidad con el objetivo del proyecto debe prevalecer sobre la adopción de tecnologías más modernas cuando estas no aportan un beneficio real.
- La infraestructura debe evolucionar únicamente cuando exista una necesidad claramente identificada.

---

# Resumen

La evolución de TimeBoard Time Service refleja un crecimiento progresivo basado en decisiones técnicas cuidadosamente fundamentadas.

Cada etapa del proyecto incorporó únicamente los componentes necesarios para resolver los requisitos existentes en ese momento, preservando siempre los principios de simplicidad, compatibilidad y mantenibilidad que guiaron el diseño desde sus comienzos.

Este apéndice constituye el registro histórico de dicha evolución y complementa el resto de la documentación técnica del proyecto.
