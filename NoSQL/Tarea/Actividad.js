/* Comienzo Ejercicio 1 */
use Master;
db.Movies.find()
/* Fin Ejercicio 1 */

/* Comienzo Ejercicio 2 */
db.Movies.find().count()
/* Fin Ejercicio 2 */

/* Comienzo Ejercicio 3 */
db.Movies.insertOne({"title": "test", "year":1800, "cast":[], "genres": []})
/* Fin Ejercicio 3 */

/* Comienzo Ejercicio 4 */
var pelicula = {"title": "test", "year":1800, "cast":[], "genres": []}
db.Movies.deleteOne(pelicula)
/* Fin Ejercicio 4 */

/* Comienzo Ejercicio 5 */
var query_and = {"cast": {$all: ['and']}}
db.Movies.find(query_and).count()
/* Fin Ejercicio 5 */

/* Comienzo Ejercicio 6 */
var query_and = {"cast": {$all: ['and']}}
db.Movies.updateMany(query_and,{$pull: {'cast': 'and'}})
/* Fin Ejercicio 6 */

/* Comienzo Ejercicio 7 */
var query_size0 = {"cast": {$size: 0}}
db.Movies.find(query_size0).count()
/* Fin Ejercicio 7 */

/* Comienzo Ejercicio 8 */
var query_size0 = {"cast": {$size: 0}}
db.Movies.updateMany(query_size0, {$push:{'cast': 'Undefined'}})
/* Fin Ejercicio 8 */

/* Comienzo Ejercicio 9 */
var query_size_genres0 = {"genres": {$size: 0}}
db.Movies.find(query_size_genres0).count()
/* Fin Ejercicio 9 */

/* Comienzo Ejercicio 10 */
var query_size_genres0 = {"genres": {$size: 0}}
db.Movies.updateMany(query_size_genres0, {$push:{'genres': 'Undefined'}})
/* Fin Ejercicio 10 */

/* Comienzo Ejercicio 11 */
var query_anno_reciente = {}
var projection_anno = {"year":1, "_id": 0}
db.Movies.find(query_anno_reciente,projection_anno).sort({'year': -1}).limit(1)
/* Fin Ejercicio 11 */

/* Comienzo Ejercicio 12 */
db.Movies.aggregate([
    {$match : {'year': {$gte: (1960-20)}}},
    { $group: {'_id': '$year', 'total' : {$sum: 1}}}
    ]).sort({'_id': 1})
/* Fin Ejercicio 12 */

/* Comienzo Ejercicio 13 */
db.Movies.aggregate([
    {$match : {$and: [{'year': {$gte: 1960}}, {'year': {$lte: 1969}}]}},
    { $group: {'_id': '$year', 'total' : {$sum: 1}}}
    ]).sort({'_id': 1})
/* Fin Ejercicio 13 */

/* Comienzo Ejercicio 14 */
var year_most_total = db.Movies.aggregate([
    { $group: {'_id': '$year', 'total' : {$sum: 1}}}
    ]).sort({'total': -1}).limit(1).toArray()
//una vez sacamos el total más alto, buscamos por este valor:
var total_maximo = year_most_total[0].total
total_maximo
db.Movies.aggregate([
    { $group: {'_id': '$year', 'total' : {$sum: 1}}},
    {$match : {'total': {$eq : total_maximo}}}
    ]).sort({'total': 1})
/* Fin Ejercicio 14 */

/* Comienzo Ejercicio 15 */
var year_least_total = db.Movies.aggregate([
    { $group: {'_id': '$year', 'total' : {$sum: 1}}}
    ]).sort({'total': 1}).limit(1).toArray()
//una vez sacamos el total más alto, buscamos por este valor:
var total_minimo = year_least_total[0].total
total_minimo
db.Movies.aggregate([
    { $group: {'_id': '$year', 'total' : {$sum: 1}}},
    {$match : {'total': {$eq : total_minimo}}}
    ]).sort({'total': 1})
/* Fin Ejercicio 15 */

/* Comienzo Ejercicio 16 */
var fase_unwind = {$unwind: '$cast'}
var query_no_repetidos = {'_id': 0} //quitamos el id para no generar errores de duplicados
var fase_no_repetidos = { $project: query_no_repetidos}
var fase_out = {$out: 'actors'}
var etapas = [fase_unwind,fase_no_repetidos,fase_out]
db.Movies.aggregate(etapas)
//probamos y contamos
db.actors.find().count()
/* Fin Ejercicio 16 */

