const{MongoCLient, MongoClient} = require('mongodb');
async function main(){
    const uri = "mongodb+srv://jackbardoe:William1@r0s5.hxkyr5l.mongodb.net/?retryWrites=true&w=majority"
    const client = new MongoClient(uri);
    try{
        await client.connect();
        await listDatabses(client);
    }
    catch(e){
        console.error(e);
    }
    finally{
        await client.close();
    }

}