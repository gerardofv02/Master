use Master;
db.createCollection("Master_Prueba_Carga", {
   validator: { $jsonSchema: {
      bsonType: "object",
      required: ["phone"],
      properties: {
         phone: {
            bsonType: "string",
            description: "must be a string and is required"
         },
         email: {
            bsonType: "string",
            pattern: "@test\\.com$",
            description: "must match the regex"
         },
         status: {
            enum: ["unknown", "incomplete"],
            description: "allowed values"
         }
      }
   }}
});

use Master

db

show collections

db.Master_Primera_Clase.insertOne({"test": "test"})
db.Master_Primera_Clase.find()

show dbs
use Master
show collections
/* Comienzo de insertar a una persona*/
/*
var new_persona = {"nombre": "jerry",
"email": "jerry@test.com",
"edad": 23,
"phone": "999999999"}
db.Master_Prueba_Carga.insertOne(new_persona)
db.Master_Prueba_Carga.find()
*/
/*Fin de insertar a una sola persona*/

/*Comienzo insertar a varias personas*/
/*
var new_persona_varias = [{"nombre": "jerry2",
"email": "jerry2@test.com",
"edad": 24,
"phone": "888888888"},
{"nombre": "jerry3",
"email": "jerry3@test.com",
"edad": 25,
"phone": "777777777"}
]
db.Master_Prueba_Carga.insertMany(new_persona_varias)
db.Master_Prueba_Carga.find()
*/
/*Fin de insertar a varias  persona*/

/*Comenzamos jugando con los finds*/
/* Por defecto en las queries se mostraran todos los atributos de los registros
que se quieren obtener
Si no se quieren mostrar los atributos se tiene que indicar en el find:
find(qyery,projection)
ejemplo: find({"edad":24},{"phone":1, "_id": 0, "nombre": 1}
0 -> no muestra
1-> muestra
cuando ya hay un campo con un uno, solo muestra ese*/
var query = {"edad": 24} // Buscamos aquellas personas cuya edad sea 24
var query2 = {"edad": {$gte: 20}} //mayor que 10
var query3 = {"edad": {$lt: 30}} //menor que 30
var projection = {"phone":1, "_id": 0, "nombre": 1}
var projection2 = {"phone": 0}
db.Master_Prueba_Carga.find(query3, projection2)
/*Fin jugando con los finds*/

/*Comenzamos jugando con los updates*/
/* Para actualizar datos en una coleccion*/
/* Los operadores mas importantes:
Operadores <Update>
● $currentDate. Establece el valor de un campo en la
fecha actual.
● $inc. Incrementa el valor del campo en la cantidad
especificada.
● $min. Modifica al valor especificado si es menor que
este.
● $max. Modifica al valor especificado si es mayor que
este.
● $mul. Multiplica el valor del campo por la cantidad
especificada.
● $rename. Renombra el nombre de un campo.
● $set. Actualiza o añade el valor de/a un campo.
● $setOnInsert. Actualiza o añade el valor de/a un
campo si update inserta un documento.
● $unset. Elimina el campo especificado.*/
var query4 = {}
var operacion = {$set: {"campo": "borrar"}}
db.Master_Prueba_Carga.updateMany(query4, operacion)
db.Master_Prueba_Carga.find()

//var query5 = {"edad": {$lt: 30}}
var query5 = {"edad": {$gte: 30}}
var operacion2 = {$unset: {"campo": "borrar"}}
db.Master_Prueba_Carga.updateMany(query5,operacion2)
db.Master_Prueba_Carga.find()

/*Fin jugando con los updates*/

/* Comenzamos jugando con los deletes*/
/* Basicamnete los deletes son para vorrar registros de distintas colecciones con la query que se quiera indicar*/
var reg = {"prueba": "orrado", "phone": "aa"}
db.Master_Prueba_Carga.insertOne(reg)
db.Master_Prueba_Carga.find()

db.Master_Prueba_Carga.deleteOne(reg)

var query6 = {"nombre": "jerry2"}
db.Master_Prueba_Carga.deleteMany(query6)
db.Master_Prueba_Carga.find()
/* Fin jugando con los deletes*/

/* Jugando con los finds avanzados*/
/* Posibles selectores:
● $eq. Igual al valor especificado
● $gt. Mayor que valor especificado
● $gte. Mayor o igual que valor especificado
● $in. Cualquier valor de los especificados (array)
● $lt. Menor que valor especificado
● $lte. Menos o igual que valor especificado
● $ne. Distinto de valor especificado
● $nin. Cualquier valor que no esté especificado (array)


$and. Que cumpla todas las condiciones especificadas (array de filtros)
● $not. Invierte las condición especificada (filtros)
● $nor. NOT OR ((!expr1)AND!(!expr2)) (array de filtros)
● $or. Que cumpla algunas de las condiciones especificadas (array de
filtros)
Elementos
● $exists. Que contiene el campo o no (true/false)
● $type. Filtra por el tipo
Evaluacion
● $expr. Permite el uso de expresiones de agregación dentro de la query.
● $mod. Realiza una operación de módulo en el valor de un campo y
selecciona documentos con un resultado específico.
● $regex. Permite expresiones regulares.
● $text. Búsquedas de texto.
● $jsonSchema. Búsquedas de texto.

*/

/* Fin con los finds avanzados*/