/* Comienzo Ejercicio 17 */
db.actors.aggregate([
    {$match: {'cast': {$ne: 'Undefined'}}},
    {$group: {'_id': '$cast', 'total_pelis': {$sum:1}}}
    ]).sort({'total_pelis': -1}).limit(5)
/* Fin Ejercicio 17 */

/* Comienzo Ejercicio 18 */
db.actors.aggregate([
    {$group: {'_id': {'title': '$title','year': '$year'}, 'total_actors': {$sum:1}}}
    ]).sort({'total_actors': -1}).limit(5)
/* Fin Ejercicio 18 */

/* Comienzo Ejercicio 19 */
db.actors.aggregate([
    {$match: {'cast': {$ne: 'Undefined'}}},
    {$group: {'_id': '$cast','comienza': {$min: '$year'},'termina':{$max: '$year'}}},
    {$addFields:{'años':{ $subtract: ['$termina','$comienza']}}}
    ]).sort({'años': -1}).limit(5)
/* Fin Ejercicio 19 */

/* Comienzo Ejercicio 20 */
var fase_unwind = {$unwind: '$genres'}
var query_no_repetidos = {'_id': 0} //quitamos el id para no generar errores de duplicados
var fase_no_repetidos = { $project: query_no_repetidos}
var fase_out = {$out: 'genres'}
var etapas = [fase_unwind,fase_no_repetidos,fase_out]
db.actors.aggregate(etapas)
//probamos y contamos
db.genres.find().count()
/* Fin Ejercicio 20 */

/* Comienzo Ejercicio 21 */
db.genres.aggregate([
    {$match: {'genres': {$ne: 'Undefined'}}},
    {$group: {'_id': {'generos': '$genres', 'year': '$year'}, 'total_pelis': {$sum: 1}}}
    ]).sort({'total_pelis': -1}).limit(5)
/* Fin Ejercicio 21 */

/* Comienzo Ejercicio 22 */
db.genres.aggregate([
    {$match: {'cast': {$ne: 'Undefined'}}},
    {$group: {'_id': '$cast', 'generos': {$addToSet: '$genres'}}},
    {$addFields:{'numgeneros': {$size: '$generos'}}}
    ]).sort({'numgeneros': -1}).limit(5)
/* Fin Ejercicio 22 */

/* Comienzo Ejercicio 23 */
db.genres.aggregate([
    {$match: {'genres': {$ne: 'Undefined'}}},
    {$group: {'_id': {'title': '$title', 'year': '$year'}, 'generos': {$addToSet: '$genres'}}},
    {$addFields:{'numgeneros': {$size: '$generos'}}}
    ]).sort({'numgeneros': -1}).limit(5)
/* Fin Ejercicio 23 */

/* Comienzo Ejercicio 24 */
db.genres.aggregate([
    {$match: {'genres': {$ne: 'Undefined'}}},
    {$group: {'_id': '$genres', 'peliculas': {$addToSet: '$title'}}},
    {$addFields: {'total_pelis': {$size: '$peliculas'}}}
    ]).sort({'total_pelis': -1}).limit(5)
/* Fin Ejercicio 24 */

/* Comienzo Ejercicio 25 */
db.genres.aggregate([
    {$match: {'cast': {$ne: 'Undefined'}, 'genres': {$ne: 'Undefined'}}},
    {$group: {'_id': '$cast', 'generos': {$addToSet: '$genres'}}},
    {$match: {$expr: {$eq: [{$size: '$generos'}, 1]}}},
    {$addFields:{'numgeneros': {$size: '$generos'}}}
    ]).sort({'numgeneros': -1})
/* Fin Ejercicio 25 */

/* Comienzo Ejercicio 26 */
db.actors.aggregate([
    {$match: {'cast': {$ne: 'Undefined'}}},
    {$group: {'_id': '$cast','peliculas': {$addToSet: '$title'}}},
    {$addFields: {'total_pelis': {$size: '$peliculas'}}},
    {$match: {'total_pelis' : {$gt: 10}}}
    ]).sort({'total_pelis': 1})
/* Fin Ejercicio 26 */
