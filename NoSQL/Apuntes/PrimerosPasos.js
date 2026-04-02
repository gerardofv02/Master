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
var query5 = {"edad": {$gte: 20}}
var query7 =  {"edad": {$eq:25}}
var query6 = {"edad": {$lte: 22}}
var logic = {$and: [query5,query6]} //Con esto decimos aquellos que cumplan ambas condiciones
var logic2 = {$nor: [query6,query7]}//Con esto decimos aquellos que no cumplan ninguna de las dos condicones
db.Master_Prueba_Carga.find(logic2)

var query = {"edad": {$exists: true}}
db.Master_Prueba_Carga.find(query)

var query = {"noexiste": {$exists: false}}
var operacion = {$set: {"siexiste": null}}
//como si existe el campo, no me crea el otro campo. Si no existiese dicho campo, me lo crearía
db.Master_Prueba_Carga.updateOne(query, operacion)
db.Master_Prueba_Carga.find()

//para buscar por tipo de campo (string, double, null):

var query = {"noexiste": {$type: "null"}}
db.Master_Prueba_Carga.find(query)
/* Fin con los finds avanzados*/

/* Documentos embebidos comeinzo*/

var array_personas = [
    {"nombre":"jerry4", "email":"trest@test.com", "edad_telefono": {"edad": 22, "phone": "7837129879"}, "phone": "7837129879",  "campo": null  },
    {"nombre":"jerry5", "email":"trest5@test.com", "edad_telefono": {"edad": 25, "phone": "7835129879"}, "phone": "7837129879", "campo": null  },
    {"nombre":"jerry6", "email":"trest6@test.com", "edad_telefono": {"edad": 26, "phone": "7836129879"}, "phone": "7837129879", "campo": null  },
    {"nombre":"jerry7", "email":"trest7@test.com", "edad_telefono": {"edad": 27, "phone": "7837829879"}, "phone": "7837129879", "campo": null  }
    ]
    
db.Master_Prueba_Carga.insertMany(array_personas)
//para buscar estos campos especiales, se hace con el punto (como llamando a un atributo de un objeto en progra)
//ejemplo:
var query = {"edad_telefono.edad": {$gte: 26}}

db.Master_Prueba_Carga.find(query)
db.Master_Prueba_Carga.find()

/* Inicio probando arrays*/
var array_personas2 = [
    {"nombre":"jerry8", "email":"trest@test.com", "edad_telefono": {"edad": 22, "phone": "78371295879"}, "phone": "7837729879",  "campo": null, "color_fav": ['red','green']  },
    {"nombre":"jerry9", "email":"trest5@test.com", "edad_telefono": {"edad": 25, "phone": "78351294879"}, "phone": "78374129879", "campo": null,"color_fav": ['green','red']  },
    {"nombre":"jerry10", "email":"trest6@test.com", "edad_telefono": {"edad": 26, "phone": "783612934879"}, "phone": "78374129879", "campo": null,"color_fav": ['blue','green']  },
    {"nombre":"jerry11", "email":"trest7@test.com", "edad_telefono": {"edad": 27, "phone": "78378298759"}, "phone": "78371529879", "campo": null,  "color_fav": ['orange','pink']}
    ]
    
var persona3 = {"nombre":"jerry9", "email":"trest@test.com", "edad_telefono": {"edad": 22, "phone": "783471295879"}, "phone": "78374729879",  "campo": null, "color_fav": ['red','green','orange']  }
db.Master_Prueba_Carga.insertOne(persona3)
db.Master_Prueba_Carga.insertMany(array_personas2)

var query_array = {color_fav: ['red','green']} // Se tiene que poner exactamente los valores y en el orden correcto

var query_array2 = {color_fav: {$all:['red','green']}} //obtiene todas las que tengan estos dos tags independientemente del orden o si tienen más elementos el array

var query_array3 = {color_fav: 'red'} // opbitne todos los registros en el cual tenga como valor en color favortio red pero en cualquier posicion del array

//se usal $elemMatch para que ambas condiciones que se den tengan que cumplirse

var query_array4 = {"color_fav.1" : 'red'} //sirve para obtener aquellos registros donde la posición del array del campo color fav, el elemento 1 sea rojo >(se comineza desde 0 siempre)

var query_array5 = {color_fav: {$in: ['red','pink']}} //obtiene todos los registros en los cualqes el array contenga 'red' o pink (uno u otro)

var query_array6 = {color_fav: {$nin: ['red','pink']}} //obtiene todos los registros en los cualqes el array no contenga 'red' ni pink (ni uno ni otro)

var query_array7 = {color_fav :{$size:3}} //devuelve aquellos registros donde el tamaño del array del campo valga 3 en este caso

db.Master_Prueba_Carga.find(query_array7)

/* Ahora vamos con los arrays de obtetos o documentos embebidos */

var array_personas2 = [
    {"nombre":"jerry8", "email":"trest@test.com", "edad_telefono": {"edad": 22, "phone": "78371295879"}, "phone": "7837729879",  "campo": null, "color_fav": [{"color": 'red', "poscion": 2},{"color": 'green', "posicion":1}]  },
    {"nombre":"jerry9", "email":"trest5@test.com", "edad_telefono": {"edad": 25, "phone": "78351294879"}, "phone": "78374129879", "campo": null,"color_fav": [{"color": 'green', "poscion": 2},{"color": 'red', "posicion":1}]  },
    {"nombre":"jerry10", "email":"trest6@test.com", "edad_telefono": {"edad": 26, "phone": "783612934879"}, "phone": "78374129879", "campo": null,"color_fav": [{"color": 'blue', "poscion": 2},{"color": 'green', "posicion":1}] },
    {"nombre":"jerry11", "email":"trest7@test.com", "edad_telefono": {"edad": 27, "phone": "78378298759"}, "phone": "78371529879", "campo": null,  "color_fav": [{"color": 'orange', "poscion": 2},{"color": 'pink', "posicion":1}]}
    ]
    
