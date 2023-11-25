# DeployWebOnAzure
Build Image
docker build -t my_flask_app .  

Run Image
docker run -e ConnectionString="postgresql://postgresql:Dang0511!@postgresqlwebapp.postgres.database.azure.com:5432/user_database" -p 5000:5000 my_flask_app

Tag Image
docker tag my_flask_app danuxpeach/my_flask_app:latest 

Push Image
docker push  danuxpeach/my_flask_app:latest 

Use WebApp on Azure to deploy and config env 
ConnectionString="postgresql://postgresql:Dang0511!@postgresqlwebapp.postgres.database.azure.com:5432/user_database"
