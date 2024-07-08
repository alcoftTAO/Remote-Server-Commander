# Alcoft Remote Server Commander
Este es un software que te permite ejecutar algunos comandos root en un servidor remoto, pero sin tener acceso completo al usuario root del servidor.

## Cómo utilizarlo
### Instalar dependencias
En primer lugar, debes de instalar las dependencias, tanto para el cliente como para el servidor.
Si no tienes acceso al servidor es posible que tengas que contactar con el responsable del servidor para iniciar y configurar el programa.

#### Instalar dependencias en Windows
1. Asegúrate de tener Python y Git instalados en tú sistema (se recomienda Python 3.12).
2. Abre Microsoft PowerShell.
3. Haz `cd` en el directorio donde deseas descargar este repositorio.
4. Ejecuta:
```sh
git clone https://github.com/alcoftTAO/Remote-Server-Commander.git
cd Remote-Server-Commander
```

5. Descargua PIP para Python ejecutando:
```sh
python -m ensurepip
```

6. Instala los requisitos de Python ejecutando:
```sh
python -m pip install -r requirements.txt
```

7. ¡Listo! Ya instalaste los requisitos.

#### Instalar dependencias en GNU/Linux
1. Asegúrate de tener Python y Git instalados en tú sistema (se recomienda Python 3.12).
2. Abre tu terminal favorita.
3. Haz `cd` en el directorio donde deseas descargar este repositorio.
4. Ejecuta:
```sh
git clone https://github.com/alcoftTAO/Remote-Server-Commander.git
cd Remote-Server-Commander
```

5. Asegúrate de tener PIP instalado. Si no lo tienes, instálalo usando el gestor de paquetes de tu sistema.
6. Instala los requisitos de Python ejecutando:
```sh
pip install -r requirements.txt
```

7. ¡Listo! Ya instalaste los requisitos.

> [!NOTE]
> Si ejecutas un comando `python [···]` y no funciona, intenta ejecutar `python3 [···]` o `py [···]`.

### Configurar el servidor
Debes ejecutar el script `Server.py` en tú servidor con acceso root.
Si deseas que el servidor inicie automáticamente el script, puedes usar `systemd`:
1. Crea un servicio de systemd:
```sh
sudo vim /etc/systemd/system/rsc.service
```

> [!NOTE]
> Reemplaza `vim` con cualquier otro editor de texto que desees.

2. Escribe esto en el nuevo archivo:
```
[Unit]
Description=Remote Server Commander
After=network-online.target ufw.service

[Service]
Type=simple
WorkingDirectory=[DIR]
ExecStart=python Server.py [ARGS]

[Install]
WantedBy=multi-user.target
```

> [!NOTE]
> Reemplaza `[DIR]` con el directorio del repositorio.
> Reemplaza `[ARGS]` con los argumentos del servidor. Si no conoces los argumentos, ingresa al directorio del repositorio y ejecuta `python Server.py help`.
> Si no tienes `ufw` como firewall de tú servidor, elimina `ufw.service`.

3. Habilita el servicio:
```sh
sudo systemctl daemon-reload
sudo systemctl enable rsc.service
```

4. Inicia el servicio:
```sh
sudo systemctl start rsc.service
```

5. ¡Listo!

### Conéctate a un servidor usando el cliente
Hay dos formas de conectarse para ejecutar un comando en el servidor utilizando el cliente.
1. Conexión única:
Esta conexión solo puede ejecutar 1 comando, pero podría ser más rápida.
Para utilizar esta conexión, ejecuta:
```sh
python Client.py ip=[IP] pwd=[CONTRASEÑA] cmd=[COMANDO]
```

> [!NOTE]
> Reemplaza `[IP]` con la IP del servidor.
> Reemplaza `[CONTRASEÑA]` con la contraseña del servidor.
> Reemplaza `[COMANDO]` con el comando que deseas ejecutar en el servidor. Asegúrate de que sea un comando válido.

2. Conexión con terminal:
Esta conexión crea una "terminal", donde puedes escribir tantos comandos como quieras.
Para utilizar esta conexión, ejecuta:
```sh
python Client.py ip=[IP] pwd=[CONTRASEÑA] term
```

> [!NOTE]
> Reemplaza `[IP]` con la IP del servidor.
> Reemplaza `[CONTRASEÑA]` con la contraseña del servidor.
> Cuando hayas terminado de ejecutar comandos, escribe `exit` en la terminal para cerrar el programa.

## Licencia
Licencia MIT.
