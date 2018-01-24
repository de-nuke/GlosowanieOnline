# GlosowanieOnline
Uruchomienie

  * `chmod +x build_all.sh run_all.sh`
  * `./build_all.sh`
  * `./run_all.sh`
  * `docker exec web python src/create_db.py`

**Jesli bedzie coś nie tak podczas buildowania** (./build\_all.sh):
W Dockerfile zarowno w `web/` jak i w `webfront/` **usuncie** z tych linijek:
  * (web)`RUN echo nameserver 10.30.0.132 >> /etc/resolv.conf && pip3 install --no-cache-dir -r requirements.txt`
  * (webfront)`RUN echo nameserver 10.30.0.132 >> /etc/resolv.conf && pip install -r requirements.txt`
  
ten fragment:
  * `echo nameserver 10.30.0.132 >> /etc/resolv.conf &&`

---------------------------------
Wyczyszczenie bazy: `sudo docker exec web python src/drop_db.py`
Reset głosowania: `sudo docker exec web python src/reset_votes.py`
Wpisanie przykładowych danych: `sudo docker exec web python src/create_db.py`

----------------------------------

API:
* http://localhost:8001/admin (GET), przeglądarka
* http://localhost:8001/vote (POST - token + candidate_id)
* http://localhost:8001/results (GET)
* http://localhost:8001/candidates (GET)
* http://localhost:8001/login (POST - first_name, last_name, father_name, mother_name, id_series_number, pesel)
* http://localhost:8001/candidate/[id] (GET)
 
WWW: http://localhost:8002/site/login - przykladowy adres. Liczy sie PORT 
