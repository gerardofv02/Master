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
db.Movies.aggregate([
    {$match : {$and: [{'year': {$gte: 1960}}, {'year': {$lte: 1969}}]}},
    { $group: {'_id': '$year', 'total' : {$sum: 1}}}
    ]).sort({'_id': 1})
/* Fin Ejercicio 14 */