var persona3 = {"nombre":"jerry9", "email":"trest@test.com", "edad_telefono": {"edad": 22, "phone": "783471295879"}, "phone": "78374729879",  "campo": null, "color_fav": [{"color": 'red', "poscion": 2},{"color": 'green', "posicion":1}, {"color": 'orange', "posicion": 3}] }
db.Master_Prueba_Carga.insertOne(persona3)
db.Master_Prueba_Carga.insertMany(array_personas2)

var query_array = {'color_fav.color':'red'} //me buscar cualquier registro donde dentro del array de objetos el atributo collor valga red (cualquiera)

var query_array1 = {'color_fav.0.color': 'red'} //me busca caulquier registro dopnde dentro del array de objetos el atribito color del PRIMER obtjeto del array sea 'red'

db.Master_Prueba_Carga.find(query_array)

/*
Elementos imporantes de los arrays con el find:
Filtros
$all. Encuentra arrays que contienen todos los
elementos especificados en la consulta
$elemMatch. Selecciona documentos si el
elemento en el campo del array coincide con
todas las condiciones especificadas de
$elemMatch
$size. Selecciona si tiene el tamaño especificado
Proyecciones
$. Selecciona el primer elemento del array
$elemMatch. Muestra los campos si cumple
criterios
$slice. Controla el número de elementos de un
array que devuelve una consulta
Modificadores
$each . Para añadir varios items
$position. Especifica la posición en el array
$slice. Limita el tamaño del array
$sort. Reordena el array
Update
$. Actúa como un marcador de posición para
actualizar el primer elemento que coincide con
la condición de consulta
$[]. Actúa como un marcador de posición para
actualizar todos los elementos que coinciden
con la condición de consulta
$[<identifier>]. Actúa como un marcador de
posición para actualizar todos los elementos que
coinciden con la condición de consulta de
ArrayFilters.
$addToSet. Agrega elementos a un array sólo si
aún no existen en el conjunto.
$pop. Elimina el primer o último elemento de un
array
$pull. Elimina todos los elementos de un array
especificada en una query
$push. Añade un item al array
$pullAll. Elimina todos los elementos de un
arrayx
find() devuelve un cursor de documentos que se puede iterar. Las funciones principales son:
● close. Cierra el cursor.
● count. Cuenta número de documentos del cursor original (sin iterar)
● forEach. Aplicar una función a todos los documentos del cursor
● hasNext. Devuelve true o false si quedan documentos que iterar.
● skip. Salta número de documentos.
● limit. Limita número de documentos del cursor.
● next. Itera el siguiente documento.
● pretty. Mostrar JSON más visual.
● size. Cuenta número documentos después de realizar limit y/o skip.
● sort. Ordena la salida.
● toArray. Itera cursor y lo asigna a un array.



*/

/* Fin probando arrays*/

/* Vamos con los cursores */
// Ordenamos de forma ascencente:
db.Master_Prueba_Carga.find().sort({phone: 1})

// Ordenamos de forma descendente
db.Master_Prueba_Carga.find().sort({phone: -1})

// Limit para limitar la cantidad de registros que aparezcan:

db.Master_Prueba_Carga.find().limit(2) //solo dos registros

// Skip para saltar x registros
db.Master_Prueba_Carga.find().sort({phone: 1}).limit(2).skip(3) // salta 3 registros

//Count para saber la cantidad de registros que hay
db.Master_Prueba_Carga.find().count()

// hasNext para saber si hay algun registro despues o no
db.Master_Prueba_Carga.find().skip(1).hasNext()//devuelve true porq hay mas de 1 registro

db.Master_Prueba_Carga.find().skip(db.Master_Prueba_Carga.find().count()).hasNext()//devuelve false porq no hay mas registros despues del ultimo

// next sirve para devolver el siquiente curosr
db.Master_Prueba_Carga.find().skip(1).next() 

//pretty para mostrar el json mas visual (como el pretty json de visual studio code)
//Size: igual que el count pero para contar los elementos una vez hecho el skip
db.Master_Prueba_Carga.find().skip(5).size()    

//toArray para convertirlo en un array

//probando pull


var query_red = {"color_fav": {$all: ['red']}}
db.Master_Prueba_Carga.find(query_red).count()

var query_red = {"color_fav": {$all: ['red']}}
db.Master_Prueba_Carga.updateMany(query_red,{$pull: {'color_fav': 'red'}})

// probando arrays vacios
var query_size_0 = {"color_fav": {$size: 0}}
db.Master_Prueba_Carga.find(query_size_0)

//probando push
var query_size_0 = {"color_fav": {$size: 0}}
db.Master_Prueba_Carga.updateMany(query_size_0,{$push: {'color_fav': 'red'}})

//probando el para devolver el valor maximo de la edad
var query_edad_reciente = {}
var projection_edad = {"edad":1, "_id": 0}
db.Master_Prueba_Carga.find(query_edad_reciente,projection_edad).sort({'edad': -1}).limit(1)