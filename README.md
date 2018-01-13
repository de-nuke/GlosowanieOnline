# GlosowanieOnline

  cd postgres
  sudo docker build -t me/postgres .
  cd ..
  cd web
  sudo docker build -t me/web .
  cd ..
  cd nginx 
  sudo docker build -t me/nginx .
  cd ..
  cd webfront
  sudo docker build -t me/webfront .
  cd ..
  sudo docker volume create --name postgres-data
  sudo docker run -d --name postgres --volume postgres-data:/var/lib/postgresql me/postgres
  sudo docker run -d --name web --link postgres:postgres --env-file web/web.env me/web
  sudo docker run -d --name nginx --volumes-from web --link web:web --publish XXXX:80  me/nginx
 (XXXX - port dla flaskowej apki do API)
  sudo docker run -d -p 5000:5000 me/webfront
  sudo docker exec web python create_db.py
  
W przeglądarce powinno działać zarówno 'http://localhost:XXXX' (dla API) jak i 'http://localhost:5000' dla apki ze stroną internetową
  
