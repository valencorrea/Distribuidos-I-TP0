# TP0: Docker + Comunicaciones + Concurrencia

## Reentrega

#### A corregir
1. Falta close de client sockets en "happy path" y cuando se ejecuta el SIGTERM
2. No haces lock para el store_bets en "happy path" AUNQUE lo tenés ahí disponible
3. No manejas correctamente el corte de paquetes con \n en el server: puede ser que leas un paquete y parte del siguiente que va a quedar corrupto (receive_client_bets)
4. Usas threads pero no explicas por qué está bien utilizarlos en este caso de uso para python

#### Cambios realizados
1a. Se agrega el cierre del socket con el cual se este comunicando en ese momento el servidor en ese momento, inmediatamente despues de haberle enviado los documentos ganadores del sorteo.
1b. Se agrega un lockeo para el diccionario de clientes dentro de exit_gracefully para poder cerrar cada socket addres en caso de que se ejecute SIGTERM.
2. Si bien se habia agregado una variable en servidor self._bets_lock y en register_bet se utilizaba en una de las invocaciones a store_bets, 
se agrego tambien el lock para cuando se hace la ultima invocacion al final del bucle ya que alli no se estaba realizando.
3. 
4. 



