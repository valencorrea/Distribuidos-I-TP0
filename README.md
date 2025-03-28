# TP0: Docker + Comunicaciones + Concurrencia

## Parte 2: Repaso de Comunicaciones

### Ejercicio N°7:
Las secciones de repaso del trabajo práctico plantean un caso de uso denominado Lotería Nacional. 
Para la resolución de las mismas deberá utilizarse como base el código fuente provisto en la primera parte, con las modificaciones agregadas en el ejercicio 4.

#### Requerimientos:
Modificar los clientes para que notifiquen al servidor al finalizar con el envío de todas las apuestas y así proceder con el sorteo. Inmediatamente después de la notificacion, los clientes consultarán la lista de ganadores del sorteo correspondientes a su agencia. Una vez el cliente obtenga los resultados, deberá imprimir por log: action: consulta_ganadores | result: success | cant_ganadores: ${CANT}.

El servidor deberá esperar la notificación de las 5 agencias para considerar que se realizó el sorteo e imprimir por log: action: sorteo | result: success. Luego de este evento, podrá verificar cada apuesta con las funciones load_bets(...) y has_won(...) y retornar los DNI de los ganadores de la agencia en cuestión. Antes del sorteo no se podrán responder consultas por la lista de ganadores con información parcial.

Las funciones load_bets(...) y has_won(...) son provistas por la cátedra y no podrán ser modificadas por el alumno.

No es correcto realizar un broadcast de todos los ganadores hacia todas las agencias, se espera que se informen los DNIs ganadores que correspondan a cada una de ellas.


#### Solucion:
El cliente avisa al server la finalizacion con 'F;n' con n nombre agencia. Dado que el cliente conoce la cantidad de clientes que tiene conectados, una vez que todos le avisaron que finalizaron sus apuestas, las procesa y evalua quienes fueron los ganadores. Previamente el server se guarda el socket de cada agencia, para cuando itere sobre las apuestas buscando ganadores, obtener los documentos asociados a cada una y enviarlos. El procolo definido para esta situacion es W;documento1;documento2;... . El cliente es capaz de interpretar este mensaje y dar aviso de los ganadores.
