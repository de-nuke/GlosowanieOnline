# GlosowanieOnline
Uruchomienie

  * `chmod +x build_all.sh run_all.sh`
  * `./build_all.sh`
  * `./run_all.sh`
  

**Jesli bedzie coś nie tak podczas buildowania** (./build\_all.sh):
W Dockerfile zarowno w `web/` jak i w `webfront/` **usuncie** z tych linijek:
  * (web)`RUN echo nameserver 10.30.0.132 >> /etc/resolv.conf && pip3 install --no-cache-dir -r requirements.txt`
  * (webfront)`RUN echo nameserver 10.30.0.132 >> /etc/resolv.conf && pip install -r requirements.txt`
  
ten fragment:
  * `echo nameserver 10.30.0.132 >> /etc/resolv.conf &&`

----------------------------------
W przeglądarce:

API: http://localhost:8001/makosak/notes/2 - przykladowy adres. Liczy sie PORT

WWW: http://localhost:8002/site/login - przykladowy adres. Liczy sie PORT 
