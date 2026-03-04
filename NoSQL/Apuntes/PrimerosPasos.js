use Master;
/*db.createCollection("Master_Prueba", {
      validator: { $jsonSchema: {
         bsonType: "object",
         required: [ "phone" ],
         properties: {
            phone: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            email: {
               bsonType : "string",
               pattern : "@test\.com$",
               description: "must be a string and match the regular expression pattern"
            },
            status: {
               enum: [ "Unknown", "Incomplete" ],
               description: "can only be one of the enum values"
            }
         }
      } }
});
*/
let a = db.getCollection('Master_Prueba');
print(a.find());